def response_dictionary(data):
    l = []
    for i in data:
        dict = {}
        dict['id'] = i[0]
        dict['name'] = i[1]
        dict['role'] = i[2]
        l.append(dict)
    return l
