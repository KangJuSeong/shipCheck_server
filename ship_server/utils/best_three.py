import os


def best_three(arr):
    arr = arr.tolist()
    sorted_list = sorted(arr)
    first = sorted_list[-1]
    second = sorted_list[-2]
    third = sorted_list[-3]
    first_index = arr.index(first)
    second_index = arr.index(second)
    third_index = arr.index(third)
    label_path = os.listdir(os.getcwd().replace('\\', '/') + '/keras_model/class_history')
    label_name = os.getcwd().replace('\\', '/') + '/keras_model/class_history/' + label_path[0]
    f = open(label_name)
    label_list = []
    for line in f.readlines():
        label_list.append(line.replace('\n', ''))
    result = {'first': [], 'second': [], 'third': []}
    result['first'].append(label_list[first_index])
    result['first'].append(str(int(round(first, 2) * 100)) + '%')
    result['second'].append(label_list[second_index])
    result['second'].append(str(int(round(second, 2) * 100)) + '%')
    result['third'].append(label_list[third_index])
    result['third'].append(str(int(round(third, 2) * 100)) + '%')
    return result
