def bestThree(arr):
    arr = arr.tolist()
    sorted_list = sorted(arr)
    first = sorted_list[-1]
    second = sorted_list[-2]
    third = sorted_list[-3]
    print(third)
    first_i = arr.index(first)
    second_i = arr.index(second)
    third_i = arr.index(third)
    f = open('/workspace/shipCheck_server/ship_server/keras_model/labels.txt')
    data = {'first': [], 'second': [], 'third': []}
    cnt = 0
    while True:
        if cnt == 3:
            break
        line = f.readline()
        if not line:
            break
        index = line.find(' ')
        title = line[index+1:]
        number = int(line[:index])
        if number == first_i:
            data['first'].append(title.replace('\n', ''))
            data['first'].append(format(first * 100, '.2f') + '%')
            cnt = cnt + 1
        if number == second_i:
            data['second'].append(title.replace('\n', ''))
            data['second'].append(format(second * 100, '.2f') + '%')
            cnt = cnt + 1
        if number == third_i:
            data['third'].append(title.replace('\n', ''))
            data['third'].append(format(third * 100, '.2f') + '%')
            cnt = cnt + 1
    f.close()
    result = []
    result.append(data['first'])
    result.append(data['second'])
    result.append(data['third'])
    print(result)
    return result