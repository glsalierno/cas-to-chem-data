import sys
import requests
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def get_compound_info(cas_number, compound_name=None):
    """Fetches SMILES, IsomericSMILES, InChI, and IUPAC name from PubChem for a CAS number using PUG REST API."""
    base_url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug'
    
    try:
        # Step 1: Get CID from CAS number
        cid_url = f'{base_url}/compound/xref/RN/{cas_number}/cids/JSON'
        response = requests.get(cid_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'IdentifierList' not in data or 'CID' not in data['IdentifierList']:
            logging.error(f"No CID found for CAS {cas_number}")
            return {'Error': f'CAS number {cas_number} not found in PubChem'}
        
        cid = data['IdentifierList']['CID'][0]
        
        # Step 2: Get properties: CanonicalSMILES, IsomericSMILES, InChI, IUPACName
        properties_url = f'{base_url}/compound/cid/{cid}/property/CanonicalSMILES,IsomericSMILES,InChI,IUPACName/JSON'
        response = requests.get(properties_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'PropertyTable' not in data or 'Properties' not in data['PropertyTable']:
            logging.error(f"Failed to retrieve properties for CID {cid}")
            return {'Error': f'Failed to retrieve properties for CID {cid}'}
        
        properties = data['PropertyTable']['Properties'][0]
        
        # Cross-check with name if provided
        if compound_name:
            name_cid_url = f'{base_url}/compound/name/{compound_name}/cids/JSON'
            name_response = requests.get(name_cid_url, timeout=10)
            if name_response.status_code == 200:
                name_data = name_response.json()
                if 'IdentifierList' in name_data and 'CID' in name_data['IdentifierList']:
                    name_cid = name_data['IdentifierList']['CID'][0]
                    if name_cid != cid:
                        logging.info(f"CID mismatch: CAS-based {cid}, name-based {name_cid}. Using name-based.")
                        cid = name_cid
                    # Refetch properties with name-based CID
                    properties_url = f'{base_url}/compound/cid/{cid}/property/CanonicalSMILES,IsomericSMILES,InChI,IUPACName/JSON'
                    response = requests.get(properties_url, timeout=10)
                    response.raise_for_status()
                    data = response.json()
                    properties = data['PropertyTable']['Properties'][0]
        
        return properties
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error: {str(e)}")
        return {'Error': f'Network error: {str(e)}'}
    except json.JSONDecodeError:
        logging.error("Failed to parse JSON response")
        return {'Error': 'Failed to parse JSON response'}
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return {'Error': f'Unexpected error: {str(e)}'}

def format_property(prop_name, prop_value):
    """Formats the property value with its name."""
    return f"{prop_name}: {prop_value}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cas_number = sys.argv[1]
        compound_name = sys.argv[2] if len(sys.argv) > 2 else None
        properties = get_compound_info(cas_number, compound_name)
        if 'Error' not in properties:
            # Map the actual keys to desired labels
            prop_map = {
                'CanonicalSMILES': properties.get('ConnectivitySMILES', 'Not available'),
                'IsomericSMILES': properties.get('SMILES', 'Not available'),
                'InChI': properties.get('InChI', 'Not available'),
                'IUPACName': properties.get('IUPACName', 'Not available')
            }
            for label, value in prop_map.items():
                if value != 'Not available':
                    print(format_property(label, value))
        else:
            print(f"Error: {properties['Error']}")
    else:
        print("Please provide a CAS number as an argument. Optional: compound name.")
