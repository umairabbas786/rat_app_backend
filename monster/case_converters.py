import re


def snake_to_pascal(v):
    return v.title().replace('_', '')


def camel_to_snake(v):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', v).lower()


def camel_to_pascal(v):
    return v if len(v) == 0 else f'{v[0].upper()()}{v[1:]}'


def snake_to_camel(v):
    if '_' not in v:
        return v
    chunks = v.split('_')
    return f'{chunks[0]}{snake_to_pascal("_".join(chunks[1:]))}'


def pascal_to_camel(v):
    return v if len(v) == 0 else f'{v[0].lower()}{v[1:]}'


def pascal_to_snake(v):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', v).lower()
