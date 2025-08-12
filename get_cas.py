import sys
import requests

def get_cas_from_name(name):
    url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/xrefs/RN/JSON'
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Get only the first CAS number
            if 'InformationList' in data and 'Information' in data['InformationList']:
                cas_numbers = data['InformationList']['Information'][0].get('RN', [])
                if cas_numbers:
                    return cas_numbers[0]
    except:
        pass
    return 'Not found'

if __name__ == "__main__":
    print(get_cas_from_name(sys.argv[1]))
