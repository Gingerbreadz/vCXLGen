import subprocess
import os
import sys

def count_model_files(path: str) -> int:
    count = 0
    for _, _, files in os.walk(path):
        count += sum(1 for f in files if f.endswith(".m"))
    return count

def count_exe_files(path: str) -> int:
    count = 0
    for _, _, files in os.walk(path):
        count += sum(1 for f in files if f != "Makefile" and not "." in f)
    return count

def eval_model(genfile: str, proto: str, target_count: int = 216):
        litmus_path = os.path.join(
            "Protocols", "MOESI_Directory", "RF_Dir", "ord_net", "FullSystem_NoCE", 
            proto.replace("RCC", "RCCHetero").replace("CXL", "CXL2"),
            "Litmus_Tests"
        )
        out_file = os.path.join("..", "output", "litmus", f"{proto}.txt")

        if count_model_files(litmus_path) < target_count:
            subprocess.run(("python3", genfile))
        else:
            print(f"Skipping litmus test generation for {proto}.")

        if count_exe_files(litmus_path) < target_count:
            subprocess.run(("python3", "ParallelCompiler.py", litmus_path))
        else:
            print(f"Skipping litmus test compilation for {proto}.")

        if not os.path.exists(out_file):
            subprocess.run(("python3", "ParallelChecker.py", litmus_path, out_file))
        else:
            print(f"Skipping litmus test checking for {proto}.")

if __name__ == "__main__":
    tests = [
        ("GenMESIxMESIxMESI.py", "MESIxMESIxMESI"),
        ("GenMESIxCXLxMESI.py", "MESIxCXLxMESI"),
        ("GenMESIxCXLxRCC.py", "MESIxCXLxRCC"),
        ("GenRCCxCXLxRCC.py", "RCCxCXLxRCC"),
    ]

    args = sys.argv[1:]
    success = False

    for gen, proto in tests:
        if ("all" in args) or any(a in proto for a in args):
            print(f"Evaluating {proto}...")
            success = True
            eval_model(gen, proto)

    if not success:
        print("ERROR: No configuration specified. Use 'all' or specify which configurations to evaluate:")
        for _, proto in tests:
            print(f" - {proto}")
        sys.exit(1)
