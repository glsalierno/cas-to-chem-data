import sys
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def get_smiles_from_cas(cas, compound_name=None):
    base_url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug'
    
    try:
        # Get CID from CAS
        cid_url = f'{base_url}/compound/xref/RN/{cas}/cids/JSON'
        response = requests.get(cid_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'IdentifierList' not in data or 'CID' not in data['IdentifierList']:
            logging.error(f"No CID found for CAS {cas}")
            return 'Not found'
        
        cids = data['IdentifierList']['CID']
        cid = cids[0]  # Use first CID
        
        # Get SMILES
        smiles_url = f'{base_url}/compound/cid/{cid}/property/IsomericSMILES/TXT'
        response = requests.get(smiles_url, timeout=10)
        response.raise_for_status()
        smiles = response.text.strip()
        
        # Cross-check with name if provided
        if compound_name:
            name_url = f'{base_url}/compound/name/{compound_name}/property/IsomericSMILES/TXT'
            name_response = requests.get(name_url, timeout=10)
            if name_response.status_code == 200:
                name_smiles = name_response.text.strip()
                if name_smiles != smiles:
                    logging.info(f"Using name-based SMILES {name_smiles} over CAS-based {smiles} for {compound_name} (CAS {cas})")
                    return name_smiles  # Prefer name-based for consistency
        return smiles
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed for CAS {cas}: {e}")
        return 'Not found'
    except Exception as e:
        logging.error(f"Unexpected error for CAS {cas}: {e}")
        return 'Not found'

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_smiles.py <CAS> [compound_name]")
        sys.exit(1)
    
    cas = sys.argv[1]
    compound_name = sys.argv[2] if len(sys.argv) > 2 else None
    print(get_smiles_from_cas(cas, compound_name))
