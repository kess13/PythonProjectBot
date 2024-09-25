import asyncio
import pyodbc
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command, StateFilter
from aiogram import Router
import logging
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

#
# # Define your connection parameters
# server = 'your_public_ip_or_domain'  # Replace with your server's public IP or domain
# port = 1433  # Default port for SQL Server
# database = 'your_database'
# username = 'your_username'
# password = 'your_password'
#
# # Construct the connection string
# connection_string = (
#     f'DRIVER={{ODBC Driver 17 for SQL Server}};'
#     f'SERVER={server},{port};'
#     f'DATABASE={database};'
#     f'UID={username};'
#     f'PWD={password}'
# )




API_TOKEN = ''  # Replace with your actual bot token

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()

# Set up the database connection
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"  # Replace with your server
    "DATABASE=test;"  # Replace with your database name
    "Trusted_Connection=yes;"
    "TrustServerCertificate=Yes;"
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    print("Database connection successful.")
except pyodbc.Error as e:
    print("Error while connecting to database:", e)
    conn = None

# Define FSM States
class Form(StatesGroup):
    waiting_for_service = State()
    waiting_for_name = State()
    waiting_for_surname = State()
    waiting_for_email = State()
    waiting_for_phone = State()
    waiting_for_question = State()

button_text_mapping = {
    "tech_security": "Технічна охорона",
    "physical_security": "Фізична охорона",
    "certification": "Сертифікація",
    "training": "Навчання",
    "contract_docs": "Договірна документація",
    "payment": "Оплата",
    "object_security": "Охорона об'єктів",
    "home_security": "Охорона квартир та будинків",
    "gps_monitoring": "GPS моніторинг",
    "security_installation": "Монтаж систем безпеки",
    "personal_gps": "Персональний GPS трекінг",
    "fire_safety": "Пожежна безпека",
    "personal_security": "Охорона фізичних осіб",
    "object_physical_security": "Фізична охорона об'єктів",
    "cargo_security": "Охорона та супровід вантажів та цінностей",
    "military_security": "Воєнізована охорона",
    "gertc_payment": "Платіжна система ГЕРЦ",
    "city24_terminals": "Платіжні термінали City24",
    "ipay_payment": "Платіжна система Ipay",
    "portmone_payment": "Платіжна система Portmone",
    "city24_service": "Платіжний сервіс City24",
    "back_to_main": "⬅️ Назад"
}

