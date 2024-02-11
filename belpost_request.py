import pprint
import requests

URL = "https://api.belpost.by/api/v1/tracking"
TRACKER = 'BV280488510BY'


def get_data(tracker):
    'Get json data file from Belpost'

    payload = {
        'number': tracker,
        'show_order': True
    }

    data_list = []

    response = requests.post(URL, json=payload)

    if response.status_code == 404:
        return 'Uncorrect code format'

    json_data = response.json()
    data = json_data.get('data', [])

    first_tracking_info = data[0]
    steps = first_tracking_info.get('steps', [])

    if not steps:
        return 'No infotmation'

    reversed_steps = steps[::-1]
    for i in reversed_steps:
        data_list.append({
            'place_index': i['place_index'],
            'place': i['place'],
            'created_at': i['created_at'],
            'event': i['event']
        })
    return data_list


def main():
    pprint.pprint(get_data(TRACKER))


if __name__ == "__main__":
    main()
