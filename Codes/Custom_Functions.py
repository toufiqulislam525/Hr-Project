# Dictionary format -- User(id,name,role)
#[{"id" : data[0],"name" : data[1], "role": data[2]}]
#Git something
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

# Dictionary format  -- attendence(id,check_in,check_out,day,week,month,year)
# [{"id" : data[0],"check_in" : data[1],"check_out" : data[2],"day" : data[3]......}]


def response_dictionary_3(data):
    l = []
    for i in data:
        dict = {}
        dict['id'] = i[0]
        dict['check_in'] = i[1]
        dict['check_out'] = i[2]
        dict['day'] = i[3]
        dict['week'] = i[4]
        dict['month'] = i[5]
        dict['year'] = i[6]
        l.append(dict)
    return l


def attendence_sheet_result_formatter(data):
    dict = {}
    for i in data:
        date = i[1]
        ids = i[2]
        dict[date] = ids
    return dict


# Converts string to datetime format
def time_filter(time):
    result = ""
    for char in time:
        if (char == '.'):
            return result
        result += char
    return result


def leave_request_formatter(data):
    l = []
    for i in data:
        dict = {}
        dict['id'] = i[0]
        dict['start_date'] = i[1]
        dict['end_date'] = i[2]
        if (i[3] == 0):
            dict['Approved'] = "Pending"
        elif i[3] > 0:
            dict['Approved'] = "Approved"
        elif i[3] < 0:
            dict['Approved'] = "Denied"
        l.append(dict)
    return l
