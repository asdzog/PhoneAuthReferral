import random
import string


def generate_confirmation_code():
    return ''.join(random.choices(string.digits, k=4))


def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def imitate_code_sending(phone, code):
    print(f'Код подтверждения ({code}) отправлен на номер телефона {phone}')