@router.message(Command('start'))
async def send_main_menu(message: types.Message, state: FSMContext):
    buttons = [
        [types.InlineKeyboardButton(text="Технічна охорона", callback_data="tech_security")],
        [types.InlineKeyboardButton(text="Фізична охорона", callback_data="physical_security")],
        [types.InlineKeyboardButton(text="Сертифікація", callback_data="certification")],
        [types.InlineKeyboardButton(text="Навчання", callback_data="training")],
        [types.InlineKeyboardButton(text="Договірна документація", callback_data="contract_docs")],
        [types.InlineKeyboardButton(text="Оплата", callback_data="payment")]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.send_message(message.chat.id, "Виберіть послугу:", reply_markup=keyboard)
    await state.set_state(Form.waiting_for_service)


async def send_tech_security_menu(message: types.Message):
    buttons = [
        [types.InlineKeyboardButton(text="Охорона об'єктів", callback_data="object_security")],
        [types.InlineKeyboardButton(text="Охорона квартир та будинків", callback_data="home_security")],
        [types.InlineKeyboardButton(text="GPS моніторинг", callback_data="gps_monitoring")],
        [types.InlineKeyboardButton(text="Монтаж систем безпеки", callback_data="security_installation")],
        [types.InlineKeyboardButton(text="Персональний GPS трекінг", callback_data="personal_gps")],
        [types.InlineKeyboardButton(text="Пожежна безпека", callback_data="fire_safety")],
        [types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.send_message(message.chat.id, "Виберіть підкатегорію Технічна охорона:", reply_markup=keyboard)

async def send_physical_security_menu(message: types.Message):
    buttons = [
        [types.InlineKeyboardButton(text="Охорона фізичних осіб", callback_data="personal_security")],
        [types.InlineKeyboardButton(text="Фізична охорона об'єктів", callback_data="object_physical_security")],
        [types.InlineKeyboardButton(text="Охорона та супровід вантажів та цінностей", callback_data="cargo_security")],
        [types.InlineKeyboardButton(text="Воєнізована охорона", callback_data="military_security")],
        [types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.send_message(message.chat.id, "Виберіть підкатегорію Фiзична охорона:", reply_markup=keyboard)

async def send_payment_menu(message: types.Message):
    buttons = [
        [types.InlineKeyboardButton(text="Платіжна система ГЕРЦ", callback_data="gertc_payment")],
        [types.InlineKeyboardButton(text="Платіжні термінали City24", callback_data="city24_terminals")],
        [types.InlineKeyboardButton(text="Платіжна система Ipay", callback_data="ipay_payment")],
        [types.InlineKeyboardButton(text="Платіжна система Portmone", callback_data="portmone_payment")],
        [types.InlineKeyboardButton(text="Платіжний сервіс City24", callback_data="city24_service")],
        [types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.send_message(message.chat.id, "Виберіть платіжний сервіс:", reply_markup=keyboard)

@router.callback_query(lambda call: True)
async def handle_callback(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    # Retrieve current state data
    data = await state.get_data()

    if call.data == "tech_security":
        await send_tech_security_menu(call.message)
        data['Послуга'] = "Технічна охорона"
        await state.update_data(Послуга=data['Послуга'])

    elif call.data == "physical_security":
        await send_physical_security_menu(call.message)
        data['Послуга'] = "Фізична охорона"
        await state.update_data(Послуга=data['Послуга'])

    elif call.data == "payment":
        await send_payment_menu(call.message)
        data['Послуга'] = "Оплата"
        await state.update_data(Послуга=data['Послуга'])

    elif call.data == "object_security":
        await handle_subcategory_selection(call.message, state, "Охорона об'єктів")

    elif call.data == "home_security":
        await handle_subcategory_selection(call.message, state, "Охорона квартир та будинків")

    elif call.data == "gps_monitoring":
        await handle_subcategory_selection(call.message, state, "GPS моніторинг")

    elif call.data == "security_installation":
        await handle_subcategory_selection(call.message, state, "Монтаж систем безпеки")

    elif call.data == "personal_gps":
        await handle_subcategory_selection(call.message, state, "Персональний GPS трекінг")

    elif call.data == "fire_safety":
        await handle_subcategory_selection(call.message, state, "Пожежна безпека")

    elif call.data == "back_to_main":
        await send_main_menu(call.message, state)
        await state.clear()  # Clear the state when going back to the main menu

    elif call.data == "skip_field":
        await process_user_input(call.message, state, skipped=True)

    else:
        await bot.send_message(call.message.chat.id, "Вибір не зрозумілий. Спробуйте ще раз.")

async def handle_subcategory_selection(message: types.Message, state: FSMContext, subcategory: str):
    data = await state.get_data()
    data['Підкатегорія'] = subcategory
    await state.update_data(Підкатегорія=data['Підкатегорія'])
    await bot.send_message(message.chat.id, f"Ви обрали {subcategory}.")
    await bot.send_message(message.chat.id, "Введiть своє Iм'я.")
    await state.set_state(Form.waiting_for_name)

@router.message(StateFilter([Form.waiting_for_name, Form.waiting_for_surname, Form.waiting_for_email, Form.waiting_for_phone, Form.waiting_for_question]))
async def process_user_input(message: types.Message, state: FSMContext, skipped=False):
    data = await state.get_data()
    current_state = await state.get_state()
    current_message = message.text

    buttons = [[types.InlineKeyboardButton(text="Пропустити", callback_data="skip_field")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    if current_state == Form.waiting_for_name.state:
        if not skipped:
            data['Name'] = current_message
        else:
            data['Name'] = "Пропущено"
        await state.update_data(Name=data['Name'])
        await bot.send_message(message.chat.id, "Будь ласка введiть своє прізвище", reply_markup=keyboard)
        await state.set_state(Form.waiting_for_surname)

    elif current_state == Form.waiting_for_surname.state:
        if not skipped:
            data['Прізвище'] = current_message
        else:
            data['Прізвище'] = "Пропущено"
        await state.update_data(Прізвище=data['Прізвище'])
        await bot.send_message(message.chat.id, "Будь ласка введiть свій Email (не обязательно чтобы пропустить нажмите кнопку нижче))", reply_markup=keyboard)
        await state.set_state(Form.waiting_for_email)

    elif current_state == Form.waiting_for_email.state:
        if not skipped:
            data['Email'] = current_message
        else:
            data['Email'] = "Пропущено"
        await state.update_data(Email=data['Email'])
        await bot.send_message(message.chat.id, "Будь ласка введiть свій номер телефону", reply_markup=keyboard)
        await state.set_state(Form.waiting_for_phone)

    elif current_state == Form.waiting_for_phone.state:
        if not skipped:
            data['Телефон'] = current_message
        else:
            data['Телефон'] = "Пропущено"
        await state.update_data(Телефон=data['Телефон'])
        await bot.send_message(message.chat.id, "Будь ласка введiть ваше запитання", reply_markup=keyboard)
        await state.set_state(Form.waiting_for_question)

    elif current_state == Form.waiting_for_question.state:
        if not skipped:
            data['Запитання'] = current_message
        else:
            data['Запитання'] = "Пропущено"
        await state.update_data(Запитання=data['Запитання'])
        await bot.send_message(message.chat.id, "Дякую! Ваші дані були збережені.")

        for key, value in data.items():
            await bot.send_message(message.chat.id, f"данi: {key} : {value}")

        await save_user_data_to_db(data)
        await state.clear()

async def save_user_data_to_db(user_data):
    if conn:
        try:
            insert_query = """
            INSERT INTO users1 (service, name, surname, email, phone_number, question)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, (
                user_data.get('Послуга', ''),
                user_data.get('Name', ''),
                user_data.get('Прізвище', ''),
                user_data.get('Email', ''),
                user_data.get('Телефон', ''),
                user_data.get('Запитання', '')
            ))
            conn.commit()
            print("Data saved to database successfully.")
        except pyodbc.Error as e:
            print("Error while executing query:", e)

@router.message(lambda message: True)
async def echo_message(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.reply("Невiдома команда, введiть /start")
    else:
        await process_user_input(message, state)

# Register the router with the dispatcher
dp.include_router(router)

# Define an async function to start polling
async def on_startup():
    try:
        await dp.start_polling(bot, skip_updates=True)
    except asyncio.CancelledError:
        print("Polling was cancelled.")
    finally:
        await bot.session.close()
        if conn:
            conn.close()
            print("Database connection closed.")

# Run the bot
if __name__ == '__main__':
    asyncio.run(on_startup())
