import json


def mix(src, dst):
    for k, v in src.items():
        if hasattr(dst, '__getitem__'):
            if dst.get(k) and type(v) == dict:
                mix(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and type(v) == dict:
            mix(v, getattr(dst, k))
        else:
            setattr(dst, k, v)

black_list = ["flag","environ"]

def check(data):
    str=json.dumps(data)  # 字典转换为字符串
    for i in black_list:
        if i in str:
            return True
    return False