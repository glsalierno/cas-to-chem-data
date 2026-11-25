# cas-to-chem-data

Python scripts that fetch chemical identifiers and toxicology fields from [PubChem](https://pubchem.ncbi.nlm.nih.gov/) using CAS numbers or compound names. Supported lookups include SMILES, InChI, IUPAC names, CAS, and PubChem tox data.

This repository keeps the **overview and license on `main`**, and keeps the working scripts on dedicated branches. Script branches are not merged into `main`.

## Branches

- **`main`** — This overview, prerequisites, and the Boost Software License 1.0.
- **`single_PUG_pull`** — Single-input PubChem PUG REST helpers (one CAS or name at a time):
  - `get_cas.py` — CAS number from a compound name
  - `get_compound_info2.py` — CAS, IUPAC name, and SMILES from a compound name
  - `get_iupac_name.py` — IUPAC name from a compound name, with optional CAS cross-check
  - `get_smiles.py` — Isomeric SMILES from a CAS number, with optional name cross-check
  - `get_smiles_InChI_IUPAC.py` — Canonical SMILES, isomeric SMILES, InChI, and IUPAC name from a CAS number
- **`GHStox_PUG_pull`** — Toxicological data retrieval (`get_toxinfo_by_cas7a.py`). Accepts one or more CAS numbers on the command line, or prompts interactively. Limits concurrency to five requests, applies retries and delays, and writes `tox_data.json` and `tox_data.xlsx`.

A `batch_PUG_pull` branch previously existed but was identical to `main` and has been removed. Batch-style `*_batch.py` scripts mentioned in older notes were never pushed to this repository.

To use a script, check out its branch:

```bash
git clone https://github.com/glsalierno/cas-to-chem-data.git
cd cas-to-chem-data
git checkout single_PUG_pull   # or GHStox_PUG_pull
```

## Prerequisites

- Python 3.6+
- `requests` — HTTP calls in the `single_PUG_pull` scripts
- `aiohttp` and `openpyxl` — async fetching and Excel output in the tox script
- For MATLAB, Python must be on `PATH` (the tox script can be called with `!python ...`)

```bash
pip install requests aiohttp openpyxl
```

## Examples

```bash
# from single_PUG_pull
python get_cas.py benzene
python get_smiles.py 50-00-0
python get_smiles_InChI_IUPAC.py 754-12-1

# from GHStox_PUG_pull
python get_toxinfo_by_cas7a.py 754-12-1 50-00-0
```

## Limitations

- PubChem enforces rate limits. The tox script caps concurrency at five requests (adjust the semaphore if needed).
- Always verify returned data; PubChem records can change or be incomplete.

## License

Boost Software License 1.0. See [LICENSE](LICENSE).
