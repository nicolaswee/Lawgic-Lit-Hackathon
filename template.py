import json
import requests
import time
import urllib
import telegram


TOKEN = "BOT API KEY HERE"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
bot = telegram.Bot(token=TOKEN)

""" 
Download content from URL
Return string
"""
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

"""
Get string from json
"""
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

"""
Get messages sent to bot
"""
def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js
    
    
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)
    

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)
    
    
def respond_command(text, chat_id, username):
    if text == "/start":
        respond = "Hello " + username
        first_keyboard = telegram.KeyboardButton(text="Option 1")
        second_keyboard = telegram.KeyboardButton(text="Option 2")
        thrid_keyboard = telegram.KeyboardButton(text="Option 3")
        forth_keyboard = telegram.KeyboardButton(text="Option 4")
        custom_keyboard = [[ first_keyboard, second_keyboard, thrid_keyboard, forth_keyboard ]]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="This is round 1", reply_markup=reply_markup)
        # send_message(respond, chat_id)
    if text == "Option 4":
        respond = "Hello " + username
        first_keyboard = telegram.KeyboardButton(text="Option 5")
        second_keyboard = telegram.KeyboardButton(text="Option 6")
        thrid_keyboard = telegram.KeyboardButton(text="Option 7")
        forth_keyboard = telegram.KeyboardButton(text="Option 8")
        custom_keyboard = [[ first_keyboard, second_keyboard, thrid_keyboard, forth_keyboard ]]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="This is round 2", reply_markup=reply_markup)

    if text == "Option 5":
        respond = "Hello " + username
        first_keyboard = telegram.KeyboardButton(text="Option 9")
        second_keyboard = telegram.KeyboardButton(text="Option 10")
        thrid_keyboard = telegram.KeyboardButton(text="Option 11")
        forth_keyboard = telegram.KeyboardButton(text="Option 12")
        custom_keyboard = [[ first_keyboard, second_keyboard, thrid_keyboard, forth_keyboard ]]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="This is round 3", reply_markup=reply_markup)
    
def reply(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"].strip()
            chat_id = update["message"]["chat"]["id"]
            username = update["message"]["chat"]["username"]
            
            respond_command(text, chat_id, username)
        except Exception as e:
            print(e)
                        

def send_message(text, chat_id):
    text = urllib.request.pathname2url(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
    

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            reply(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()

