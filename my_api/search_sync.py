"""
Defines a task to run and constantly refresh the search index.

Thank you to: https://github.com/tiangolo/fastapi/issues/2713
"""
import asyncio
from my_api.database import SEARCH_SYNCER_DELAY_SECONDS

class BackgroundSearchSyncer:
    def __init__(self):
        self.value = 0
        self.running = True

    async def run_main(self):
        while self.running:
            await asyncio.sleep(SEARCH_SYNCER_DELAY_SECONDS)
            self.value += 1
        print("DONE!!!")
