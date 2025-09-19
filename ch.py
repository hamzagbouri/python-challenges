d = {'x':10, 'y': 20, 'z':10, 'a': 5}
def filter_by_value(dict, value):
    new_d = {}
    for k,v in dict.items():
        if v == value:
            new_d[k] = v
    return new_d

print(filter_by_value(d, 10))