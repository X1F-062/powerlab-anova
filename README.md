# powerlab-anova: One-Way ANOVA Power Analysis

# Implementation status: Core CLI — draft ready · MCP (+15) — adapter written, not tested · AI agent (+10) — not implemented  

# Update this line to reflect the actual project status.

# 

# This project is an educational, clean-room reimplementation based on observing the behavior of the “F tests, one-way ANOVA (fixed effects, omnibus)” calculation in GPower 3.1.9.7. The GPower source code and decompilation output are not included in this repository. GPower.exe is not committed to the repository and is excluded via .gitignore.

# References

# Faul, F., Erdfelder, E., Lang, A.-G., \& Buchner, A. (2007). G\*Power 3: A flexible statistical power analysis program for the social, behavioral, and biomedical sciences. Behavior Research Methods, 39, 175–191.

# 

# Faul, F., Erdfelder, E., Buchner, A., \& Lang, A.-G. (2009). Statistical power analyses using G\*Power 3.1: Tests for correlation and regression analyses. Behavior Research Methods, 41, 1149–1160.

# 

# This software is not G\*Power and should not be presented as such.

# Version and Hash (To Be Completed)

# \- G\*Power version: 3.1.9.7 (Windows), available from the official website: psychologie.hhu.de

# \- GPower.exe SHA-256: TODO (PowerShell: Get-FileHash GPower.exe)

# \- Screenshot verifying the REA/Ghidra session: docs/rea\_check.png (TODO)

# \- 60-second demo video: TODO

# Installation and Usage

# pip install -r requirements.txt

# 

# ./gpower-clone --test anova-oneway --mode a-priori --f 0.25 --alpha 0.05 --power 0.95 --groups 3

# 

# ./gpower-clone --test anova-oneway --mode post-hoc --f 0.25 --alpha 0.05 --n\_total 100 --groups 3

# The output is a single-line JSON object containing: n\_total, n\_per\_group, actual\_power, critical, df1, df2, and ncp.

# 

# For invalid input, the program returns {"error": ...} and exits with code 2.

# 

# Effect size can be specified using --f, --eta2, or --means ... --sd ....

# 

# Important: Check the instructor's CONTRACT.md for the required parameter names and output fields. It was not available when this repository was written, so names such as --groups, df1/df2, and n\_per\_group are assumptions. Update src/powerlab/cli.py and api.py as needed to match the contract.

# Tests

# Run the test suite with:

# python -m pytest tests

# Alternatively, generate 960 scale-test vectors and then run the tests:

# python tests/gen\_scale\_vectors.py

# \- test\_oracle\_math.py: Independent mathematical validation using the Poisson-beta mixture formula and 100,000 Monte Carlo simulations.

# \- test\_properties.py: Monotonicity, minimality (including the strict rule for k), invalid inputs, and boundary conditions.

# \- test\_cli\_mcp\_parity.py: Verifies that the CLI and the shared layer called by MCP (api.solve) produce matching results.

# \- test\_differential.py: Critical test. Requires at least 90% exact matches for N against oracle/gpower\_vectors.csv (at least 30 vectors collected from the G\*Power GUI).

# \- Scale-test vectors were generated with SciPy, not G\*Power. Differences involving fractional N and rounding of k are documented in LEDGER.

# MCP Tool Schema (anova\_oneway)

# Input:

# \- mode: "a-priori" or "post-hoc"

# \- alpha

# \- groups (expected value: 3)

# \- f or eta2

# \- power (for a-priori mode)

# \- n\_total (for post-hoc mode)

# Output: The same JSON object returned by the CLI.

# 

# To run the MCP server:

# pip install mcp

# python -m src.powerlab.mcp\_server

