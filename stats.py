import os
import re
import sys

if len(sys.argv) < 2:
    print("Usage: python3 stats.py <directory_path>")
    sys.exit(1)

directory = sys.argv[1]

file_ranking = []
err_files = []

for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith(".m"):
            filepath = os.path.join(root, file.replace(".m", "_results.txt"))
            test_name = file.removeprefix("MU_MESIxMESIxMESI_")
            test_setup = re.search(r"(cache[^/]*)+", root).group(0)
            try:

                with open(filepath, 'r') as f:
                    contents = f.read()
                    
                    if "No error found." in contents:

                        state_size = int(re.search(r"The size of each state is \d+ bits \(rounded up to (\d+) bytes\)", contents).group(1)) / 1000000000.0
                        states = int(re.search(r"(\d+) states, \d+ rules fired in (\d+(\.\d+)?)s", contents).group(1))
                         
                        file_ranking.append((state_size * states, test_name, test_setup))
                    else:
                        err_files.append((test_name, test_setup))
            except Exception as e:
                print(f"Error opening file {filepath}: {e}")


print("Memory,TestName,TestSetup")
for (size, name, setup) in sorted(file_ranking):
    print(f"{size},{name},{setup}")

print()

for (name,setup) in err_files:
    print(f"OUT_OF_MEMORY,{name},{setup}")