# Dictionary format -- User(id,name,role)
#[{"id" : data[0],"name" : data[1], "role": data[2]}]
def response_dictionary(data):
    l = []
    for i in data:
        dict = {}
        dict['id'] = i[0]
        dict['name'] = i[1]
        dict['role'] = i[2]
        l.append(dict)
    return l


# Dictionary format -- check_in_out(id,time)
# [{"id" : data[0],"time" : data[1]}]
def response_dictionary_2(data):
    l = []
    for i in data:
        dict = {}
        dict['id'] = i[0]
        dict['time'] = i[1]
        l.append(dict)
    return l
