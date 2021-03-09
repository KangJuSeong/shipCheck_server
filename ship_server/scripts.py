import os


def script():
    os.system('python manage.py makemigrations')
    os.system('python manage.py migrate')
    os.system('python manage.py runserver')


if __name__ == '__main__':
    script()