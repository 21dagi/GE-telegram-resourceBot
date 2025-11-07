from aiogram.fsm.state import State, StatesGroup

class UploadFile(StatesGroup):
    """Defines the states for the file upload process."""
    waiting_for_category_id = State()
    waiting_for_file = State()

class Contact(StatesGroup):
    """Defines the state for the contact form."""
    waiting_for_message = State()

class ManageUsers(StatesGroup):
    """Defines states for admin user management."""
    waiting_for_user_id_to_toggle_admin = State()
    waiting_for_user_id_to_ban = State()

# NEW: States for the search feature
class Search(StatesGroup):
    waiting_for_query = State()