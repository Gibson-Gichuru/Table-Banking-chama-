import requests
from flask import current_app

bot_urls = {"send_message":f"https://{current_app.config['TELEBOT_TOKEN']}/sendMessage"}

def parse_message(message):

    pass


def send_message(message):

    pass

