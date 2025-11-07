from typing import Any, Dict, Callable, Optional
from aiogram import Dispatcher
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject, User
from database.firestore_service import get_user

# Expanded translations for a better user experience
translations = {
    "en": {
        "Welcome!": "Welcome to the Gedam-Eyesus Academic Resource Bot!",
        "Main Menu": "Main Menu",
        "የመጻሕፍት ቤት": "Library",
        "የዜማ ቤት": "Zema House",
        "ኪነ ጥበብ": "Arts",
        "ስለ ገዳሜ እየሱስ": "About Gedame-Eyesus",
        "እኛን ያግኙን": "Contact Us",
        "ቋንቋ ቀይር": "Change Language",
        "ፋይሎችን አስገባ": "Upload Files",
        "ተጠቃሚዎችን ያስተዳድሩ": "Manage Users",
        "Choose your language:": "Choose your language:",
        "Language updated.": "Language updated.",
        "Please choose a subcategory:": "Please choose a subcategory:",
        "Files in this category:": "Files in this category:",
        "Category not found.": "Category not found.",
        "You are not an admin.": "You do not have permission for this action.",
        "Please enter the category ID for the file you want to upload:": "Please enter the category ID for the file you want to upload:",
        "Invalid Category ID. Please try again.": "Invalid Category ID. Please try again.",
        "Now, please send the file.": "Now, please send the file.",
        "An error occurred. Please start the upload process again.": "An error occurred. Please start the upload process again.",
        "File uploaded successfully!": "File uploaded successfully!",
        "ተመለስ": "Back",
        "Search 🔎": "Search 🔎",
"Please enter what you are looking for...": "Please enter what you are looking for...",
"Search Results:": "Search Results:",
"No results found for your query.": "No results found for your query.",
"Close Search": "Close Search",
    },
    "am": {
        "Welcome!": "እንኳን ወደ ገዳመ ኢየሱስ የአካዳሚክ ሪሶርስ ቦት በደህና መጡ!",
        "Main Menu": "ዋና ማውጫ",
        "የመጻሕፍት ቤት": "የመጻሕፍት ቤት",
        "የዜማ ቤት": "የዜማ ቤት",
        "ኪነ ጥበብ": "ኪነ ጥበብ",
        "ስለ ገዳሜ እየሱስ": "ስለ ገዳሜ እየሱስ",
        "እኛን ያግኙን": "እኛን ያግኙን",
        "ቋንቋ ቀይር": "ቋንቋ ቀይር",
        "ፋይሎችን አስገባ": "ፋይሎችን አስገባ",
        "ተጠቃሚዎችን ያስተዳድሩ": "ተጠቃሚዎችን ያስተዳድሩ",
        "Choose your language:": "ቋንቋ ይምረጡ:",
        "Language updated.": "ቋንቋ ተቀይሯል።",
        "Please choose a subcategory:": "እባክዎ ንዑስ ምድብ ይምረጡ:",
        "Files in this category:": "በዚህ ምድብ ውስጥ ያሉ ፋይሎች፡",
        "Category not found.": "ምድቡ አልተገኘም።",
        "You are not an admin.": "ይህንን ለማድረግ ፈቃድ የለዎትም።",
        "Please enter the category ID for the file you want to upload:": "እባክዎ የሚልኩትን ፋይል ምድብ ID ያስገቡ:",
        "Invalid Category ID. Please try again.": "የማያገለግል የምድብ ID ነው። እባክዎ እንደገና ይሞክሩ።",
        "Now, please send the file.": "አሁን እባክዎ ፋይሉን ይላኩ።",
        "An error occurred. Please start the upload process again.": "ስህተት አጋጥሟል። እባክዎ የማስገባት ሂደቱን እንደገና ይጀምሩ።",
        "File uploaded successfully!": "ፋይሉ በተሳካ ሁኔታ ተልኳል!",
        "ተመለስ": "ተመለስ",
        "Search 🔎": "ፈልግ 🔎",
"Please enter what you are looking for...": "እባክዎ የሚፈልጉትን ያስገቡ...",
"Search Results:": "የፍለጋ ውጤቶች:",
"No results found for your query.": "ለጥያቄዎ ምንም ውጤቶች አልተገኙም።",
"Close Search": "ፍለጋ ዝጋ",
    },
    "or": {
        "Welcome!": "Baga Nagaan Gara Boottii Qabeenyaa Akkaadaamii Gedam-Eyesus Dhuftan!",
        "Main Menu": "Baafata Guddaa",
        "የመጻሕፍት ቤት": "Mana Kitaabaa",
        "የዜማ ቤት": "Mana Zema",
        "ኪነ ጥበብ": "Aartii",
        "ስለ ገዳሜ እየሱስ": "Waa'ee Gedame-Eyesus",
        "እኛን ያግኙን": "Nu Qunnamaa",
        "ቋንቋ ቀይር": "Afaan Jijjiiri",
        "ፋይሎችን አስገባ": "Faayiloota Olkaa'i",
        "ተጠቃሚዎችን ያስተዳድሩ": "Fayyadamaa Bulchi",
        "Choose your language:": "Afaan keessan filadhaa:",
        "Language updated.": "Afaan jijjiirameera.",
        "Please choose a subcategory:": "Mee ramaddii xiqqaa filadhaa:",
        "Files in this category:": "Faayiloonni ramaddii kana keessa jiran:",
        "Category not found.": "Ramaddiin hin argamne.",
        "You are not an admin.": "Kana gochuuf hayyama hin qabdu.",
        "Please enter the category ID for the file you want to upload:": "Mee ID garee faayilii olkaa\'uu barbaaddu galchi:",
        "Invalid Category ID. Please try again.": "ID garee sirrii miti. Irra deebi\'ii yaali.",
        "Now, please send the file.": "Amma, mee faayilicha ergi.",
        "An error occurred. Please start the upload process again.": "Dogoggorri tokko uumameera. Adeemsa olkaa\'uu irra deebi\'ii jalqabi.",
        "File uploaded successfully!": "Faayiliin milkaa\'inaan olkaa\'ameera!",
        "ተመለስ": "Deebi'i",
        "Search 🔎": "Barbaadi 🔎",
"Please enter what you are looking for...": "Mee waan barbaaddan galchaa...",
"Search Results:": "Bu'aa Barbaachaa:",
"No results found for your query.": "Wanti gaafatte hin argamne.",
"Close Search": "Barbaacha Cufi",
    },
}

class LanguageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Any],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        # Safely get the user object from any event type
        user: Optional[User] = data.get("event_from_user")

        # If there's no user, we can't determine the language, so we'll default to Amharic.
        if not user:
            data["_"] = lambda text: translations["am"].get(text, text)
            return await handler(event, data)
        
        # If there is a user, get their language from the database
        db_user = await get_user(str(user.id), user.username)
        lang = db_user.get("language", "am")
        
        # Create a translator function that already knows the user's language
        data["_"] = lambda text: translations.get(lang, translations["am"]).get(text, text)
        return await handler(event, data)

def setup_middleware(dp: Dispatcher):
    """Sets up the language middleware."""
    dp.update.middleware(LanguageMiddleware())