import telebot
from telebot import types

# --- ⚙️ НАСТРОЙКИ БОТА ---
TOKEN = 'ТВОЙ_ТОКЕН'
ADMIN_ID = 6305773261  # Твой личный ID
SUPPORT_LINK = 'https://t.me/ТВОЙ_ЛОГИН'

# 🎥 ID ВИДЕО (Вставлять сюда!)
VIDEO_ABOUT = 'СЮДА_ID_ВИДЕО_О_ПОДПИСКЕ'
VIDEO_CODES = 'СЮДА_ID_ВИДЕО_КАК_НАЙТИ_КОДЫ'

bot = telebot.TeleBot(TOKEN)
user_data = {}

# --- 💼 БАЗА ПРОМОКОДОВ (ДЛЯ БЛОГЕРОВ) ---
# Здесь мы настраиваем, какой блогер кого привел и из какой он страны
PROMO_DB = {
    'UZB_BLOG': {'discount': 500, 'region': 'UZ', 'owner': 'Блогер Узбекистан'},
    'RU_BLOG': {'discount': 500, 'region': 'RU', 'owner': 'Блогер Россия'},
    'IT_MINSK': {'discount': 700, 'region': 'BY', 'owner': 'Блогер Беларусь'}
}

# --- 🎛 КЛАВИАТУРЫ ---
def main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🛒 Купить подписку", callback_data="buy_menu"),
        types.InlineKeyboardButton("ℹ️ О подписке", callback_data="about_sub"),
        types.InlineKeyboardButton("📜 Правила и Поддержка", callback_data="rules_support")
    )
    return markup

def back_keyboard(callback_data="start"):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data=callback_data))
    return markup

# --- 🚀 1. ГЛАВНОЕ МЕНЮ ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.clear_step_handler_by_chat_id(chat_id)
    user_data[chat_id] = {'price': 4000, 'promo_applied': False, 'region': 'ALL', 'promo_name': None}
    
    text = (
        "Добро пожаловать! Ваша безопасность — это наш приоритет 🛡️\n\n"
        "Этот бот — твой прямой доступ к официальной премиум-подписке **Google AI Pro (Gemini Pro + 2 ТБ хранилища)**.\n\n"
        "Выбери нужный раздел ниже 👇"
    )
    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=main_keyboard())

