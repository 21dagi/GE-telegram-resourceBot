# Import the module itself, not the variable from within it
from database import firestore_service

async def seed_database():
    """Seeds the database with the initial category structure if it's empty."""
    # Access db through the module to get the initialized instance at runtime
    categories_ref = firestore_service.db.collection("categories")

    # Use .stream() and check if it has any documents
    docs = categories_ref.limit(1).stream()
    if any(docs):
        print("Database already seeded. Skipping.")
        return

    print("Seeding database...")

    categories = [
        # Main Menu
        {"id": "main-library", "name_am": "የመጻሕፍት ቤት", "name_en": "Library", "name_or": "Mana Kitaabaa", "parent_id": "main", "is_end_category": False},
        {"id": "main-zema", "name_am": "የዜማ ቤት", "name_en": "Zema House", "name_or": "Mana Zema", "parent_id": "main", "is_end_category": False},
        {"id": "main-arts", "name_am": "ኪነ ጥበብ", "name_en": "Arts", "name_or": "Aartii", "parent_id": "main", "is_end_category": False}, # Changed to be a parent

        # Library Submenus
        {"id": "library-grade1-12", "name_am": "1-12 ኮርሶች መጻሕፍት", "name_en": "Grade 1-12 Course Books", "name_or": "Kitaabota Barnootaa 1-12", "parent_id": "main-library", "is_end_category": False},
        {"id": "library-course-books", "name_am": "የኮርስ መጻሕፍት", "name_en": "Course Books", "name_or": "Kitaabota Koorsii", "parent_id": "main-library", "is_end_category": True},
        {"id": "library-abnet", "name_am": "የአብነት መማሪያ መጽሐፍት", "name_en": "Abnet Learning Books", "name_or": "Kitaabota Barumsa Abnet", "parent_id": "main-library", "is_end_category": False},
        {"id": "library-other-refs", "name_am": "ሌሎች ማጣቀሻዎች", "name_en": "Other References", "name_or": "Wabiilee Biraa", "parent_id": "main-library", "is_end_category": True},

        # Grades 1-12
        {"id": "grade-1", "name_am": "ክፍል 1", "name_en": "Grade 1", "name_or": "Kutaa 1", "parent_id": "library-grade1-12", "is_end_category": True},
        {"id": "grade-2", "name_am": "ክፍል 2", "name_en": "Grade 2", "name_or": "Kutaa 2", "parent_id": "library-grade1-12", "is_end_category": True},
        {"id": "grade-3", "name_am": "ክፍል 3", "name_en": "Grade 3", "name_or": "Kutaa 3", "parent_id": "library-grade1-12", "is_end_category": True},
        {"id": "grade-4", "name_am": "ክፍል 4", "name_en": "Grade 4", "name_or": "Kutaa 4", "parent_id": "library-grade1-12", "is_end_category": True},
        {"id": "grade-5", "name_am": "ክፍል 5", "name_en": "Grade 5", "name_or": "Kutaa 5", "parent_id": "library-grade1-12", "is_end_category": True},
        {"id": "grade-6", "name_am": "ክፍል 6", "name_en": "Grade 6", "name_or": "Kutaa 6", "parent_id": "library-grade1-12", "is_end_category": True},
        {"id": "grade-7", "name_am": "ክፍል 7", "name_en": "Grade 7", "name_or": "Kutaa 7", "parent_id": "library-grade1-12", "is_end_category": True},
        {"id": "grade-8", "name_am": "ክፍል 8", "name_en": "Grade 8", "name_or": "Kutaa 8", "parent_id": "library-grade1-12", "is_end_category": True},
        {"id": "grade-9", "name_am": "ክፍል 9", "name_en": "Grade 9", "name_or": "Kutaa 9", "parent_id": "library-grade1-12", "is_end_category": True},
        {"id": "grade-10", "name_am": "ክፍል 10", "name_en": "Grade 10", "name_or": "Kutaa 10", "parent_id": "library-grade1-12", "is_end_category": True},
        {"id": "grade-11", "name_am": "ክፍል 11", "name_en": "Grade 11", "name_or": "Kutaa 11", "parent_id": "library-grade1-12", "is_end_category": True},
        {"id": "grade-12", "name_am": "ክፍል 12", "name_en": "Grade 12", "name_or": "Kutaa 12", "parent_id": "library-grade1-12", "is_end_category": True},

        # Abnet
        {"id": "abnet-widase-maryam", "name_am": "ውዳሴ ማርያም", "name_en": "Widase Maryam", "name_or": "Widase Maryam", "parent_id": "library-abnet", "is_end_category": True},
        {"id": "abnet-opt2", "name_am": "abnetoption2", "name_en": "abnetoption2", "name_or": "abnetoption2", "parent_id": "library-abnet", "is_end_category": True},

        # Zema Submenus
        {"id": "zema-widase-maryam", "name_am": "ውዳሴ ማርያም ዜማ", "name_en": "Widase Maryam Zema", "name_or": "Zema Widase Maryam", "parent_id": "main-zema", "is_end_category": False},
        {"id": "zema-mahlete-tsige", "name_am": "ማህሌተ ጽጌ", "name_en": "Mahlete Tsige", "name_or": "Mahlete Tsige", "parent_id": "main-zema", "is_end_category": True},
        {"id": "zema-kidase-debre", "name_am": "ቅዳሴ ዘደብረ ዓባይ በጣዕመ ዜማ(ግዕዝ)", "name_en": "Kidase Zedebre Abay", "name_or": "Kidase Zedebre Abay", "parent_id": "main-zema", "is_end_category": True},
        {"id": "zema-mestegabie", "name_am": "መስተጋብዕ", "name_en": "Mestegabie", "name_or": "Mestegabie", "parent_id": "main-zema", "is_end_category": False},
        {"id": "zema-kidan-hours", "name_am": "ኪዳንና ሰዓታት", "name_en": "Kidan & Hours", "name_or": "Kidan fi Sa'atiiwwan", "parent_id": "main-zema", "is_end_category": False},
        {"id": "zema-kidase-word", "name_am": "የቅዳሴ ቃል ትምህርት", "name_en": "Kidase Word Lesson", "name_or": "Barnoota Jechaa Kidase", "parent_id": "main-zema", "is_end_category": False},

        # Widase Maryam Zema (Daily)
        {"id": "widase-mon", "name_am": "የሰኞ", "name_en": "Monday", "name_or": "Wixata", "parent_id": "zema-widase-maryam", "is_end_category": True},
        {"id": "widase-tue", "name_am": "የማክሰኞ", "name_en": "Tuesday", "name_or": "Kibxata", "parent_id": "zema-widase-maryam", "is_end_category": True},
        {"id": "widase-wed", "name_am": "የረቡዕ", "name_en": "Wednesday", "name_or": "Roobii", "parent_id": "zema-widase-maryam", "is_end_category": True},
        {"id": "widase-thu", "name_am": "የሐሙስ", "name_en": "Thursday", "name_or": "Kamisa", "parent_id": "zema-widase-maryam", "is_end_category": True},
        {"id": "widase-fri", "name_am": "የአርብ", "name_en": "Friday", "name_or": "Jimaata", "parent_id": "zema-widase-maryam", "is_end_category": True},
        {"id": "widase-sat", "name_am": "የቅዳሜ", "name_en": "Saturday", "name_or": "Sanbata", "parent_id": "zema-widase-maryam", "is_end_category": True},
        {"id": "widase-sun", "name_am": "የእሁድ", "name_en": "Sunday", "name_or": "Dilbata", "parent_id": "zema-widase-maryam", "is_end_category": True},

        # Kidan & Hours
        {"id": "liton", "name_am": "ሊጦን", "name_en": "Liton", "name_or": "Liton", "parent_id": "zema-kidan-hours", "is_end_category": True},
        {"id": "mestebkue", "name_am": "መስተብቊዕ", "name_en": "Mestebkue", "name_or": "Mestebkue", "parent_id": "zema-kidan-hours", "is_end_category": True},

        # Kidase Word Lesson
        {"id": "kidan-geez-zema", "name_am": "ኪዳን በግዕዝ ዜማ", "name_en": "Kidan in Geez Zema", "name_or": "Kidan Zema Geez", "parent_id": "zema-kidase-word", "is_end_category": True},
        {"id": "liton-araray-zema", "name_am": "ሊጦን አራራይ ዜማ", "name_en": "Liton Araray Zema", "name_or": "Liton Araray Zema", "parent_id": "zema-kidase-word", "is_end_category": True},

        # Arts (End Categories)
        {"id": "arts-book1", "name_am": "Book1", "name_en": "Book1", "name_or": "Book1", "parent_id": "main-arts", "is_end_category": True},
        {"id": "arts-book2", "name_am": "Book2", "name_en": "Book2", "name_or": "Book2", "parent_id": "main-arts", "is_end_category": True},
        {"id": "arts-book3", "name_am": "Book3", "name_en": "Book3", "name_or": "Book3", "parent_id": "main-arts", "is_end_category": True},
    ]

    for category in categories:
        # Use the explicit ID for the document
        categories_ref.document(category["id"]).set({
            "name_am": category["name_am"],
            "name_en": category["name_en"],
            "name_or": category["name_or"],
            "parent_id": category["parent_id"],
            "is_end_category": category["is_end_category"],
        })
    print("Database seeding complete.")