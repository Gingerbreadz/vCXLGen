# vCXLGen

vCXLGen is a cache coherence bridge generator and verifier for CXL.mem

## Software Dependencies

- Linux distribution (e.g. Ubuntu 20.04)
- Graphviz 2.43.0
- Python 3.8 or higher
  - antlr3 3.4
  - colorama 0.4.3
  - graphviz 0.16
  - networkx 2.5.1
  - psutil 5.8.0
  - tabulate 0.8.9
- CMurphi 5.4.9.1

## Quick setup

Set up the complete environment with the `nix` package manager

```
nix develop
```

## Antlr3 setup

To install antlr3, clone it, move to the antrl3 python3 directory, then run the install script.

```
git clone https://github.com/Errare-humanum-est/antlr3 antlr3
cd antlr3/runtime/Python3
sudo python3 setup.py install
```

## CMurphi setup

To install CMuprhi, run from the parent directory:

```
git clone https://github.com/Errare-humanum-est/CMurphi.git CMuprhi
cd CMurphi/src && make
```

## Datasets

Stable state protocols, used as inputs by vCXLGen to generate the bridged cache coherence protocol, are provided in the *Protocols/MOESI Directory/ord* net directory.
A set of litmus tests to verify the correctness of the protocols is provided in the MurphiLitmusTests directory.

## Experiment workflow
In the top level directory run:

```
python3 eval.py       # Generate and run the litmus tests
```

This will generate the bridged coherence protocol state machines and litmus tests of protocols presented in the paper, which
will be verified using the Murphi model checker. Warnings can be ignored when using the provided protocols, but can help to debug problems when using new atomic protocols as inputs to vCXLGen.
The generated files can be found in the directory: *Protocols/MOESI Directory/ord net/*

## Model Checker Setup

To compile the generated litmus tests **update the variable 'murphi_compiler_path'** in the file ParallelCompiler.py to your local Murphi path. Now compile the model checker files:

```
python3 ParallelCompiler.py
```

## Evaluation and Expected Results

To verify the correctness of the generated bridged cache coherence protocols, the Murphi model checker is used.
Run the generated model checking executables:

```
python3 ParallelChecker.py
```

The runtime of all litmus tests depends on the amount of RAM and number of CPUs available. The ParallelChecker.py will automatically run all litmus tests and generate a report file **'Test_Result.txt'** in the TestScripts directory.

If the ParallelChecker reports that no Murphi test files were found, change the access permission of the executables to ’+x’.

## Understanding the Test Report

In the report file *'Test_Result.txt'* the litmus tests failing are listed. None of the litmus tests should fail under normal operation. The types of failure that are listed can be as follows:

- Not served yet: Due to some error the litmus test was not served

- Out of memory: The verification test ran out of available RAM.

- File not found: No executable was found.

- Fail: The litmus test failed because of an unknown error (e.g. executable could not be run)

- Litmus test fail: A litmus test has failed

- Deadlock: A deadlock in the protocol was found

- Invariant: An invariant specified was violated
