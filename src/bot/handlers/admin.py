from typing import Callable
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import StateFilter

from bot.states import UploadFile, ManageUsers
from database.firestore_service import (
    get_end_categories,
    add_resource,
    is_admin as is_admin_db,
    get_user,
    get_all_users,
    toggle_admin_status,
    toggle_ban_status,
)

router = Router()

# --- File Upload Flow (Existing code, slightly modified for i18n) ---
@router.message(F.text.in_({"ፋይሎችን አስገባ", "Upload Files", "Faayiloota Olkaa'i"}))
async def upload_files_start_msg(message: Message, state: FSMContext, _: Callable):
    if not await is_admin_db(str(message.from_user.id)): return
    # This handler is triggered by the ReplyKeyboard, now we call the FSM logic
    await upload_files_start(message, state, _)

async def upload_files_start(message: Message, state: FSMContext, _: Callable):
    end_categories = await get_end_categories()
    user = await get_user(str(message.from_user.id), "")
    lang = user.get("language", "am")
    lang_key = f"name_{lang}"
    
    categories_text = "\n".join(
        [f"`{cat['id']}` - {cat.get(lang_key, cat.get('name_am'))}" for cat in end_categories]
    )
    
    await message.answer(
        _("Please enter the category ID for the file you want to upload:") + f"\n\n{categories_text}",
        parse_mode="Markdown"
    )
    await state.set_state(UploadFile.waiting_for_category_id)
def get_manage_users_keyboard(_: Callable) -> InlineKeyboardMarkup:
    """Creates the inline keyboard for the user management section."""
    buttons = [
        [InlineKeyboardButton(text=_("List All Users"), callback_data="admin_list_users")],
        [InlineKeyboardButton(text=_("Promote/Demote Admin"), callback_data="admin_toggle_admin_start")],
        [InlineKeyboardButton(text=_("Ban/Unban User"), callback_data="admin_ban_user_start")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
@router.message(F.text.in_({"ተጠቃሚዎችን ያስተዳድሩ", "Manage Users", "Fayyadamaa Bulchi"}))
async def manage_users_start(message: Message, _: Callable):
    """Displays the admin user management menu."""
    if not await is_admin_db(str(message.from_user.id)):
        return
    await message.answer(_("User Management Panel"), reply_markup=get_manage_users_keyboard(_))

@router.callback_query(F.data == "admin_list_users")
async def list_users_handler(callback_query: CallbackQuery, _: Callable):
    """Lists all users in the database."""
    users = await get_all_users()
    if not users:
        await callback_query.message.edit_text(_("No users found."))
        return
    
    user_list_text = "<b>📜 User List 📜</b>\n\n"
    for user in users:
        status = "✅ Admin" if user.get('is_admin') else "👤 User"
        if user.get('is_banned'): status = "🚫 Banned"
        user_list_text += f"<b>ID:</b> `{user.get('id')}`\n<b>Name:</b> {user.get('username', 'N/A')}\n<b>Status:</b> {status}\n\n"

    # For long lists, consider pagination. For now, send as one message.
    await callback_query.message.edit_text(user_list_text, parse_mode="HTML")
    await callback_query.answer()

@router.callback_query(F.data == "admin_toggle_admin_start")
async def toggle_admin_start(callback_query: CallbackQuery, state: FSMContext, _: Callable):
    """Starts the process of toggling a user's admin status."""
    await callback_query.message.edit_text(_("Enter the User ID to promote or demote:"))
    await state.set_state(ManageUsers.waiting_for_user_id_to_toggle_admin)
    await callback_query.answer()

@router.message(ManageUsers.waiting_for_user_id_to_toggle_admin)
async def process_toggle_admin(message: Message, state: FSMContext, _: Callable):
    """Processes the user ID and toggles admin status."""
    user_id = message.text.strip()
    new_status = await toggle_admin_status(user_id)
    
    if new_status is None:
        await message.answer(_("User ID not found. Please try again."))
    else:
        status_text = "promoted to Admin" if new_status else "demoted to User"
        await message.answer(_("Success! User {user_id} has been {status_text}.").format(user_id=user_id, status_text=status_text))
    
    await state.clear()
    await message.answer(_("User Management Panel"), reply_markup=get_manage_users_keyboard(_))
@router.message(UploadFile.waiting_for_category_id)
async def process_category_id(message: Message, state: FSMContext, _: Callable):
    """Processes the category ID provided by the admin."""
    # Basic validation: check if it's an end category
    category_id = message.text.strip()
    end_categories = await get_end_categories()
    if category_id not in [cat['id'] for cat in end_categories]:
        await message.answer(_("Invalid Category ID. Please try again."))
        return

    await state.update_data(category_id=category_id)
    await message.answer(_("Now, please send the file."))
    await state.set_state(UploadFile.waiting_for_file)

@router.message(UploadFile.waiting_for_file, F.document)
async def process_file_upload(message: Message, state: FSMContext, _: Callable):
    """Handles the uploaded file and saves it to Firestore."""
    data = await state.get_data()
    category_id = data.get("category_id")

    if not category_id:
        await message.answer(_("An error occurred. Please start the upload process again."))
        await state.clear()
        return

    file_id = message.document.file_id
    file_name = message.document.file_name
    mime_type = message.document.mime_type
    file_size = message.document.file_size

    await add_resource(
        category_id,
        file_name,
        file_id,
        str(message.from_user.id),
        mime_type,
        file_size,
    )

    await message.answer(_("File uploaded successfully!"))
    await state.clear()

# Need to import get_user for the language logic
from database.firestore_service import get_user