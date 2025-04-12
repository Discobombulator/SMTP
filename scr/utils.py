import sys

def read_config():
    try:
        with open('./config.txt') as f:
            sender = f.readline().strip().split(' ')[1]
            password = f.readline().strip().split(' ')[1]
            recipients = f.readline().strip().split(' ')[1:]
            subject = f.readline().strip().partition(' ')[2]
            attachments = f.readline().strip().split(' ')[1:]
            return sender, password, recipients, subject, attachments
    except Exception:
        print('Ошибка чтения конфигурации. Проверьте config.txt и README.md.')
        sys.exit()

def read_message_text():
    with open('./message.txt', 'r', encoding='utf-8') as f:
        return f.read()
