import os
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

db = None

def setup_firestore():
    """Initializes the Firestore client."""
    global db
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase_credentials.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()

async def get_user(user_id: str, username: str):
    """Retrieves or creates a user in the database."""
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()
    if not user_doc.exists:
        is_initial_admin = user_id == os.getenv("ADMIN_USER_ID")
        user_data = {
            "is_admin": is_initial_admin,
            "username": username,
            "language": "am",
            "join_date": datetime.utcnow(),
            "is_banned": False,
        }
        user_ref.set(user_data)
        return user_data
    return user_doc.to_dict()

async def get_all_users():
    """Retrieves all users from the database."""
    users_ref = db.collection("users")
    return [{"id": doc.id, **doc.to_dict()} for doc in users_ref.stream()]

async def toggle_admin_status(user_id: str):
    """Flips the is_admin boolean for a given user ID."""
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        current_status = user_doc.to_dict().get("is_admin", False)
        user_ref.update({"is_admin": not current_status})
        return not current_status
    return None

async def toggle_ban_status(user_id: str):
    """Flips the is_banned boolean for a given user ID."""
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        current_status = user_doc.to_dict().get("is_banned", False)
        user_ref.update({"is_banned": not current_status})
        return not current_status
    return None

async def update_user_language(user_id: str, language: str):
    """Updates the user's preferred language."""
    db.collection("users").document(user_id).update({"language": language})

async def is_admin(user_id: str) -> bool:
    """Checks if a user is an admin."""
    user = await get_user(user_id, "")
    return user.get("is_admin", False)

async def get_category(category_id: str):
    """Retrieves a category by its ID."""
    if not category_id: return None
    category = db.collection("categories").document(category_id).get()
    if category.exists:
        cat_data = category.to_dict()
        cat_data['id'] = category.id
        return cat_data
    return None

async def get_categories_by_parent(parent_id: str):
    """Retrieves subcategories for a given parent ID."""
    categories_ref = db.collection("categories").where("parent_id", "==", parent_id)
    docs = categories_ref.stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]

async def get_end_categories():
    """Retrieves all categories that are marked as end categories."""
    categories_ref = db.collection("categories").where("is_end_category", "==", True)
    docs = categories_ref.stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]

async def add_resource(category_id, file_name, telegram_file_id, uploaded_by, mime_type, size):
    """Adds a new resource to the database."""
    db.collection("resources").add({
        "category_id": category_id,
        "file_name": file_name,
        "telegram_file_id": telegram_file_id,
        "upload_date": datetime.utcnow(),
        "uploaded_by": uploaded_by,
        "mime_type": mime_type,
        "size": size,
    })

async def get_resources_by_category(category_id: str):
    """Retrieves resources for a given category, including their document IDs."""
    resources_ref = db.collection("resources").where("category_id", "==", category_id)
    return [{"id": doc.id, **doc.to_dict()} for doc in resources_ref.stream()]

async def get_resource_by_id(resource_id: str):
    """Retrievels a single resource by its unique document ID."""
    resource_doc = db.collection("resources").document(resource_id).get()
    return resource_doc.to_dict() if resource_doc.exists else None

async def get_all_resources():
    """Retrieves all resources from the database for in-app searching."""
    resources_ref = db.collection("resources")
    return [{"id": doc.id, **doc.to_dict()} for doc in resources_ref.stream()]