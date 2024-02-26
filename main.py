import telebot
from telebot import types

bot = telebot.TeleBot('XXX')

comics = {
    'Комикс 1': ['page1_1.jpg', 'page2_1.jpg', 'page3_1.jpg', 'page4_1.jpg', 'page5_1.jpg'],
    'Комикс 2': ['page1_2.jpg', 'page2_2.jpg', 'page3_2.jpg', 'page4_2.jpg', 'page5_2.jpg'],
    'Комикс 3': ['page1_3.jpg', 'page2_3.jpg', 'page3_3.jpg', 'page4_3.jpg', 'page5_3.jpg']
}

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for comic_title in comics:
        button = types.InlineKeyboardButton(text=comic_title, callback_data=comic_title)
        keyboard.add(button)
    bot.send_message(message.chat.id, "Выберите комикс для просмотра:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    if call.data in comics:
        user_data[chat_id] = {'comic': call.data, 'page': 0}
        send_comic_page(chat_id)
    elif call.data in ['prev', 'reset', 'next']:
        handle_callback(chat_id, call.data)

def send_comic_page(chat_id):
    user_info = user_data[chat_id]
    comic_title = user_info['comic']
    current_page = user_info['page']

    if 0 <= current_page < len(comics[comic_title]):
        page_image = comics[comic_title][current_page]
        image_path = f"comics_png/{page_image}"
        photo = open(image_path, 'rb')
        bot.send_photo(chat_id, photo)

        keyboard = types.InlineKeyboardMarkup(row_width=3)
        buttons = [
            types.InlineKeyboardButton(text='⏪', callback_data='prev'),
            types.InlineKeyboardButton(text='🔄', callback_data='reset'),
            types.InlineKeyboardButton(text='⏩', callback_data='next')
        ]
        keyboard.add(*buttons)

        bot.send_message(chat_id, "Выберите действие:", reply_markup=keyboard)
    else:
        del user_data[chat_id]
        start_over(chat_id)

def start_over(chat_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for comic_title in comics:
        button = types.InlineKeyboardButton(text=comic_title, callback_data=comic_title)
        keyboard.add(button)
    bot.send_message(chat_id, "Выберите комикс для просмотра:", reply_markup=keyboard)

def handle_callback(chat_id, data):
    user_info = user_data.get(chat_id)
    if user_info and data in ['prev', 'reset', 'next']:
        if data == 'prev':
            user_info['page'] -= 1
        elif data == 'next':
            user_info['page'] += 1

        send_comic_page(chat_id)
    elif data == 'reset':
        del user_data[chat_id]
        start_over(chat_id)

bot.polling()
