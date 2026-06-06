"""
surface_builder.py —— 量子点表面识别模块
"""

import os
import json
import argparse
import numpy as np
from ase.io import read, write

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def compute_coordination_numbers(atoms, cutoff=3.0):
    pos = atoms.get_positions()
    n = len(atoms)
    cn = np.zeros(n, dtype=int)
    for i in range(n):
        d = np.linalg.norm(pos - pos[i], axis=1)
        cn[i] = int(np.sum((d > 1e-8) & (d < cutoff)))
    return cn

def identify_surface_atoms(atoms, cutoff=3.0):
    cn = compute_coordination_numbers(atoms, cutoff=cutoff)
    threshold = max(1, int(np.mean(cn)) - 1)
    surface = [i for i, c in enumerate(cn) if c <= threshold]
    return surface, cn.tolist()

def build_surface_model(structure_file, output_dir="qd_surface_out"):
    ensure_dir(output_dir)
    atoms = read(structure_file)
    atoms.set_pbc(False)
    surface, cn = identify_surface_atoms(atoms)
    write(os.path.join(output_dir, "qd_surface.xyz"), atoms)
    with open(os.path.join(output_dir, "surface_atoms.json"), "w") as f:
        json.dump({"surface_atoms": surface, "coordination_numbers": cn}, f, indent=2)
    return surface

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QD surface builder")
    parser.add_argument("structure_file")
    parser.add_argument("--out", default="qd_surface_out")
    args = parser.parse_args()
    surf = build_surface_model(args.structure_file, args.out)
    print(f"[surface_builder] surface atoms: {len(surf)}")

