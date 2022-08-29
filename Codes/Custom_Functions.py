def response_dictionary(data):
    l = []
    for i in data:
        dict = {}
        dict['id'] = i[0]
        dict['name'] = i[1]
        dict['role'] = i[2]
        l.append(dict)
    return l


def response_dictionary_2(data):
    l = []
    for i in data:
        dict = {}
        dict['id'] = i[0]
        dict['time'] = i[1]
        l.append(dict)
    return l
