import json


def prepare_for_save(attr_dict_data):
    """
    This function is used to take output data and change authors format

    :param attr_dict_data: attribute data
    :return: changes in authors field
    """
    for d in attr_dict_data:
        d["authors"] = "|".join(d["authors"])
    return attr_dict_data


def toJSON(dictionary):
    """This function is used to convert list of dicts to json object"""
    return json.dumps(
        dictionary,
        default=lambda o: o.__dict__,
        sort_keys=True, indent=4)


def save_json_to_file(json_data, filename):
    """
    This function is used to save a JSON string to a file

    :param json_data: json data object
    :param filename: filename
    :return: None
    """
    with open(filename, 'w') as f:
        json.dump(json_data, f)
