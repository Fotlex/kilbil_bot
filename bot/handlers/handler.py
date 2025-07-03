from aiogram.types import Message, CallbackQuery, Contact
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.texts import *
from bot.keyboards import *
from bot.states import DateState
from panel.models import User
from bot.kilbil_api import *
from bot.utils import *
from panel.models import SupportHelp


router = Router()


@router.message(CommandStart())
async def started(message: Message, user: User):    
    await message.answer(text=START_TEXT)
    print(user.api_id)
    if user.phone_namber:
        result = await search_client(normalize_phone(user.phone_namber))
        
        if result.get('result_text') == 'Клиент найден':
            user.api_id = result.get("client_id")
            await user.asave()
            await message.answer(
                text='Добро пожаловать в меню',
                reply_markup=get_menu_keyboard()
            )
        else:
            await message.answer(
                text='Нужно зарегестрироваться',
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Начать регестрацию', callback_data='start_reg')]
                ])
            )
            
        return
    
    await message.answer(
        text='Для начала работы, пожалуйста, поделитесь своим контактом, нажав на кнопку ниже.',
        reply_markup=get_contact_keyboard()
    )   

    
@router.message(F.contact)
async def contact_handler(message: Message, user: User):
    contact: Contact = message.contact
    
    phone_number = contact.phone_number
    user.phone_namber = phone_number
    await user.asave()
    
    result = await search_client(normalize_phone(user.phone_namber))
        
    if result.get('result_text') == 'Клиент найден':
        user.api_id = result.get("client_id")
        await user.asave()
        await message.answer(
            text='Добро пожаловать в меню',
            reply_markup=get_menu_keyboard()
        )
    else:
        await message.answer(
            text='Нужно зарегестрироваться',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Начать регестрацию', callback_data='start_reg')]
            ])
        )
    
    
@router.callback_query(F.data == 'start_reg')
async def reg(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Введите ФИО, через пробел',
        reply_markup=None
    )
    await state.set_state(DateState.wait_name)
    await callback.answer('')
    
    
@router.message(F.text, DateState.wait_name)
async def names(message: Message, state: FSMContext, user: User):
    full_name = message.text.strip()  
    parts = full_name.split()  
    
    try:
        user.api_last_name = parts[0]
        user.api_first_name = parts[1]
        user.api_middlename = parts[2]
        
        await user.asave()
        
        await message.answer('Отлично, теперь введите вашу электронную почту')
        await state.set_state(DateState.wait_mail)
        
    except Exception as e:
        await message.answer('Вы ввели некоректное ФИО, попробуйте еще раз')
        await message.delete()
        return
    
    
@router.message(F.text, DateState.wait_mail)
async def mails(message: Message, state: FSMContext, user: User):
    if not is_valid_email_regex(message.text):
        await message.answer(text='Вы ввели некоректный email, попробуйте снова')
        await message.delete()
        return
    
    user.api_email = message.text
    await user.asave()
    
    await message.answer(
        text='Отлично! Теперь введите дату своего рождения в формате 25.06.2025'
    )
    
    await state.set_state(DateState.wait_date)
    
    
@router.message(F.text, DateState.wait_date)
async def dates(message: Message, state: FSMContext, user: User):
    if not is_valid_date(message.text):
        await message.answer(text='Вы ввели некоректную дату, попробуйте снова')
        await message.delete()
        return
    
    user.api_date_born = message.text
    await user.asave()
    
    await state.clear()
    
    response = await create_client(
        normalize_phone(user.phone_namber),
        user.api_last_name,
        user.api_first_name,
        user.api_middlename,
        user.api_email,
        user.api_date_born
    )
    
    client_id = response.get("client_id")
    
    if response:
        user.api_id = client_id
        await user.asave()
        print(user.api_id)
        await message.answer(
            text='Ваш клиент успешно создан!',
            reply_markup=get_menu_keyboard()
        )
        return
        
    await message.answer(text='Что-то пошло не так, попробуйте позже')
    
    
@router.message(F.text == 'Мой баланс')
async def ballances(message: Message, user: User):
    response = await get_ballance_info(user.api_id)
    operations = await get_operation_history(user.api_id)
    operations_list = operations.get('client_moves', [])
    if response and operations:
        total_balance = sum(float(item.get('balance', 0)) for item in response)
        try:
            total_money_spent = sum(float(item.get('move_asum', 0)) for item in operations_list)
        except Exception as e:
            total_money_spent = 0
        
        await message.answer(
            text=f'Ваш текущий баланс - {total_balance:.2f}.\nОбщая сумма покупок - {total_money_spent:.2f}',
            reply_markup=get_menu_keyboard()
        )
        
    else:
        await message.answer('Что-то пошло не так, попробуйте снова позже', reply_markup=get_menu_keyboard())

    
@router.message(F.text == 'История покупок')
async def purchase_history(message: Message, user: User):
    operations_data = await get_operation_history(user.api_id)

    if operations_data and operations_data.get("result_code") == "0":
        operations_list = operations_data.get('client_moves', [])
        
        final_message = format_history_message(operations_list)
        
        await message.answer(final_message)
    else:
        await message.answer("Не удалось получить историю операций. Пожалуйста, попробуйте снова позже.")
        
        
@router.message(F.text == 'Техническая поддержка')
async def support(message: Message):
    url = await SupportHelp.objects.aget(id=1)
    
    await message.answer(
        text='Переходите для решения ваших вопросов',
        reply_markup=get_support_keyboard(url.support_url)
    )
    
    
@router.message(F.text == 'Виртуальная карта')
async def wallet(message: Message, user: User):
    response = await get_wallet_card(user.api_id)
    print(response)
    
    if response and response.get("result_code") == 0:
        await message.answer(f'{response.get("wallet_link")}')
        return
    
    await message.answer('Что-то пошло не так, попробуйте снова позже')
        
    
    
    
    
    
        
    