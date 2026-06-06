"""
ligand_design.py —— 量子点表面配体构型生成模块
"""

import os
import json
import argparse
import numpy as np
from ase.io import read, write
from ligand_library import get_ligands_by_category, ligand_to_dict

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def unit(v):
    n = np.linalg.norm(v)
    return v / (n + 1e-9)

def add_simple_ligand(atoms, site_index, ligand_name, bond_length=2.0):
    pos = atoms.positions[site_index]
    neighbors = [atoms.positions[j] - pos for j in range(len(atoms)) if j != site_index and np.linalg.norm(atoms.positions[j] - pos) < 3.0]
    normal = unit(-np.mean(neighbors, axis=0)) if neighbors else np.array([0.0, 0.0, 1.0])
    lig = ligand_name.lower()

    if lig in ["cl-", "br-", "i-", "formate", "acetate", "oleate", "scn-"]:
        atoms.append("Cl")
        atoms[-1].position = pos + normal * bond_length
    elif lig in ["ammonia", "amine", "pyridine", "top", "tpp"]:
        atoms.append("N")
        atoms[-1].position = pos + normal * bond_length
    elif lig in ["zncl2", "cdcl2", "pbcl2", "b(c6f5)3"]:
        atoms.append("B")
        atoms[-1].position = pos + normal * bond_length
    else:
        atoms.append("H")
        atoms[-1].position = pos + normal * bond_length

    return atoms

def generate_candidates(structure_file, category="ALL", coverage=0.5, output_dir="ligand_design_out"):
    ensure_dir(output_dir)
    atoms = read(structure_file)
    atoms.set_pbc(False)

    ligands = get_ligands_by_category(category)
    n_surface = max(1, int(len(atoms) * 0.2))
    site_indices = list(range(min(n_surface, len(atoms))))
    candidate_records = []

    for lig in ligands:
        new_atoms = atoms.copy()
        n_attach = max(1, int(len(site_indices) * float(coverage)))
        attach_sites = site_indices[:n_attach]
        for idx in attach_sites:
            new_atoms = add_simple_ligand(new_atoms, idx, lig.name)
        fname = f"{lig.category}_{lig.name}_candidate.xyz"
        write(os.path.join(output_dir, fname), new_atoms)
        candidate_records.append({
            "ligand": ligand_to_dict(lig),
            "file": fname,
            "attach_sites": attach_sites,
        })

    with open(os.path.join(output_dir, "ligand_candidate_summary.json"), "w") as f:
        json.dump(candidate_records, f, indent=2)

    return candidate_records

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ligand design")
    parser.add_argument("structure_file")
    parser.add_argument("--category", default="ALL")
    parser.add_argument("--coverage", default="0.5")
    parser.add_argument("--out", default="ligand_design_out")
    args = parser.parse_args()
    recs = generate_candidates(args.structure_file, args.category, args.coverage, args.out)
    print(f"[ligand_design] generated {len(recs)} candidates")

