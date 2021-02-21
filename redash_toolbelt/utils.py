import json


def save_dict_as_json_file(dict, filename, msg):
    with open(filename, 'w') as f:
        f.write(json.dumps(dict))
        print(msg)
