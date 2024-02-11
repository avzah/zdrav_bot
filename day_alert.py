import json
from bot.bot import Bot
from bot.handler import MessageHandler, BotButtonCommandHandler

TOKEN = "001.1888341050.2947708086:89260743344"

bot = Bot(token=TOKEN, api_url_base='https://api.armgs.team/bot/v1')

DATABASE_PATH = 'main.json'
ADDRESS_PATH = 'resp.json'

try:
    with open(DATABASE_PATH, "r") as read_file:
        arUsers = json.load(read_file)
except:
    arUsers = {}

def message_cb(bot, event):
    print(event)

    if event.text == '/start':
        arUsers[event.data['from']['userId']] = event.data['from']
        with open(DATABASE_PATH, "w") as write_file:
            json.dump(arUsers, write_file)

    try:
        with open(ADDRESS_PATH, "r") as read_file:
            db_for_notifications = json.load(read_file)
    except:
        db_for_notifications = {}

    # print(db_for_notifications)
    print('Пользователи: ', arUsers)

    start = event.text.find('Министерство здравоохранения')
    zdrav_all_old = event.text[start:]
    finish = zdrav_all_old.find('.')
    zdrav_all = zdrav_all_old[:finish]

    print('Пришло: ', zdrav_all)

    if not zdrav_all:
        print("Сегодня нет замечаний по здраву")
        send_alert(
            'Алексей Викторович, сегодня необновлённых дашбордов здравоохранения нет',
            'aleksey.zaharov@tularegion.ru')

    d_bd = {}
    all_zdrav_strings = zdrav_all.split('Информационная панель: ')
    del all_zdrav_strings[0]

    print("*0*")
    print(all_zdrav_strings)

    for s in all_zdrav_strings:

        lines = s.split(';')[0].split(': ')[1].split(', ')

        print("**", lines)

        db_name = s.split(',')[0]

        d_bd[db_name] = lines

        print(d_bd, '*********')

        for line in lines:
            print(db_name, line, '!!!')

            try:
                userID = db_for_notifications.get(db_name).get(line)
                print('userID: ', userID)

                send_alert('Уважаемый методист {0} {3}, когда обновите свой дашборд {1}, лист {2}?'
                           .format(arUsers[userID]['firstName'], db_name, line, arUsers[userID]['lastName']), userID)

                send_alert(
                    'Михаил Владимирович, сегодня не обновлён дашборд {1}, лист {2}, отвественный пользователь - {0} {3}. Не ругайте его, пожалуйста, сильно...'
                    .format(arUsers[userID]['firstName'], db_name, line, arUsers[userID]['lastName']),
                    'aleksey.zaharov@tularegion.ru')

            except:
                print("Нет данных методиста листа '{0}' дашборда '{1}'".format(line, db_name))

                send_alert(
                    'Михаил Владимирович, сегодня не обновлён дашборд {0}, лист {1}, отвественного пользователя я не нашел. Может Вы знаете, кто за этот показатель может отвечать?'
                    .format(db_name, line), 'aleksey.zaharov@tularegion.ru')

def send_alert(text_to_send, chat):
    print('chat: ', chat)
    print('text_to_send: ', text_to_send)

    bot.send_text(chat_id=chat, text=text_to_send)


bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.start_polling()
bot.idle()
