import sys
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def get_iupac_name(name, cas=None):
    base_url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug'
    
    try:
        # Try fetching IUPAC name by compound name
        url = f'{base_url}/compound/name/{name}/property/IUPACName/TXT'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        iupac = response.text.strip()
        
        # If CAS is provided, cross-check with CAS-based lookup
        if cas:
            cid_url = f'{base_url}/compound/xref/RN/{cas}/cids/JSON'
            cid_response = requests.get(cid_url, timeout=10)
            cid_response.raise_for_status()
            data = cid_response.json()
            
            if 'IdentifierList' in data and 'CID' in data['IdentifierList']:
                cid = data['IdentifierList']['CID'][0]
                cas_url = f'{base_url}/compound/cid/{cid}/property/IUPACName/TXT'
                cas_response = requests.get(cas_url, timeout=10)
                if cas_response.status_code == 200:
                    cas_iupac = cas_response.text.strip()
                    if cas_iupac != iupac:
                        logging.info(f"Name IUPAC ({iupac}) differs from CAS IUPAC ({cas_iupac}) for {name}")
                        return iupac  # Prefer name-based IUPAC for specificity
        return iupac
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed for {name}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error for {name}: {e}")
    return 'Not found'

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_iupac_name.py <compound_name> [CAS]")
        sys.exit(1)
    
    name = sys.argv[1]
    cas = sys.argv[2] if len(sys.argv) > 2 else None
    print(get_iupac_name(name, cas))
