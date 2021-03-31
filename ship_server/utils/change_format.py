def change_datetime(data):
    if str(type(data)) == "<class 'rest_framework.utils.serializer_helpers.ReturnDict'>":
        date_time = data['regit_date'].replace('T', '일 ').replace('-', '년', 1).replace('-', '월') \
            .replace(':', '시', 1).replace(':', '분')
        data['regit_date'] = date_time[:date_time.find('분') + 1]
        return data
    else:
        for i in data:
            date_time = i['regit_date'].replace('T', '일 ').replace('-', '년', 1).replace('-', '월') \
                .replace(':', '시', 1).replace(':', '분')
            i['regit_date'] = date_time[:date_time.find('분') + 1]
        return data


def change_datetime_notice(data):
    if str(type(data)) == "<class 'rest_framework.utils.serializer_helpers.ReturnDict'>":
        date_time = data['date'].replace('T', '일 ').replace('-', '년', 1).replace('-', '월') \
            .replace(':', '시', 1).replace(':', '분')
        data['date'] = date_time[:date_time.find('분') + 1]
        return data
    else:
        for i in data:
            date_time = i['date'].replace('T', '일 ').replace('-', '년', 1).replace('-', '월') \
                .replace(':', '시', 1).replace(':', '분')
            i['date'] = date_time[:date_time.find('분') + 1]
        return data


def change_unit(data):
    if data['unit'] == '사령부' or data['unit'] == '직할대':
        return data
    data['unit'] = data['unit'][:2] + '여단 ' + data['unit'][3] + '대대'
    return data

