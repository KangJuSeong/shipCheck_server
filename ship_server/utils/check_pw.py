def repeat_search(password):
    repeat = 0
    print(len(password))
    for i in range(len(password)-1):
        if password[i] == password[i+1]:
            repeat = repeat + 1
            if repeat == 2:
                return 1
        else:
            repeat = 0
    return 0


def solution(s):
    return ''.join(sorted(s, reverse=True))


def check_pw(pw):
    if not pw.isalnum():
        if repeat_search(pw):
            print("3번연속 중복된 단어가 있습니다.")
            return {'message': "Repeat the same character 3 times",
                    'status': '2'}
        else:
            # 비밀번호 검사 시 특수문자가 무조건 들어가므로 오름차순의 의미가 있는가?
            if solution(pw) == pw or sorted(pw) == pw:
                print("순서대로 입력됐습니다.")
                return {'message': "Password with sequence",
                        'status': '3'}
            else:
                print("비밀번호 체크 완료")
                return {'message': "Success check password",
                        'status': '4'}
    else:
        print('특수문자가 없습니다.')
        return {'message': "Not special character in password",
                'status': '1'}