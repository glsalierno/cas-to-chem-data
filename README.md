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

This repo uses branches to organize code:
- **main**: Overview, prerequisites, examples, and license.
- **single**: Single-input scripts (basic versions for one CAS/name at a time).
- **batch**: Batch-enabled scripts (support TXT files with multiple inputs).
- **tox**: Toxicological data scripts (with batch support and API rate delays).

## Prerequisites
- Python 3.6+
- **Dependencies**: Install via pip:
- - `requests`: For synchronous HTTP API calls.
- `aiohttp`: For asynchronous HTTP in the tox script (enables batch fetching).
- `openpyxl`: For Excel output in the tox script.
- For MATLAB: Python in PATH.

## Limitations
- PubChem rate limits: Tox script limits to 5 concurrent (adjust semaphore if needed).
- Verify data; API may vary.

## Contributing
PRs welcome!

## License
Boost Software License 1.0
```
