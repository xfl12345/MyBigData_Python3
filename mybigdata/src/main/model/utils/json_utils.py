import json


def json2class(target_object: object, json_content):
    json_in_dict = {}
    if isinstance(json_content, str):
        json_in_dict = json.loads(json_content)
    elif not isinstance(json_content, dict):
        raise TypeError("Unexcepted args input.")
    dict2class(target_object=target_object, source_dict=json_in_dict)


def dict2class(target_object: object, source_dict: dict):
    if not isinstance(source_dict, dict):
        raise TypeError("Unexcepted args input.")

    for key in source_dict.keys():
        if key in target_object.__class__.__dict__.keys():
            # TODO 判断是否是一样的数据类型 、递归赋值
            target_object.__setattr__(key, source_dict[key])
