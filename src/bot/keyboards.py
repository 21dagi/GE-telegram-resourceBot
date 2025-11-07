from typing import Callable
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from database.firestore_service import get_categories_by_parent, get_category

async def get_main_menu_keyboard(is_admin: bool, _: Callable) -> ReplyKeyboardMarkup:
    """Generates the main menu as a persistent reply keyboard."""
    buttons = [
        # MODIFICATION: Added Search button
        [KeyboardButton(text=_("Search 🔎"))],
        [
            KeyboardButton(text=_("የመጻሕፍት ቤት")),
            KeyboardButton(text=_("የዜማ ቤት")),
        ],
        [KeyboardButton(text=_("ኪነ ጥበብ"))],
        [
            KeyboardButton(text=_("ስለ ገዳሜ እየሱስ")),
            KeyboardButton(text=_("እኛን ያግኙን")),
        ],
        [KeyboardButton(text=_("ቋንቋ ቀይር"))],
    ]
    if is_admin:
        buttons.insert(4, [ # Adjusted index for the new search button
            KeyboardButton(text=_("ፋይሎችን አስገባ")),
            KeyboardButton(text=_("ተጠቃሚዎችን ያስተዳድሩ")),
        ])
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder=_("Select an option or search")
    )
def get_search_results_keyboard(results: list, _: Callable) -> InlineKeyboardMarkup:
    """Generates an inline keyboard with search results."""
    buttons = []
    row = []
    for res in results:
        # Use the short document ID, same as the resource keyboard
        row.append(InlineKeyboardButton(text=res["file_name"], callback_data=f"res_{res['id']}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    
    # Add a button to close/dismiss the search results
    buttons.append([InlineKeyboardButton(text=_("Close Search"), callback_data="close_search")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
def get_language_keyboard() -> InlineKeyboardMarkup:
    """Generates the language selection keyboard (remains inline)."""
    buttons = [[
        InlineKeyboardButton(text="English", callback_data="lang_en"),
        InlineKeyboardButton(text="አማርኛ", callback_data="lang_am"),
        InlineKeyboardButton(text="Afaan Oromoo", callback_data="lang_or"),
    ]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def get_submenu_keyboard(parent_id: str, lang: str, _: Callable) -> InlineKeyboardMarkup:
    """Generates a submenu keyboard for a given parent category."""
    subcategories = await get_categories_by_parent(parent_id)
    category = await get_category(parent_id)
    grandparent_id = category.get('parent_id', 'main') if category else 'main'

    buttons = []
    row = []
    lang_name_key = f"name_{lang}"
    for sub in subcategories:
        button_text = sub.get(lang_name_key, sub.get("name_am"))
        row.append(InlineKeyboardButton(text=button_text, callback_data=f"nav_{sub['id']}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row: buttons.append(row)

    buttons.append([InlineKeyboardButton(text=_("ተመለስ"), callback_data=f"nav_{grandparent_id}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def get_resources_keyboard(resources: list, parent_id: str, _: Callable) -> InlineKeyboardMarkup:
    """Generates a keyboard with a list of resources."""
    buttons = []
    row = []
    for res in resources:
        # MODIFICATION: Use the short document ID in callback_data, not the long file_id
        row.append(InlineKeyboardButton(text=res["file_name"], callback_data=f"res_{res['id']}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row: buttons.append(row)

    buttons.append([InlineKeyboardButton(text=_("ተመለስ"), callback_data=f"nav_{parent_id}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def get_back_keyboard(callback_data: str, _: Callable) -> InlineKeyboardMarkup:
    """Generates a simple back button keyboard."""
    buttons = [[InlineKeyboardButton(text=_("ተመለስ"), callback_data=callback_data)]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)