from notion.client import NotionClient
from notion.collection import NotionDate
import pandas as pd

class Notion:
    def __init__(self, token: str, page: str):
        self.client = NotionClient(token_v2=token)
        self.page = self.client.get_collection_view(page)

    def get_collection(self):
        notion_data = []
        for task in self.page.collection.get_rows():
            notion_task = {
                "title": task.name,
                "status": task.status,
                "due": task.due.start if task.due else ""
            }
            notion_data.append(notion_task)

        return notion_data

    def create_record(self, name: str, status: str, due: str=None):
        row = self.page.collection.add_row()
        row.name = name
        row.status = status
        #row.due = task.to_notion

    def compare_record(self, name: str, status: str):
        pass