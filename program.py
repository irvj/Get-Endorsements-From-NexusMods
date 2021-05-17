from cred_lib import credentials
from datetime import datetime,timezone
import json
import os
import requests

# instead of using a credential file, uncomment the following variables and input your information
# game_name = 'XXXXX' # e.g. stardewvalley, skyrim // as displayed in NexusMods url
# mod_id = 'XXXXX' # get from mod page url
# api_key = 'XXXXX' # personal api key from NexusMods

game_name = credentials.cred_modname
mod_id = credentials.cred_modnum
api_key = credentials.cred_apikey

def main():
    mod_data = get_mod_from_api()
    current_date = get_date_and_serialize()
    endorsements = (mod_data['endorsement_count'])
    save_data = load_json_file()
    unique_id = increment_id(save_data)
    new_data = {'ID': unique_id, 'Date': current_date, 'Endorsements': endorsements}
    save_data['Data'].append(new_data)
    save_json_file(save_data)

def get_mod_from_api():
    mod_url = 'http://api.nexusmods.com/v1/games/{}/mods/{}.json'.format(game_name,mod_id)
    api_headers = {'apikey': api_key}
    response = requests.get(mod_url, headers=api_headers)
    data = response.json()
    return data

def get_date_and_serialize():
    now_utc = datetime.now(timezone.utc)
    data = now_utc.strftime('%Y-%m-%d-%X')
    return data

def increment_id(data):
    filename = os.path.abspath('data.json')
    if os.path.exists(filename):
        current_id = data['Data'][-1]['ID'] + 1
    else:
        current_id = 1
    return current_id

def load_json_file():
    data = {'Data':[]}
    filename = os.path.abspath('data.json')
    if os.path.exists(filename):
        with open(filename) as f:
            data = json.load(f)
    return data

def save_json_file(new_data):
    filename = os.path.abspath('data.json')
    with open(filename, 'w') as f:
        json.dump(new_data, f, indent=4)

if __name__ == '__main__':
    main()