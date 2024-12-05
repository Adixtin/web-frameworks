from flask import Flask

app = Flask(__name__)

def ping():
    return 'pong'