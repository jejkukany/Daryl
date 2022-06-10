# ─── IMPORTS ────────────────────────────────────────────────────────────────────

#Telegram API
import telegram
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from key import *
#Command APIs
from GoogleNews import GoogleNews
import pyrebase
import time
import random

# ─── API LOGINS AND CONFIG ──────────────────────────────────────────────────────

#Telegram API login
updater = Updater(ttoken, use_context=True)
dispatcher = updater.dispatcher

#Pyrebase API login/config
firebase=pyrebase.initialize_app(firebaseconfig)
db=firebase.database()

#GoogleNews API config
googlenews = GoogleNews(lang='en', period='2d', encode='utf-8')

# ─── COMMANDS ───────────────────────────────────────────────────────────────────

#
# ──────────────────────────────────────────────────────────────── FUNCTIONALITY ─────
#

def ecostart(update: Update, context: CallbackContext):
    data = {'money' : 0}
    try:
        balance = db.child(update.message.from_user.username).get()
        db.child(update.message.text.split(' ')[1]).update(data)
    except:
        db.child(update.message.from_user.username).update(data)

#
# ────────────────────────────────────────────────────────────────── GENERAL ─────
#

#Start
def start(update: Update, context: CallbackContext):
   update.message.reply_text(f'''
🧐️Daryl🧐️
👨‍🏫️General👨‍🏫️
    🌥️-/news (Whatever)
    🕵‍♂️️-/profile
    ⏰️-/timer (time in seconds)
💰️Economy💰️ 
    👷️-/work
    💸️-/bal
    💳️-/pay (UserName) (Amount)
    🛒️-/shop (list/buy) (item)
    ''')

#Profile
def profile(update= Update, context= CallbackContext):
    try:
        balance = db.child(update.message.from_user.username).get()
        bal = balance.val()['money']
        update.message.reply_text(f'''
🕵‍♂️️Profile🕵‍♂️️
🙅‍♂️️-Name : {update.message.from_user.first_name} {update.message.from_user.last_name}
👨‍💻️-Username : {update.message.from_user.username}
💸️-Money : {bal}$''')
    except:
        ecostart(update, context)
        profile(update, context)

#News
def news(update: Update, context: CallbackContext):
    try:
        googlenews = GoogleNews()
        googlenews.set_lang('en')
        googlenews.set_period('7d')
        googlenews.get_news(update.message.text.split(' ')[1])
        gnews = googlenews.get_texts()
        glinks = googlenews.get_links()
        update.message.reply_text(f'''<a href="{glinks[0]}">{gnews[0]}</a>

<a href="{glinks[1]}">{gnews[1]}</a>

<a href="{glinks[2]}">{gnews[2]}</a>
    ''',parse_mode=telegram.constants.PARSEMODE_HTML, disable_web_page_preview= True)
    except:
        update.message.reply_text(f'Search Failed Eror[404]')

#Timer
def timer(update: Update, context: CallbackContext):
    try:
        import time
        time.sleep(int(update.message.text.split(' ')[1])/int(update.message.text.split(' ')[1]))
        update.message.reply_text(f'Timer for {update.message.text.split(" ")[1]}s has just started')
        time.sleep(int(update.message.text.split(' ')[1]))
        update.message.reply_text(f'Your timer for {update.message.text.split(" ")[1]}s has just stoped!!!')
    except:
        update.message.reply_text(f'Unprocessable entity[422]')

#
# ────────────────────────────────────────────────────────────────── ECONOMY ─────
#

#Work
def work(update = Update, context = CallbackContext):
    try:
        work_list = ['Hacker', 'Softwear', 'Milkman']
        moneyearned = random.randrange(50,200)
        balance = db.child(update.message.from_user.username).get()
        for money in balance.each():
            data = money.val()
            data = {'money' : balance.val()['money'] + int(moneyearned)}
            db.child(update.message.from_user.username).update(data)
        update.message.reply_text(f'You worked as {random.choice(work_list)} and earnd {moneyearned}')
    except:
       ecostart(update, context)
       work(update, context)

#Balance
def bal(update: Update, context: CallbackContext):
    try:
        balance = db.child(update.message.from_user.username).get()
        bala = balance.val()['money']
        update.message.reply_text(f'Your Balance is {bala}$')
    except:
        ecostart(update, context)
        bal(update, context)

#Pay
def pay(update=Update, context= CallbackContext):
    try:
        balance = db.child(update.message.text.split(' ')[1]).get()
        balance = db.child(update.message.from_user.username).get()
        if int(update.message.text.split(' ')[2]) < balance.val()['money']:
            data = balance.val()['money']
            data = {'money' : balance.val()['money'] - int(update.message.text.split(' ')[2])}
            db.child(update.message.from_user.username).update(data)
            balance = db.child(update.message.text.split(' ')[1]).get()
            data = {'money' : balance.val()['money'] + int(update.message.text.split(' ')[2])}
            db.child(update.message.text.split(' ')[1]).set(data)
            who = update.message.text.split(' ')[1]
            hmm = update.message.text.split(' ')[2]
            update.message.reply_text(f'You paid {who} {hmm}$')
        else:
            update.message.reply_text(f'You cant afford it :([broke]')
    except:
        ecostart(update, context)
        pay(update, context)

#Shop
def shop(update=Update, context= CallbackContext):
    try:
        balance = db.child(update.message.from_user.username).get()
        bal = balance.val()['money']
        #List
        if update.message.text.split(" ")[1] == "list":
            def count(item):
                global itemc
                try:
                    itemc = balance.val()[item]
                except:
                    itemc = '0'
            count('gun')
            gunc = itemc 
            count('sunglasses')
            sunglassesc = itemc
            update.message.reply_text(f'''
            SHOP
            GUN {gunc}
            SUNGLASSES {sunglassesc}''')
        #Buy
        elif update.message.text.split(" ")[1] == "buy":
            def buying(item, price):
                try:
                    balance.val()[item]
                    data = {'money' : balance.val()['money'] - price, f'{item}' : balance.val()[item] + 1}
                    db.child(update.message.from_user.username).update(data)
                    update.message.reply_text(f'You bought a {item} for {price}$')
                except:
                    data = {'money' : balance.val()['money'] - price, f'{item}' : 1}
                    db.child(update.message.from_user.username).update(data)
                    update.message.reply_text(f'You bought a {item} for {price}$')
            if update.message.text.split(" ")[2] == "gun":
                buying("gun", 1000)
            if update.message.text.split(" ")[2] == "sunglasses":
                buying("sunglasses", 100)
    except:
        ecostart(update, context)
        shop(update, context)


# ─── COMMAND HANDLERS ───────────────────────────────────────────────────────────

#Shop
shop_handler = CommandHandler('shop', shop)
dispatcher.add_handler(shop_handler)

#Pay
pay_handler = CommandHandler('pay', pay)
dispatcher.add_handler(pay_handler)

#Profile
profile_handler = CommandHandler('profile', profile)
dispatcher.add_handler(profile_handler)

#News
news_handler = CommandHandler('news', news)
dispatcher.add_handler(news_handler)

#Start
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

#Timer
timer_handler = CommandHandler('timer', timer)
dispatcher.add_handler(timer_handler)

#Balance
bal_handler = CommandHandler('bal', bal)
dispatcher.add_handler(bal_handler)

#Work
work_handler = CommandHandler('work', work)
dispatcher.add_handler(work_handler)

# ─── POLLING ───────────────────────────────────────────────────────────────────

updater.start_polling()