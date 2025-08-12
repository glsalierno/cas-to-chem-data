import sys
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def get_compound_info(compound_name):
    base_url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug'
    try:
        # Get CID by name
        cid_url = f'{base_url}/compound/name/{compound_name}/cids/JSON'
        response = requests.get(cid_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        cid = data['IdentifierList']['CID'][0]
        
        # Get CAS from synonyms
        synonyms_url = f'{base_url}/compound/cid/{cid}/synonyms/JSON'
        response = requests.get(synonyms_url, timeout=10)
        response.raise_for_status()
        synonyms = response.json()['InformationList']['Information'][0]['Synonym']
        cas = next((s for s in synonyms if s.replace('-', '').isdigit()), 'Not found')
        
        # Get IUPAC
        iupac_url = f'{base_url}/compound/cid/{cid}/property/IUPACName/TXT'
        iupac = requests.get(iupac_url, timeout=10).text.strip()
        
        # Get SMILES
        smiles_url = f'{base_url}/compound/cid/{cid}/property/IsomericSMILES/TXT'
        smiles = requests.get(smiles_url, timeout=10).text.strip()
        
        return f"{cas}\t{iupac}\t{smiles}"
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed for {compound_name}: {e}")
        return "Not found\tNot found\tNot found"
    except Exception as e:
        logging.error(f"Unexpected error for {compound_name}: {e}")
        return "Not found\tNot found\tNot found"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_compound_info2.py <compound_name>")
        sys.exit(1)
    print(get_compound_info(sys.argv[1]))
