import os
import requests

sync_url = "https://api.stocks.cafe/sync.json"
def push_data(order_id, body) -> str:
    try:
        user_id = os.getenv("STOCKSCAFE_USER_ID")
        api_key = os.getenv("STOCKSCAFE_SYNC_API_KEY")
        data = {
            "sync_api_user": user_id, 
            "sync_api_key": api_key,
            "longbridge_id": str(order_id),
            "type": str(3),
            "body": body
        }
        response = requests.post(sync_url + "?l=longbridge", json=data)
        print(f"Successfully inserted {order_id}")
        print(response.json())
        return str(response.json())
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Failed"

def process_data() -> str:
    try:
        data = {
            "sync_api_user": os.getenv("STOCKSCAFE_USER_ID"), 
            "sync_api_label_id": os.getenv("STOCKSCAFE_LABEL_ID"),
            "sync_api_key": str(os.getenv("STOCKSCAFE_SYNC_API_KEY")),
        }
        response = requests.post(sync_url + "?l=process_longbridge", json=data)
        print(f"Successfully processed longbridge")
        print(response.json())
        return str(response.json())
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Failed"