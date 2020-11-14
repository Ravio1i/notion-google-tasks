import json
#import logging
#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

import pandas as pd

from Google import GoogleTasksService
from Notion import Notion

GOOGLE_CREDENTIAL_FILE = 'google_credentials.json'
NOTION_CONFIG_FILE = 'notion_config.json'
TASKLIST = "tasks"

def main():
    # GOOGLE
    # ==================================================
    gts = GoogleTasksService(GOOGLE_CREDENTIAL_FILE)
    tasklists = gts.list_tasklists()
    for tasklist in tasklists:
        if tasklist["title"] != TASKLIST:
            continue

        tasks = gts.list_tasks(tasklist["id"], showCompleted=True)
        df_gtasks = pd.DataFrame(tasks).drop(columns=['kind', 'id', 'etag', 'selfLink', 'position'])
        print(df_gtasks)

    # NOTION
    # ==================================================
    with open(NOTION_CONFIG_FILE) as json_file: 
        notion_config = json.load(json_file) 

    notion = Notion(token=notion_config['token'], page=notion_config['page'])
    #notion_data = notion.page.collection
    notion_data = notion.get_collection()
    df_notion = pd.DataFrame(notion_data)
    # print(df_notion)

    # CREATE TASK IN NOTION
    # ==================================================
    for _, task in df_gtasks.iterrows():
        task_status = task.status if task.status == "Done" else "Backlog"

        if (df_notion.title == task.title).any():
            #logging.info("Google Task: {} exists in Notion".format(task.title))
            print(task.title)
            df_notion.title


            result = notion.page.build_query(filter=filter_param).execute()

            print(result)
            # notion.compare_record(
            #     name = task.title,
            #     status = task_status
            # )

            continue

        # CREATE TASK
        # notion.create_record(
        #     name = task.title,
        #     status = task_status
        # )


if __name__ == "__main__":
    main()
