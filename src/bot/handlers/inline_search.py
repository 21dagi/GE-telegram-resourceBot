import uuid
from aiogram import F, Router
# MODIFICATION: Import the correct class for cached documents
from aiogram.types import InlineQuery, InlineQueryResultCachedDocument
from database.firestore_service import get_all_resources

router = Router()

@router.inline_query()
async def inline_search_handler(inline_query: InlineQuery):
    """Handles inline search queries from any chat."""
    query = inline_query.query.lower().strip()

    if not query:
        await inline_query.answer([], cache_time=1)
        return

    all_resources = await get_all_resources()
    results = [
        res for res in all_resources
        if query in res.get('file_name', '').lower()
    ]

    inline_results = []
    # Limit the number of results to 50, which is Telegram's maximum.
    for res in results[:50]:
        result_id = str(uuid.uuid4())
        
        # MODIFICATION: Use InlineQueryResultCachedDocument instead
        inline_results.append(
            InlineQueryResultCachedDocument(
                id=result_id,
                title=res['file_name'],
                # This field is now correctly named for a cached document
                document_file_id=res['telegram_file_id'],
                description=f"Category: {res.get('category_id')}"
            )
        )
    
    await inline_query.answer(inline_results, cache_time=1, is_personal=True)