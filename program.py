from cred_lib import credentials
from datetime import datetime, timezone
import json
import os
import requests

# Add your mod info and NexusMods api key to cred_lib.py (see included sample_cred_lib.py)
game_name = credentials.cred_modname
mod_id = credentials.cred_modnum
api_key = credentials.cred_apikey


def main():
    mod_data = get_mod_from_api()
    current_date = get_date_and_serialize()
    endorsements = (mod_data['endorsement_count'])
    save_data = load_json_file()
    unique_id = increment_id(save_data)
    new_data = {'ID': unique_id, 'Date': current_date,
                'Endorsements': endorsements}
    save_data['Data'].append(new_data)
    save_json_file(save_data)


def get_mod_from_api():
    mod_url = 'http://api.nexusmods.com/v1/games/{}/mods/{}.json'.format(
        game_name, mod_id)
    api_headers = {'apikey': api_key}
    response = requests.get(mod_url, headers=api_headers)
    return response.json()


def get_date_and_serialize():
    now_utc = datetime.now(timezone.utc)
    return now_utc.strftime('%Y-%m-%d-%X')


def increment_id(data):
    filename = os.path.abspath('data.json')
    if os.path.exists(filename):
        return data['Data'][-1]['ID'] + 1
    else:
        return 1


def load_json_file():
    data = {'Data': []}
    filename = os.path.abspath('data.json')
    if os.path.exists(filename):
        with open(filename) as f:
            return json.load(f)


def save_json_file(new_data):
    filename = os.path.abspath('data.json')
    with open(filename, 'w') as f:
        json.dump(new_data, f, indent=4)


if __name__ == '__main__':
    main()
