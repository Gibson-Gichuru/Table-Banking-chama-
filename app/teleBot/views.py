
from flask import request, current_app

from . import bot

@bot.route("/telebot")
def bot_callback():

    return "Bot call back url"