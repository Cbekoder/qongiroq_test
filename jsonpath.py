def get(data, path):
    keys = path.split('/')
    current = data
    for key in keys:
        if key == "":
            continue
        if key.isdigit():
            key = int(key)
        current = current[key]
    return current