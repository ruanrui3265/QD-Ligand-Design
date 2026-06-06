"""
result_analysis.py —— 最优配体结果分析模块
"""

import os
import csv
import json
import argparse

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def analyze_energy_table(energy_file, output_dir="final_report_out", topn=5):
    ensure_dir(output_dir)
    records = []
    with open(energy_file, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)

    if not records:
        raise RuntimeError("energy table is empty")

    records = sorted(records, key=lambda x: float(x["total_energy"]))
    top_records = records[:topn]
    best = top_records[0] if top_records else {}

    with open(os.path.join(output_dir, "top_candidates.csv"), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(top_records)

    with open(os.path.join(output_dir, "final_energy_rank.json"), "w") as f:
        json.dump({"best": best, "top_candidates": top_records}, f, indent=2)

    with open(os.path.join(output_dir, "best_ligand_report.txt"), "w") as f:
        f.write("QD-LigandDesign final report\n")
        f.write(f"Best candidate: {best}\n")
        f.write(f"Top-N selected: {topn}\n")

    return best

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Result analysis")
    parser.add_argument("energy_file")
    parser.add_argument("--out", default="final_report_out")
    parser.add_argument("--topn", default="5")
    args = parser.parse_args()
    best = analyze_energy_table(args.energy_file, args.out, int(args.topn))
    print(f"[result_analysis] best candidate: {best}")

