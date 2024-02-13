"""
Defines a task to run and constantly refresh the search index.

Thank you to: https://github.com/tiangolo/fastapi/issues/2713
"""
import os
import asyncio
import datetime
from meilisearch import Client
from my_api.database import SEARCH_SYNCER_DELAY_SECONDS, SEARCH_INDEX_NAME, SessionLocal
from my_api import crud
from my_api.schemas import post_serializer


class BackgroundSearchSyncer:
    def __init__(self):
        self.value = 0
        self.running = True
        self.updated_at = None
        self.client = Client(url=os.environ.get("SEARCH_INDEX_URL"), 
                            api_key=os.environ.get("SEARCH_INDEX_KEY")
                        )


    async def run_main(self):
        """
        Run the syncing process. If no index exists, create one.
        """
        indices = self.client.get_indexes().keys()
        if SEARCH_INDEX_NAME not in indices:
            self.client.create_index(SEARCH_INDEX_NAME)

        while self.running:
            await asyncio.sleep(SEARCH_SYNCER_DELAY_SECONDS)
            """
            Process to sync:
            1. Get index "updated_at" timestamp
            2. Select all posts with date_modified > time updated
            3. bulk insert
            """
            self.updated_at = self.client.index(uid=SEARCH_INDEX_NAME).fetch_info().updated_at
            self.value += 1

            db = SessionLocal()
            posts_past_time = crud.get_all_posts_past_time(db, self.updated_at)
            if not posts_past_time:
                continue
            posts_to_index = [post_serializer.validate_python(post).model_dump() for post in posts_past_time]
            print("posts ", posts_to_index)
            self.client.index(SEARCH_INDEX_NAME).add_documents(posts_to_index)
            db.close()
