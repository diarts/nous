class RegisterAccData:
    correct_acc = {
        'email': 'test@mail.ru',
        'password': 'test password',
        'username': 'test user',
        'phone': 9851117141,
        'country': 7,
    }
    wrong_mail = {
        'email': 'not mail',
        'password': 'test password',
        'username': 'test user',
        'phone': 9851117141,
        'country': 7,
    }
    wrong_phone = {
        'email': 'test@mail.ru',
        'password': 'test password',
        'username': 'test user',
        'phone': '9851117141',
        'country': 7,
    }
    wrong_country = {
        'email': 'test@mail.ru',
        'password': 'test password',
        'username': 'test user',
        'phone': 9851117141,
        'country': 10,
    }
    missed_password = {
        'email': 'test@mail.ru',
        'username': 'test user',
        'phone': 9851117141,
        'country': 7,
    }
    missed_email_and_phone = {
        'username': 'test user',
        'password': 'test password',
    }
