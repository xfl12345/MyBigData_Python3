import json


def json2object(target_object: object, json_content):
    json_in_dict = json_content
    if isinstance(json_content, str):
        json_in_dict = json.loads(json_content)
    elif not isinstance(json_content, dict):
        raise TypeError("Unexcepted args input.")
    dict2object(target_object=target_object, source_dict=json_in_dict)


def dict2object(target_object: object, source_dict: dict):
    if not isinstance(source_dict, dict):
        raise TypeError("Unexcepted args input.")

    for key in source_dict.keys():
        if hasattr(target_object, key):
            # TODO 判断是否是一样的数据类型 、递归赋值
            # target_object.__dict__[key] = source_dict[key]
            val = source_dict[key]
            if isinstance(val, dict):
                dict2object(getattr(target_object, key), val)
            else:
                setattr(target_object, key, val)
