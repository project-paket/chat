import requests
import config
from time import sleep
from datetime import datetime
import keyboard


def input_mod(message):
    string = ''
    while not string:
        string = input(message)
        if not string:
            print('Input is empty, please, try again')

    return string


class Server:
    @staticmethod
    def read(chat_id, count=10, last_id=0):
        res = requests.get(f'{config.server}/read', params={'chat_id': chat_id, 'count': count, 'last_id': last_id})
        if res.status_code == 200:
            return res.json()

    @staticmethod
    def write(chat_id, message, name):
        res = requests.post(f'{config.server}/write', params={'chat_id': chat_id, 'message': message, 'name': name})
        if res.status_code == 200:
            return res.json()

    @staticmethod
    def create_chat(chat_id, name):
        requests.put(f'{config.server}/create_chat', params={'chat_id': chat_id, 'name': name})


class Client:
    def __init__(self):
        self.name = None
        self.chat_id = None
        self.last_message_time = 0
        self.need_wait = False

    def enjoy_to_chat(self):
        Server.create_chat(self.chat_id, self.name)

    def write_message(self):
        self.need_wait = True
        message = input_mod('Enter a message: ')
        Server.write(self.chat_id, message, self.name)
        self.need_wait = False

    def main(self):
        self.name = input_mod('Enter a name: ')
        print(f'Hi {self.name}!')

        self.chat_id = input_mod('Enter a chat id: ')
        self.enjoy_to_chat()
        print(f'You successful enjoy to {self.chat_id}')

        output_for_me = '{:>' + str(config.width_chat) + '}'

        keyboard.add_hotkey('Space', self.write_message)

        run = True
        while run:
            last_messages = Server.read(self.chat_id)
            if last_messages:
                for message in last_messages[::-1]:
                    if message['time'] > self.last_message_time:
                        top = '{} at {}'.format(message['name'], datetime.fromtimestamp(message['time']).strftime(
                            '%Y-%m-%d %H:%M:%S'))
                        if message['name'] == self.name:
                            print(output_for_me.format(top))
                            print(output_for_me.format(message['message']))
                        else:
                            print(top)
                            print(message['message'])

                        self.last_message_time = message['time']

            while self.need_wait:
                pass

            sleep(0.2)


if __name__ == '__main__':
    client = Client()
    client.main()
