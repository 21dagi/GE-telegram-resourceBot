import os
from typing import Callable
from aiogram import F, Router, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup

# MODIFICATION: Added 'get_language_keyboard' to the import list
from bot.keyboards import get_main_menu_keyboard, get_submenu_keyboard, get_resources_keyboard, get_language_keyboard
from bot.states import Contact # Import the new state
from database.firestore_service import get_user, update_user_language, get_category, get_resources_by_category, is_admin as is_admin_db, get_resource_by_id
from utils.i18n import translations

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message, _: Callable):
    """Greets the user with a more engaging welcome message."""
    await get_user(str(message.from_user.id), message.from_user.username)
    
    welcome_text = (
        "✨ <b>ሰላም፣ እንኳን ወደ ገዳመ ኢየሱስ በደህና መጡ</b> ✨\n\n"
        "<i>Peace be upon you, and welcome to Gedame Eyesus.</i>\n\n"
        "ይህ ቦት መንፈሳዊ እና አካዳሚያዊ ዕውቀትን ለማበልጸግ የተዘጋጀ ነው። በውስጡም የዜማ ትምህርቶችን፣ መጻሕፍትን፣ እና ሌሎች መንፈሳዊ ሀብቶችን ያገኛሉ።\n\n"
        "This is a sanctuary for spiritual and academic enrichment. Within, you will find a treasury of Zema chants, sacred texts, and other resources to enlighten the soul.\n\n"
        "በእግዚአብሔር ቸርነት ጉዞአችንን እንጀምር።\n"
        "<i>Let us begin our journey with the grace of God.</i> 🙏"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🕊️ ጉዞአችንን እንጀምር (Begin Journey)", callback_data="show_main_menu")]
    ])
    
    await message.answer(welcome_text, reply_markup=keyboard, parse_mode="HTML")

# Handler for the "Let's Get Started!" button
@router.callback_query(F.data == "show_main_menu")
async def show_main_menu_handler(callback_query: CallbackQuery, _: Callable):
    """Displays the main menu using ReplyKeyboardMarkup."""
    user_id = str(callback_query.from_user.id)
    is_admin = await is_admin_db(user_id)

    # Edit the welcome message to remove the button
    await callback_query.message.edit_text(_("Main Menu"))
    
    # Send a new message with the persistent keyboard
    await callback_query.message.answer(
        text=_("Please select an option from the menu below."),
        reply_markup=await get_main_menu_keyboard(is_admin, _)
    )
    await callback_query.answer()

# Message Handlers for Reply Keyboard buttons
@router.message(F.text.in_({"የመጻሕፍት ቤት", "Library", "Mana Kitaabaa"}))
async def library_menu_handler(message: Message, _: Callable):
    user = await get_user(str(message.from_user.id), "")
    await message.answer(
        _("Please choose a subcategory:"),
        reply_markup=await get_submenu_keyboard("main-library", user.get("language", "am"), _)
    )

@router.message(F.text.in_({"የዜማ ቤት", "Zema House", "Mana Zema"}))
async def zema_menu_handler(message: Message, _: Callable):
    user = await get_user(str(message.from_user.id), "")
    await message.answer(
        _("Please choose a subcategory:"),
        reply_markup=await get_submenu_keyboard("main-zema", user.get("language", "am"), _)
    )

@router.message(F.text.in_({"ኪነ ጥበብ", "Arts", "Aartii"}))
async def arts_menu_handler(message: Message, _: Callable):
    user = await get_user(str(message.from_user.id), "")
    await message.answer(
        _("Please choose a subcategory:"),
        reply_markup=await get_submenu_keyboard("main-arts", user.get("language", "am"), _)
    )

# The main navigation handler now only deals with inline buttons (sub-menus)
@router.callback_query(F.data.startswith("nav_"))
async def navigation_handler(callback_query: CallbackQuery, _: Callable):
    """Handles navigation through the inline sub-menu hierarchy."""
    category_id = callback_query.data.split("_")[1]
    user = await get_user(str(callback_query.from_user.id), "")
    lang = user.get("language", "am")

    if category_id == "main":
        await callback_query.message.edit_text(_("Main Menu"))
        return

    category = await get_category(category_id)
    if not category:
        await callback_query.answer(_("Category not found."), show_alert=True)
        return

    if category.get("is_end_category"):
        resources = await get_resources_by_category(category_id)
        if not resources:
            await callback_query.answer(_("There are no files in this category yet."), show_alert=True)
        else:
            await callback_query.message.edit_text(
                _("Files in this category:"),
                reply_markup=await get_resources_keyboard(resources, category.get("parent_id"), _),
            )
    else:
        await callback_query.message.edit_text(
            _("Please choose a subcategory:"),
            reply_markup=await get_submenu_keyboard(category_id, lang, _),
        )
    await callback_query.answer()
    
