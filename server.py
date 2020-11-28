from flask_restful import Resource, Api, reqparse
from flask import Flask, Response
import urllib3
from time import time


urllib3.disable_warnings()

app = Flask(__name__)
api = Api(app)

start_str = '{} has created this chat.'
messages = {
    '1': [
        {
            'name': 'Vanya',
            'message': 'I dont nknow',
            'time': time()
        },
        {
            'name': 'Sasha',
            'message': 'Hello',
            'time': time() - 200
        },
        {
            'name': 'Dima',
            'message': 'Its code',
            'time': time() - 100
        },
        {
            'name': 'Tanya',
            'message': 'Welcome',
            'time': time() - 300
        },
        {
            'name': 'Vania',
            'message': 'Hello world!',
            'time': time() - 400
        },
        {
            'name': 'Dima',
            'message': 'Dima has created this chat.',
            'time': time() - 500
        }
    ]
}


class Read(Resource):
    def __init__(self):
        req = reqparse.RequestParser()
        req.add_argument('chat_id', type=str, required=True)
        req.add_argument('count', type=int, default=10)
        req.add_argument('last_id', type=int, default=0)

        args = req.parse_args()
        self.chat_id = args['chat_id']
        self.count = args['count']
        self.last_id = args['last_id']

    def len(self):
        return len(messages.get(self.chat_id, []))

    def get_messages(self):
        return messages.get(self.chat_id, [])[self.last_id:self.last_id+self.count]

    def get(self):
        r = Response()
        if self.len() == 0:
            r.status_code = 404
        elif self.len() <= self.last_id or self.count <= 0:
            r.status_code = 416
        else:
            return self.get_messages()

        return r


class Write(Resource):
    def __init__(self):
        req = reqparse.RequestParser()
        req.add_argument('chat_id', type=str, required=True)
        req.add_argument('message', type=str, required=True)
        req.add_argument('name', type=str, required=True)

        args = req.parse_args()
        self.chat_id = args['chat_id']
        self.message = args['message']
        self.name = args['name']

    def is_exists(self):
        return len(messages.get(self.chat_id, [])) > 0

    def write_message(self):
        if self.is_exists():
            messages[self.chat_id] = [{'name': self.name, 'message': self.message, 'time': time()}] + \
                                     messages[self.chat_id]
            return messages[self.chat_id][-1]

    def post(self):
        r = Response()
        if not self.is_exists():
            r.status_code = 404
        elif not self.message or not self.name:
            r.status_code = 406
        else:
            return self.write_message()

        return r


class CreateChat(Resource):
    def __init__(self):
        req = reqparse.RequestParser()
        req.add_argument('chat_id', type=str, required=True)
        req.add_argument('name', type=str, required=True)

        args = req.parse_args()
        self.chat_id = args['chat_id']
        self.name = args['name']

    def is_exists(self):
        return len(messages.get(self.chat_id, [])) > 0

    def create_chat(self):
        if not self.is_exists():
            messages[self.chat_id] = [{'name': self.name, 'message':  start_str.format(self.name), 'time': time()}]

    def put(self):
        r = Response()
        if not self.name or self.is_exists():
            r.status_code = 406
        else:
            self.create_chat()

        return r


class GetAllChats(Resource):
    def get(self):
        return messages


api.add_resource(Read, '/read')
api.add_resource(Write, '/write')
api.add_resource(CreateChat, '/create_chat')
api.add_resource(GetAllChats, '/get_all_chats')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
