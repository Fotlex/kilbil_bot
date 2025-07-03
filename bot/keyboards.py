from aiogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                           KeyboardButton, InlineKeyboardButton)


def get_contact_keyboard() -> ReplyKeyboardMarkup:
    contact_button = KeyboardButton(
        text="📱 Поделиться контактом", 
        request_contact=True  
    )
    
    contact_keyboard = ReplyKeyboardMarkup(
        keyboard=[[contact_button]], 
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return contact_keyboard

def get_menu_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Виртуальная карта')],
        [KeyboardButton(text='Мой баланс')],
        [KeyboardButton(text='История покупок')],
        [KeyboardButton(text='Техническая поддержка')],
    ])
    
    
def get_support_keyboard(url):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Тех Поддержка', url=url)]
    ])