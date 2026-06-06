"""
mace_opt.py —— 基于机器学习力场的结构优化模块

说明：此处提供一个可独立运行的简化能量优化实现，
用于软著源码正文展示。正式项目中可将 energy_model
替换为真实的 MACE 力场接口。
"""

import os
import csv
import json
import argparse
import numpy as np
from ase.io import read, write

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def pairwise_repulsion_energy(atoms, cutoff=3.0):
    """
    简化的结构能量函数：
    1) 原子之间距离过近时引入排斥项；
    2) 距离过远则贡献较小；
    3) 用于候选方案快速排序。
    """
    pos = atoms.get_positions()
    syms = atoms.get_chemical_symbols()
    n = len(atoms)
    e = 0.0

    for i in range(n):
        for j in range(i + 1, n):
            r = np.linalg.norm(pos[i] - pos[j])
            if r < 1e-6:
                e += 100.0
            elif r < cutoff:
                e += (cutoff - r) ** 2
    return e

def mock_mace_relax(atoms, n_steps=50, step_size=0.01):
    """
    简化弛豫：对过近原子施加轻微“推开”操作。
    该函数用于示意 MACE 优化接口，输出可重复的优化结构。
    """
    atoms = atoms.copy()
    pos = atoms.get_positions()
    n = len(atoms)

    for _ in range(n_steps):
        forces = np.zeros_like(pos)
        for i in range(n):
            for j in range(i + 1, n):
                d = pos[i] - pos[j]
                r = np.linalg.norm(d) + 1e-12
                if r < 2.0:
                    f = (2.0 - r) * d / r
                    forces[i] += f
                    forces[j] -= f
        pos += step_size * forces

    atoms.set_positions(pos)
    return atoms

def optimize_structure(input_file, output_dir="mace_opt_out", steps=200):
    ensure_dir(output_dir)
    atoms = read(input_file)
    atoms.set_pbc(False)

    opt_atoms = mock_mace_relax(atoms, n_steps=max(20, steps // 4))
    energy = pairwise_repulsion_energy(opt_atoms)

    out_file = os.path.join(output_dir, "optimized_structure.xyz")
    write(out_file, opt_atoms)

    with open(os.path.join(output_dir, "energy_table.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["structure", "total_energy"])
        writer.writerow([os.path.basename(input_file), energy])

    with open(os.path.join(output_dir, "energy_rank.json"), "w") as f:
        json.dump({"structure": os.path.basename(input_file), "total_energy": energy}, f, indent=2)

    return energy, out_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MACE optimization")
    parser.add_argument("input_file")
    parser.add_argument("--out", default="mace_opt_out")
    parser.add_argument("--steps", default="200")
    args = parser.parse_args()
    e, out = optimize_structure(args.input_file, args.out, int(args.steps))
    print(f"[mace_opt] energy = {e:.6f}, saved to {out}")

