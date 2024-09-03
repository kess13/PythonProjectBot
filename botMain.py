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

API_TOKEN = '7432072184:AAGv-OH_DANt29xGBUJjQW1vryDPqgX_28I'  # Replace with your actual bot token

logging.basicConfig(level=logging.INFO)
is_skipped = False
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


async def  is_skipped(skipped):
    return skipped

@router.callback_query(lambda call: True)
async def handle_callback(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    # Retrieve current state data
    data = await state.get_data()

    if call.data == "tech_security":
        # Display the submenu for "Технічна охорона"
        await send_tech_security_menu(call.message)
        data['Послуга'] = "Технічна охорона"
        await state.update_data(Послуга=data['Послуга'])

    elif call.data == "physical_security":
        # Display the submenu for "Фізична охорона"
        await send_physical_security_menu(call.message)
        data['Послуга'] = "Фізична охорона"
        await state.update_data(Послуга=data['Послуга'])

    elif call.data == "payment":
        # Display the submenu for "Оплата"
        await send_payment_menu(call.message)
        data['Послуга'] = "Оплата"
        await state.update_data(Послуга=data['Послуга'])

    elif call.data == "object_security":
        await bot.send_message(call.message.chat.id, "Ви обрали Охорона об'єктів.")
        data['Підкатегорія'] = "Охорона об'єктів"
        await state.update_data(Підкатегорія=data['Підкатегорія'])
        await bot.send_message(call.message.chat.id, "Введiть своє Iм'я.")
        await state.set_state(Form.waiting_for_name)  # Set the state

    elif call.data == "home_security":
        await bot.send_message(call.message.chat.id, "Ви обрали Охорона квартир та будинків.")
        data['Підкатегорія'] = "Охорона квартир та будинків"
        await state.update_data(Підкатегорія=data['Підкатегорія'])
        await bot.send_message(call.message.chat.id, "Введiть своє Iм'я.")
        await state.set_state(Form.waiting_for_name)  # Set the state

    elif call.data == "gps_monitoring":
        await bot.send_message(call.message.chat.id, "Ви обрали GPS моніторинг.")
        data['Підкатегорія'] = "GPS моніторинг"
        await state.update_data(Підкатегорія=data['Підкатегорія'])
        await bot.send_message(call.message.chat.id, "Введiть своє Iм'я.")
        await state.set_state(Form.waiting_for_name)  # Set the state

    elif call.data == "security_installation":
        await bot.send_message(call.message.chat.id, "Ви обрали Монтаж систем безпеки.")
        data['Підкатегорія'] = "Монтаж систем безпеки"
        await state.update_data(Підкатегорія=data['Підкатегорія'])
        await bot.send_message(call.message.chat.id, "Введiть своє Iм'я.")
        await state.set_state(Form.waiting_for_name)  # Set the state

    elif call.data == "personal_gps":
        await bot.send_message(call.message.chat.id, "Ви обрали Персональний GPS трекінг.")
        data['Підкатегорія'] = "Персональний GPS трекінг"
        await state.update_data(Підкатегорія=data['Підкатегорія'])
        await bot.send_message(call.message.chat.id, "Введiть своє Iм'я.")
        await state.set_state(Form.waiting_for_name)  # Set the state

    elif call.data == "fire_safety":
        await bot.send_message(call.message.chat.id, "Ви обрали Пожежна безпека.")
        data['Підкатегорія'] = "Пожежна безпека"
        await state.update_data(Підкатегорія=data['Підкатегорія'])
        await bot.send_message(call.message.chat.id, "Введiть своє Iм'я.")
        await state.set_state(Form.waiting_for_name)  # Set the state

    elif call.data == "back_to_main":
        # Go back to the main menu
        await send_main_menu(call.message, state)
        await state.clear()  # Clear the state when going back to the main menu




    else:
        # Handle any unknown callback queries
        await bot.send_message(call.message.chat.id, "Вибір не зрозумілий. Спробуйте ще раз.")


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

@router.message(StateFilter([Form.waiting_for_name, Form.waiting_for_surname, Form.waiting_for_email, Form.waiting_for_phone, Form.waiting_for_question]))
async def process_user_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_state = await state.get_state()
    current_message = message.text

    buttons = [
        [types.InlineKeyboardButton(text="Пропустити", callback_data="skipp")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    if current_state == Form.waiting_for_name.state:
        data['Name'] = current_message
        await state.update_data(Name=data['Name'])
        await bot.send_message(message.chat.id, "Будь ласка введiть своє прізвище")
        await state.set_state(Form.waiting_for_surname)

    elif current_state == Form.waiting_for_surname.state:
        data['Прізвище'] = current_message
        await state.update_data(Прізвище=data['Прізвище'])
        await bot.send_message(message.chat.id, "Будь ласка введiть свій Email (не обязательно чтобы пропустить нажмите кнопку нижче))", reply_markup=keyboard)
        await state.set_state(Form.waiting_for_email)

    elif current_state == Form.waiting_for_email.state:
        data['Email'] = current_message
        await state.update_data(Email=data['Email'])
        await bot.send_message(message.chat.id, "Будь ласка введiть свій номер телефону")
        await state.set_state(Form.waiting_for_phone)

    elif current_state == Form.waiting_for_phone.state:
        data['Телефон'] = current_message
        await state.update_data(Телефон=data['Телефон'])
        await bot.send_message(message.chat.id, "Будь ласка введiть ваше запитання")
        await state.set_state(Form.waiting_for_question)

    elif current_state == Form.waiting_for_question.state:
        data['Запитання'] = current_message
        await state.update_data(Запитання=data['Запитання'])
        await bot.send_message(message.chat.id, "Дякую! Ваші дані були збережені")

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
                user_data['Послуга'],
                user_data['Name'],
                user_data['Прізвище'],
                user_data['Email'],
                user_data['Телефон'],
                user_data['Запитання']
            ))
            conn.commit()
            print("Data saved to database successfully.")
        except pyodbc.Error as e:
            print("Error while executing query:", e)

@router.message(lambda message: True)
async def echo_message(message: types.Message, state: FSMContext):
    is_skipped = False
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

# Close the database connection when the script ends
if conn:
    conn.close()
    print("Database connection closed.")
