import re
from datetime import datetime


def is_valid_email_regex(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.fullmatch(pattern, email))


def normalize_phone(phone: str) -> str:
    digits = ''.join(filter(str.isdigit, phone))
    
    if digits.startswith('7') and len(digits) == 11:
        return digits
    elif digits.startswith('8') and len(digits) == 11:
        return '7' + digits[1:]
    elif digits.startswith('+7') and len(digits) == 11:
        return '7' + digits[2:]
    else:
        return digits  
    

def is_valid_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False
    
    

# ... (другие импорты и код роутера) ...

def format_history_message(operations_list: list) -> str:
    if not operations_list:
        return "У вас еще нет ни одной операции."

    oper_type_map = {
        0: ("🛍️ Продажа", "Сумма покупки"),
        1: ("↩️ Возврат", "Сумма возврата"),
        2: ("🤖 Автоматическая операция", "Сумма"),
        3: ("✍️ Ручное начисление", "Сумма")
    }
    
    message_lines = ["📋 **Ваша история операций:**\n"]
    

    for operation in operations_list[:10]:
        op_type = operation.get('oper_type')
        date_str = operation.get('move_date', 'неизвестно')
        bonus_in = operation.get('bonus_in', 0.0)
        bonus_out = operation.get('bonus_out', 0.0)
        move_asum = operation.get('move_asum', 0.0)

        op_info = oper_type_map.get(op_type, ("❔ Неизвестная операция", "Сумма"))
        op_description, asum_label = op_info

        try:
            formatted_date = datetime.strptime(date_str, '%d.%m.%Y %H:%M:%S').strftime('%d.%m.%Y')
        except (ValueError, TypeError):
            formatted_date = date_str

        entry_text = f"**{op_description}** ({formatted_date})"
        
        if move_asum != 0:
            entry_text += f"\n- {asum_label}: {move_asum:.2f} руб."
        if bonus_in > 0:
            entry_text += f"\n- ✅ Начислено: +{bonus_in:.2f} бонусов"
        if bonus_out > 0:
            entry_text += f"\n- ❌ Списано: -{bonus_out:.2f} бонусов"
            
        message_lines.append(entry_text)

    return "\n\n".join(message_lines)