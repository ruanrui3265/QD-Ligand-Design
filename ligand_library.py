"""
ligand_library.py —— 量子点配体库管理模块
"""

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Ligand:
    name: str
    category: str
    smiles: str
    donor_atom: str
    description: str

X_LIGANDS = [
    Ligand("Cl-", "X", "[Cl-]", "Cl", "chloride ligand"),
    Ligand("Br-", "X", "[Br-]", "Br", "bromide ligand"),
    Ligand("I-", "X", "[I-]", "I", "iodide ligand"),
    Ligand("formate", "X", "C(=O)[O-]", "O", "formate ligand"),
    Ligand("acetate", "X", "CC(=O)[O-]", "O", "acetate ligand"),
    Ligand("oleate", "X", "CCCCCCCC/C=C\\CCCCCCCCCC(=O)[O-]", "O", "oleate ligand"),
    Ligand("SCN-", "X", "N#CS", "S", "thiocyanate ligand"),
]

Y_LIGANDS = [
    Ligand("ammonia", "Y", "N", "N", "ammonia ligand"),
    Ligand("amine", "Y", "CCCCCCCCCCN", "N", "alkylamine ligand"),
    Ligand("pyridine", "Y", "n1ccccc1", "N", "pyridine ligand"),
    Ligand("TOP", "Y", "P(CCCCC)(CCCCC)CCCCC", "P", "trioctylphosphine ligand"),
    Ligand("TPP", "Y", "P(c1ccccc1)(c1ccccc1)c1ccccc1", "P", "triphenylphosphine ligand"),
]

Z_LIGANDS = [
    Ligand("ZnCl2", "Z", "Cl[Zn]Cl", "Zn", "zinc chloride"),
    Ligand("CdCl2", "Z", "Cl[Cd]Cl", "Cd", "cadmium chloride"),
    Ligand("PbCl2", "Z", "Cl[Pb]Cl", "Pb", "lead chloride"),
    Ligand("B(C6F5)3", "Z", "Fc1c(F)c(F)c(B(c2c(F)c(F)c(F)c(F)c2F)c2c(F)c(F)c(F)c(F)c2F)c(F)c1F", "B", "Lewis acid ligand"),
]

def get_all_ligands() -> List[Ligand]:
    return X_LIGANDS + Y_LIGANDS + Z_LIGANDS

def get_ligands_by_category(category: str) -> List[Ligand]:
    category = category.upper()
    if category == "X":
        return X_LIGANDS
    if category == "Y":
        return Y_LIGANDS
    if category == "Z":
        return Z_LIGANDS
    return get_all_ligands()

def ligand_to_dict(ligand: Ligand) -> Dict:
    return {
        "name": ligand.name,
        "category": ligand.category,
        "smiles": ligand.smiles,
        "donor_atom": ligand.donor_atom,
        "description": ligand.description,
    }

