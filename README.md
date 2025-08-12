# cas-to-chem-data
PubChem CAS Retrieval Tools  Python scripts to fetch chemical data from PubChem using CAS or names. Supports SMILES, InChI, IUPAC, CAS, and tox data. Batch processing via TXT files or args, with delays for large batches in tox script.
# README.md Content for pubchem-cas-retrieval-tools

```
# PubChem CAS Retrieval Tools

Python scripts to fetch chemical data from PubChem using CAS or names. Supports SMILES, InChI, IUPAC, CAS, and tox data. Batch processing via TXT files or args, with delays for large batches in tox script.

## Features
- Batch support for all scripts (TXT input or args).
- Logging, error handling.
- Tox script has built-in concurrency limits/delays.
- Optional MATLAB integration.

## Prerequisites
- Python 3.6+
- **Dependencies**: Install via pip:
- - `requests`: For synchronous HTTP API calls.
- `aiohttp`: For asynchronous HTTP in the tox script (enables batch fetching).
- `openpyxl`: For Excel output in the tox script.
- For MATLAB: Python in PATH.

## Scripts

### get_cas_batch.py - CAS from Names
Usage: `python get_cas_batch.py <name or names.txt>`
Output: Name\tCAS

### get_compound_info2_batch.py - IUPAC, SMILES from CAS
Usage: `python get_compound_info2_batch.py <CAS or cas.txt>`
Output: CAS\tIUPAC\tSMILES

### get_smiles_batch.py - SMILES from CAS
Usage: `python get_smiles_batch.py <CAS or cas.txt>`
Output: CAS\tSMILES

### get_iupac_name_batch.py - IUPAC from Names
Usage: `python get_iupac_name_batch.py <name or names.txt>`
Output: Name\tIUPAC

### get_smiles_InChI_IUPAC_batch.py - SMILES, InChI, IUPAC from CAS
Usage: `python get_smiles_InChI_IUPAC_batch.py <CAS or cas.txt>`
Output: CAS\tCanonicalSMILES\tIsomericSMILES\tInChI\tIUPACName

### get_toxinfo_by_cas7.py - Tox Data from CAS (Batch with Delays)
Usage: `python get_toxinfo_by_cas7.py <CAS1> <CAS2> ...` or interactive.
Batch TXT: Use MATLAB wrapper or shell loop (e.g., `xargs`).
Output: tox_data.json/excel

## MATLAB Integration
For batch processing (e.g., tox script) in MATLAB:
- Use matlab/batch_tox_matlab.m
  Call: `batch_tox_matlab({'754-12-1', '50-00-0'})`
- Alternative: Directly in MATLAB command window with `!python`, e.g., `!python get_toxinfo_by_cas7.py 754-12-1 50-00-0`

This uses MATLAB's system call to run Python scripts seamlessly.

## Examples
See examples/ folder. For cas_list.txt:
- Run batch scripts to generate *_output.txt.

## Limitations
- PubChem rate limits: Tox script limits to 5 concurrent (adjust semaphore if needed).
- Verify data; API may vary.

## Contributing
PRs welcome!

## License
Boost Software License 1.0
```
