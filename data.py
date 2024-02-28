import config
import os
import pandas as pd
import requests


def call_api(url="/dataset/nurses-workplace-priorities-development-sandbox/node/argument_extraction_1"):
    headers = {
        "Authorization": f"Bearer {os.environ.get('TTTC_TURBO_TOKEN')}"
    }
    get = lambda url: requests.get(f"{config.BASE_URL}{url}", headers=headers).json()
    response = get(url)
    return response


def create_df(response):

    data = []
    for id, output in response["data"]["output"].items():
        for claim in output["claims"]:
            row = {
                # "id": id,
                # "interviewee": output["interview"],
                "interviewee": id,
                "topic": claim["topicName"] + " - " + (claim["subtopicName"] or "None"),
                "claim": claim["claim"],
                "quote": claim["quote"]
            }
            data.append(row)

    df = pd.DataFrame(data)
    return df
