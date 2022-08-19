def get_php_val_of_python_val(v):
    if isinstance(v, type(None)):
        return 'null'
    elif type(v) is str:
        return f'"{v}"'
    elif type(v) is bool:
        return 'true' if v else 'false'
    else:
        return f'{v}'