# Resource handler now fetches by document ID
@router.callback_query(F.data.startswith("res_"))
async def resource_handler(callback_query: CallbackQuery):
    """Sends the requested resource file to the user using its document ID."""
    resource_id = callback_query.data.split("_", 1)[1]
    resource = await get_resource_by_id(resource_id)
    
    if resource and "telegram_file_id" in resource:
        await callback_query.bot.send_document(
            callback_query.from_user.id,
            resource["telegram_file_id"],
            caption=resource.get("file_name")
        )
    else:
        await callback_query.answer("Error: File not found.", show_alert=True)
    await callback_query.answer()

@router.message(F.text.in_({"ስለ ገዳሜ እየሱስ", "About Gedame-Eyesus", "Waa'ee Gedame-Eyesus"}))
async def about_handler(message: Message, _: Callable):
    """Provides a detailed and well-formatted 'About' message."""
    about_text = (
        "📜 <b>ስለ ገዳመ ኢየሱስ (About Gedame Eyesus)</b> 📜\n\n"
        "<b>ተልዕኳችን (Our Mission):</b>\n"
        "የኢትዮጵያ ኦርቶዶክስ ተዋሕዶ ቤተ ክርስቲያን መንፈሳዊ እና ምሁራዊ ሀብቶችን በዲጂታል መልክ በማቅረብ ለትውልድ እንዲተላለፍ ማድረግ። የጥንት አባቶቻችንን ጥበብ ለዛሬው ትውልድ በቀላሉ ተደራሽ ማድረግ ነው።\n\n"
        "<i>To preserve and transmit the profound spiritual and intellectual heritage of the Ethiopian Orthodox Tewahedo Church. We strive to make the wisdom of our ancient fathers accessible to the modern world through this digital medium.</i>\n\n"
        "<b>ምን እናቀርባለን (What We Offer):</b>\n"
        "- የዜማ ትምህርቶች (Zema Lessons)\n"
        "- መንፈሳዊ መጻሕፍት (Spiritual Books)\n"
        "- ታሪካዊ ሰነዶች (Historical Texts)\n"
    )
    await message.answer(about_text, parse_mode="HTML")

# "Contact Us" now starts an FSM flow
@router.message(F.text.in_({"እኛን ያግኙን", "Contact Us", "Nu Qunnamaa"}))
async def contact_handler(message: Message, state: FSMContext, _: Callable):
    """Initiates the process for a user to send a message to the admin."""
    await message.answer(
        "🖋️ <b>ለአስተዳዳሪው መልዕክት ይላኩ (Send a Message to the Admin)</b>\n\n"
        "እባክዎ መልዕክትዎን፣ አስተያየትዎን ወይም ጥያቄዎን ከታች ያስፍሩ። መልዕክትዎ በቀጥታ ለአስተዳዳሪው ይላካል።\n\n"
        "<i>Please type your message, feedback, or question below. It will be forwarded directly to the administrator.</i>",
        parse_mode="HTML"
    )
    await state.set_state(Contact.waiting_for_message)

# Handler to process the user's message and forward it
@router.message(Contact.waiting_for_message)
async def process_contact_message(message: Message, state: FSMContext, bot: Bot, _: Callable):
    """Forwards the user's message to the admin and sends a confirmation."""
    admin_id = os.getenv("ADMIN_USER_ID")
    if not admin_id:
        print("ADMIN_USER_ID is not set in .env file.")
        await message.answer(_("Sorry, the contact service is currently unavailable."))
        await state.clear()
        return

    try:
        await bot.forward_message(
            chat_id=admin_id,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        await message.answer(
            "✅ <b>መልዕክትዎ ተልኳል (Message Sent)</b>\n\n"
            "አስተያየትዎ ስለደረሰን እናመሰግናለን። በቅርቡ ምላሽ እንሰጣለን።\n"
            "<i>Thank you for your feedback. We have received your message and will respond if necessary.</i>",
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Error forwarding message: {e}")
        await message.answer(_("Sorry, there was an error sending your message. Please try again later."))
    
    await state.clear()

# Language handlers also need to be message handlers now
@router.message(F.text.in_({"ቋንቋ ቀይር", "Change Language", "Afaan Jijjiiri"}))
async def language_change_handler(message: Message, _: Callable):
    await message.answer(
        _("Choose your language:"),
        reply_markup=get_language_keyboard()
    )

@router.callback_query(F.data.startswith("lang_"))
async def language_callback_handler(callback_query: CallbackQuery):
    """Handles language selection from the inline keyboard."""
    lang_code = callback_query.data.split("_")[1]
    user_id = str(callback_query.from_user.id)
    await update_user_language(user_id, lang_code)
    is_admin = await is_admin_db(user_id)
    
    temp_translator = lambda text: translations.get(lang_code, translations["am"]).get(text, text)

    await callback_query.message.delete() # Remove the inline language choice
    await callback_query.message.answer(
        temp_translator("Language updated."), 
        reply_markup=await get_main_menu_keyboard(is_admin, temp_translator)
    )
    await callback_query.answer()