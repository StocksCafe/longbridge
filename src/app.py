import os
from pathlib import Path
from src.longbridge_utils import parse_orders_history

from dotenv import load_dotenv, set_key, get_key, find_dotenv
from litestar import Litestar, get, post, Request
from litestar.static_files import create_static_files_router
from litestar.response import Template
from litestar.template.config import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine

# Use following template
# https://github.com/app-generator/flask-atlantis-dark/blob/master/apps/templates/home/index.html
# https://flask-atlantis-dark.appseed-srv1.com/index

def _load_settings():
    default_value = "Please Update"
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    stockscafe_user_id = get_key(key_to_get="STOCKSCAFE_USER_ID", dotenv_path=dotenv_path) or default_value
    stockscafe_label_id = get_key(key_to_get="STOCKSCAFE_LABEL_ID", dotenv_path=dotenv_path) or default_value
    stockscafe_sync_api_key = get_key(key_to_get="STOCKSCAFE_SYNC_API_KEY", dotenv_path=dotenv_path) or default_value
    longport_app_key = get_key(key_to_get="LONGPORT_APP_KEY", dotenv_path=dotenv_path) or default_value
    longport_app_secret = get_key(key_to_get="LONGPORT_APP_SECRET", dotenv_path=dotenv_path) or default_value
    longport_access_token = get_key(key_to_get="LONGPORT_ACCESS_TOKEN", dotenv_path=dotenv_path) or default_value
    # read from .env and update os
    os.environ["STOCKSCAFE_USER_ID"] = stockscafe_user_id
    os.environ["STOCKSCAFE_LABEL_ID"] = stockscafe_label_id
    os.environ["STOCKSCAFE_SYNC_API_KEY"] = stockscafe_sync_api_key
    os.environ["LONGPORT_APP_KEY"] = longport_app_key
    os.environ["LONGPORT_APP_SECRET"] = longport_app_secret
    os.environ["LONGPORT_ACCESS_TOKEN"] = longport_access_token

@get("/")
async def main() -> Template:
    try:
        _load_settings()
        return Template("index.html", context={
            "name": "Evan",
            "stockscafe_user_id": os.environ["STOCKSCAFE_USER_ID"],
            "stockscafe_label_id": os.environ["STOCKSCAFE_LABEL_ID"],
            "stockscafe_sync_api_key": os.environ["STOCKSCAFE_SYNC_API_KEY"],
            "longport_app_key": os.environ["LONGPORT_APP_KEY"],
            "longport_app_secret": os.environ["LONGPORT_APP_SECRET"],
            "longport_access_token": os.environ["LONGPORT_ACCESS_TOKEN"]
        })
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@post("/sync-longbridge")
async def sync_longbridge(request: Request) -> dict:
    # When "Sync LongBridge Data" button is clicked
    try:
        form_data = await request.json()
        _save_settings(form_data)
        return {"message": parse_orders_history()}
    except Exception as e:
        return {"message": f"Error occurred: {str(e)}", "status_code": 500} 

def _save_settings(form_data):
    # Retrieve the values from the form submission
        stockscafe_user_id = form_data.get('stockscafe_user_id')
        stockscafe_label_id = form_data.get('stockscafe_label_id')
        stockscafe_sync_api_key = form_data.get('stockscafe_sync_api_key')
        longport_app_key = form_data.get('longport_app_key')
        longport_app_secret = form_data.get('longport_app_secret')
        longport_access_token = form_data.get('longport_access_token')
        # Find the .env file path
        dotenv_path = find_dotenv()

        if not dotenv_path:
            return {"message": "Could not find .env file", "success": False}

        # Set the new values in the .env file
        set_key(dotenv_path, "STOCKSCAFE_USER_ID", stockscafe_user_id)
        set_key(dotenv_path, "STOCKSCAFE_LABEL_ID", stockscafe_label_id)
        set_key(dotenv_path, "STOCKSCAFE_SYNC_API_KEY", stockscafe_sync_api_key)
        set_key(dotenv_path, "LONGPORT_APP_KEY", longport_app_key)
        set_key(dotenv_path, "LONGPORT_APP_SECRET", longport_app_secret)
        set_key(dotenv_path, "LONGPORT_ACCESS_TOKEN", longport_access_token)
        # set the new values in os
        os.environ["STOCKSCAFE_USER_ID"] = stockscafe_user_id
        os.environ["STOCKSCAFE_LABEL_ID"] = stockscafe_label_id
        os.environ["STOCKSCAFE_SYNC_API_KEY"] = stockscafe_sync_api_key
        os.environ["LONGPORT_APP_KEY"] = longport_app_key
        os.environ["LONGPORT_APP_SECRET"] = longport_app_secret
        os.environ["LONGPORT_ACCESS_TOKEN"] = longport_access_token

@post("/save-settings")
async def save_settings(request: Request) -> dict:
    try:
        form_data = await request.json()
        _save_settings(form_data)
        return {"message": "Settings saved successfully!", "success": True}
    except Exception as e:
        return {"message": f"An error occurred while saving settings: {str(e)}", "success": False}

app = Litestar(
    route_handlers=[
        create_static_files_router(path="/static", directories=["static"]), # /static is available on /static
        main, sync_longbridge, save_settings],
    template_config=TemplateConfig(
        directory=Path("templates"),
        engine=JinjaTemplateEngine,
    ),
)

# Run the Litestar app
if __name__ == "__main__":
    app.run(host='0.0.0.0')