# --- 🔄 ОБРАБОТКА ВСЕХ КНОПОК ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    bot.clear_step_handler_by_chat_id(chat_id) 

    if chat_id not in user_data:
        user_data[chat_id] = {'price': 4000, 'promo_applied': False, 'region': 'ALL', 'promo_name': None}

    if call.data == "start":
        bot.delete_message(chat_id, call.message.message_id)
        send_welcome(call.message)

    # ... (ЗДЕСЬ ОСТАЕТСЯ ТВОЙ СТАРЫЙ КОД ДЛЯ "about_sub" И "rules_support") ...

    # 🛒 Меню покупки
    elif call.data == "buy_menu":
        price = user_data[chat_id]['price']
        text = f"💳 **Оформление подписки Google AI Pro.**\n\nК оплате: **{price} руб.**\n"
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(f"✅ Перейти к оплате ({price} руб.)", callback_data="pay_step"))
        if not user_data[chat_id]['promo_applied']:
            markup.add(types.InlineKeyboardButton("🎁 Ввести промокод от блогера", callback_data="ask_promo"))
        markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="start"))
        
        bot.edit_message_text(text, chat_id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

    # 🎁 Промокод
    elif call.data == "ask_promo":
        bot.edit_message_text("Напишите ваш промокод прямо в этот чат 👇", chat_id, call.message.message_id, reply_markup=back_keyboard("buy_menu"))
        bot.register_next_step_handler(call.message, process_promo)

    # 💳 Оплата (НОВАЯ СИСТЕМА КНОПОК)
    elif call.data == "pay_step":
        price = user_data[chat_id]['price']
        region = user_data[chat_id]['region']
        
        text = f"💳 **Выберите удобный способ оплаты на {price} руб.:**\n\n*Выберите вашу страну или крипту:*"
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        # Динамические кнопки (если промокод РФ - ставим РФ наверх)
        btn_rf = types.InlineKeyboardButton("🇷🇺 Карты РФ / СБП", url="https://payok.io/ПУСТЫШКА")
        btn_world = types.InlineKeyboardButton("🌍 Visa / Mastercard (Мир)", url="https://boosty.to/ПУСТЫШКА")
        btn_kaspi = types.InlineKeyboardButton("🇰🇿 Kaspi Bank (Казахстан)", callback_data="show_kaspi")
        btn_crypto = types.InlineKeyboardButton("💎 Криптовалюта (USDT)", url="https://t.me/CryptoBot?start=ПУСТЫШКА")
        
        # Меняем порядок в зависимости от промокода блогера
        if region == 'RU':
            markup.add(btn_rf, btn_world, btn_kaspi, btn_crypto)
        elif region == 'UZ':
            # Для УЗБ пока даем международную оплату и крипту наверх
            markup.add(btn_world, btn_crypto, btn_rf, btn_kaspi)
        else:
            markup.add(btn_rf, btn_world, btn_kaspi, btn_crypto)
            
        markup.add(types.InlineKeyboardButton("📸 Я ОПЛАТИЛ (Отправить чек)", callback_data="wait_for_receipt"))
        markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="buy_menu"))
        
        bot.edit_message_text(text, chat_id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

    # Показать реквизиты Kaspi
    elif call.data == "show_kaspi":
        price_kzt = int(user_data[chat_id]['price'] * 4.8) # Примерный курс
        bot.send_message(chat_id, f"🇰🇿 **Переведите {price_kzt} тенге на Kaspi:**\n\nНомер: `+7 707 XXX XX XX`\nПолучатель: Давронбек Б.\n\nПосле перевода нажмите кнопку 'Я ОПЛАТИЛ' в меню выше.", parse_mode='Markdown')

    # Ожидание чека
    elif call.data == "wait_for_receipt":
        bot.send_message(chat_id, "🧾 Отправьте фотографию чека или скриншот об оплате прямо в этот чат:")
        bot.register_next_step_handler(call.message, handle_receipt)

    # ... (ОСТАЛЬНОЙ КОД АДМИНКИ И ВЫДАЧИ АККАУНТОВ ОСТАЕТСЯ ТАКИМ ЖЕ) ...

# --- ФУНКЦИИ ЛОГИКИ ---
def process_promo(message):
    chat_id = message.chat.id
    promo = message.text.strip().upper()
    
    if promo in PROMO_DB:
        discount = PROMO_DB[promo]['discount']
        user_data[chat_id]['price'] -= discount
        user_data[chat_id]['promo_applied'] = True
        user_data[chat_id]['region'] = PROMO_DB[promo]['region']
        user_data[chat_id]['promo_name'] = promo
        
        bot.send_message(chat_id, f"🎉 Промокод найден! Скидка {discount} руб. применена.", reply_markup=back_keyboard("buy_menu"))
        # Уведомляем админа, что кто-то пришел от блогера
        bot.send_message(ADMIN_ID, f"👀 Клиент ввел промокод: {promo} (Блогер: {PROMO_DB[promo]['owner']})")
    else:
        bot.send_message(chat_id, "❌ Промокод не найден или недействителен.", reply_markup=back_keyboard("buy_menu"))

def handle_receipt(message):
    chat_id = message.chat.id
    promo_used = user_data[chat_id]['promo_name']
    promo_text = f"\n🎁 Использован промо: {promo_used}" if promo_used else "\n❌ Без промокода"
    
    if message.photo or message.document:
        bot.send_message(chat_id, "⏳ Чек отправлен на проверку. Ожидайте.")
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("✅ Подтвердить оплату", callback_data=f"confirm_pay_{chat_id}"),
            types.InlineKeyboardButton("❌ Отклонить чек", callback_data=f"reject_pay_{chat_id}")
        )
        caption = f"💰 ЧЕК ОТ КЛИЕНТА: {chat_id}{promo_text}"
        
        if message.photo:
            bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=caption, reply_markup=markup)
        else:
            bot.send_document(ADMIN_ID, message.document.file_id, caption=caption, reply_markup=markup)
    else:
        bot.send_message(chat_id, "Пожалуйста, отправьте именно картинку или файл чека.")
        bot.register_next_step_handler(message, handle_receipt)

# ... (Остальные функции оставляй без изменений) ...

print("Бот успешно запущен! Ожидание сообщений...")
try:
    bot.infinity_polling(timeout=90, long_polling_timeout=50)
except Exception as e:
    print(f"Ошибка интернета: {e}")
