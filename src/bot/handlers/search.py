from typing import Callable
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.states import Search
from bot.keyboards import get_search_results_keyboard
# MODIFICATION: Import the new database function
from database.firestore_service import get_all_resources

router = Router()

@router.message(F.text.in_({"ፈልግ 🔎", "Search 🔎", "Barbaadi 🔎"}))
async def start_search_handler(message: Message, state: FSMContext, _: Callable):
    """Handles the press of the 'Search' button and prompts for a query."""
    await message.answer(_("Please enter what you are looking for..."))
    await state.set_state(Search.waiting_for_query)

@router.message(Search.waiting_for_query)
async def process_search_query_handler(message: Message, state: FSMContext, _: Callable):
    """
    Processes the user's text query with a case-insensitive "contains" search
    and returns the results.
    """
    # 1. Get the user's query and make it lowercase for case-insensitive matching.
    query = message.text.lower().strip()
    
    # 2. Fetch ALL resources from the database.
    all_resources = await get_all_resources()
    
    await state.clear() # Clear state immediately.

    # 3. Filter the resources in Python. This is the core of the new search engine.
    # It checks if the lowercase query string is present in the lowercase file name.
    results = [
        res for res in all_resources 
        if query in res.get('file_name', '').lower()
    ]

    if not results:
        await message.answer(_("No results found for your query."))
        return

    # Limit the number of results to show to avoid spamming the user.
    MAX_RESULTS = 25
    await message.answer(
        _("Search Results:"),
        reply_markup=get_search_results_keyboard(results[:MAX_RESULTS], _)
    )

@router.callback_query(F.data == "close_search")
async def close_search_handler(callback_query: CallbackQuery):
    """Handles the 'Close Search' button press, deleting the results message."""
    await callback_query.message.delete()
    await callback_query.answer()