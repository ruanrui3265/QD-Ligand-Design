# QD-LigandDesign v1.0

QD-LigandDesign v1.0 is a Python-based workflow for quantum-dot surface ligand design and screening.  
It provides an automated pipeline for:

- reading quantum-dot structures,
- identifying surface atoms,
- managing ligand libraries,
- generating ligand-binding candidates,
- optimizing candidate structures with a machine-learning force field,
- ranking the best ligand-binding schemes.

The software is designed for researchers working on quantum-dot surface chemistry, ligand engineering, interface regulation, and structure stability screening.

---

## Features

- **Surface analysis**  
  Automatically reads quantum-dot structure files and identifies surface atoms and candidate binding sites.

- **Ligand library management**  
  Organizes common ligand types into X-type, Y-type, and Z-type categories.

- **Candidate generation**  
  Generates multiple ligand-binding structures with adjustable surface coverage.

- **Machine-learning force-field optimization**  
  Uses a simplified MACE-style optimization workflow to relax candidate structures and estimate energies.

- **Final ranking and reporting**  
  Sorts all candidates by energy and outputs the most stable ligand-binding scheme.

---

## Workflow

The typical workflow is:

1. **Analyze quantum-dot surface**  
   Read the structure file and identify surface atoms.

2. **View ligand library**  
   List available ligand types and export ligand metadata.

3. **Design and generate ligand candidates**  
   Build candidate quantum-dot/ligand structures based on selected ligand type and coverage.

4. **Run MACE energy optimization**  
   Optimize each candidate structure and compute its energy.

5. **Analyze final results**  
   Rank candidate structures and generate the final report.

---

## Repository Structure

```text
QD-LigandDesign/
├── main.py
├── surface_builder.py
├── ligand_library.py
├── ligand_library_view.py
├── ligand_design.py
├── mace_opt.py
├── result_analysis.py
├── README.md
