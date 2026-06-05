"""

main.py —— QD-LigandDesign 

"""

import os

import sys

import subprocess

from typing import List

# -------------------- ASCII logo --------------------

LOGO = r"""

==============================================================

  ____   ____    _     _   _      _     _           _         

 / __ \ |  _ \  | |   (_) | |    | |   (_)         | |        

| |  | || |_) | | |    _  | |    | |__  _  ___  __| | ___    

| |  | ||  _ <  | |   | | | |    | |'_ \| |/ __|/ _` |/ _ \   

| |__| || |_) | | |___| | | |____| | | | | | (__| (_| |  __/   

 \____/ |____/  |_____|_| |______|_| |_|_|\\___|\\__,_|\\___|   

==============================================================

=== QD-LigandDesign v1.0 ===

==============================================================

"""

# -------------------- utils --------------------

def print_section(title: str):

    print(f"\n>>> {title} <<<")

def choose(options: List[str]) -> int:

    """打印 1-based 菜单并返回 0-based index"""

    for idx, opt in enumerate(options, 1):

        print(f" {idx}. {opt}")

    while True:

        try:

            sel = int(input("Select (number): "))

            if 1 <= sel <= len(options):

                return sel - 1

        except ValueError:

            pass

        print("Invalid input, try again.")

# -------------------- menus --------------------

def surface_menu():

    print_section("Quantum-dot surface analysis")

    qd_file = input("Input quantum-dot CIF/XYZ/POSCAR file: ").strip()

    out = input("Output folder [qd_surface_out]: ").strip() or "qd_surface_out"

    cmd = [sys.executable, "surface_builder.py", qd_file, "--out", out]

    subprocess.run(cmd)

    input("Press Enter to continue...")

def ligand_menu():

    print_section("Ligand library viewer")

    category = input("Ligand category [X/Y/Z/ALL]: ").strip() or "ALL"

    out = input("Output folder [ligand_library_out]: ").strip() or "ligand_library_out"

    cmd = [sys.executable, "ligand_library_view.py", "--category", category, "--out", out]

    subprocess.run(cmd)

    input("Press Enter to continue...")

def design_menu():

    print_section("Ligand design and candidate generation")

    qd_file = input("Quantum-dot structure file: ").strip()

    category = input("Ligand category [X/Y/Z/ALL]: ").strip() or "ALL"

    coverage = input("Coverage ratio [0.5]: ").strip() or "0.5"

    out = input("Output folder [ligand_design_out]: ").strip() or "ligand_design_out"

    cmd = [

        sys.executable, "ligand_design.py",

        qd_file,

        "--category", category,

        "--coverage", coverage,

        "--out", out

    ]

    subprocess.run(cmd)

    input("Press Enter to continue...")

def mace_menu():

    print_section("MACE energy optimization")

    inp = input("Candidate structure file: ").strip()

    out = input("Output folder [mace_opt_out]: ").strip() or "mace_opt_out"

    steps = input("Optimization steps [200]: ").strip() or "200"

    cmd = [sys.executable, "mace_opt.py", inp, "--out", out, "--steps", steps]

    subprocess.run(cmd)

    input("Press Enter to continue...")

def result_menu():

    print_section("Final result analysis")

    energy_file = input("Energy result file: ").strip()

    out = input("Output folder [final_report_out]: ").strip() or "final_report_out"

    topn = input("Top-N candidates [5]: ").strip() or "5"

    cmd = [

        sys.executable, "result_analysis.py",

        energy_file,

        "--out", out,

        "--topn", topn

    ]

    subprocess.run(cmd)

    input("Press Enter to continue...")

# -------------------- main --------------------

def main():

    while True:

        os.system('cls' if os.name == 'nt' else 'clear')

        print(LOGO)

        main_opts = [

            "Analyze quantum-dot surface",

            "View ligand library",

            "Design and generate ligand candidates",

            "Run MACE energy optimization",

            "Analyze final results",

            "Exit"

        ]

        sel = choose(main_opts)

        if sel == 0:

            surface_menu()

        elif sel == 1:

            ligand_menu()

        elif sel == 2:

            design_menu()

        elif sel == 3:

            mace_menu()

        elif sel == 4:

            result_menu()

        else:

            print("Thank you for using QD-LigandDesign. Goodbye!")

            break

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print("\n\nAborted by user.")