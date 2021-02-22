import json


def save_dict_as_json_file(dict, filename, msg):
    with open(filename, 'w') as f:
        f.write(json.dumps(dict))
        print(msg)


def copy_value_if_key_exists(key, from_, to_):
    if key in from_:
        to_[key] = from_[key]