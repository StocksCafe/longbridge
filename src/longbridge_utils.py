import re
import ast
import hashlib
from src.stockscafe_utils import push_data, process_data
from longport.openapi import TradeContext, Config, OrderStatus
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_cash_flow() -> str: # get and push
    try:
        config = Config.from_env()
        ctx = TradeContext(config)    
        now = datetime.now()
        resp = ctx.cash_flow(
            start_at = now - relativedelta(years=20),
            end_at = now,
        )
        raw_data = str(resp)
        records = re.findall(r'CashFlow\s*\{(.*?)\}', raw_data)
        for record in records:
            # Use regex to find the business_time field
            match = re.search(r'business_time:\s*"([^"]+)"', record)
            if match:
                business_time = match.group(1)
                name_match = re.search(r'transaction_flow_name:\s*"([^"]+)"', record)
                name = name_match.group(1)
                # Parse the timestamp
                dt = datetime.strptime(business_time, "%Y-%m-%dT%H:%M:%SZ")
                body = "CashFlow {" + record + "}"
                # Reformat it to the desired format
                formatted_timestamp = dt.strftime("%Y%m%d%H%M%S")
                baseLine = 1000000000000000 # (15 digits)
                hash_value = abs(int(hashlib.md5(name.encode()).hexdigest(), 16) % baseLine)
                order_id = int(formatted_timestamp) + hash_value
                print(str(order_id) + " -> " + str(body))
                push_data(order_id, body, type = 4)
            else:
                print("business_time not found.")
        return str("Test")
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}"
    
def get_orders_history(ctx) -> str:
    try:
        now = datetime.now()
        resp = ctx.history_orders(
            status = [OrderStatus.Filled],
            start_at = now - relativedelta(years=20),
            end_at = now,
        )
        return str(resp)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def parse_orders_history() -> str:
    try:
        config = Config.from_env()
        ctx = TradeContext(config)
        # cash flow data - pull from longbridge and push to StocksCafe 
        get_cash_flow()
        data = get_orders_history(ctx)
        print("===== Order History START =====")
        print(data)
        print("===== Order History END =====")
        if data:
            order_ids = re.findall(r'order_id:\s*"(\d+)"', data)
            # Insert orders into DB
            for order_id in order_ids:
                details = order_details(ctx, order_id)
                response = push_data(order_id, details)
                response_dict = ast.literal_eval(response)
                if not response_dict['result_boolean']:
                    return f"Error: {response_dict['result']}"
        else:
            return "Unable to pull orders history from LongBridge. Maybe no orders yet?"
        # Process orders
        response = process_data()
        response_dict = ast.literal_eval(response)
        if not response_dict['result_boolean']:
            return f"Error: {response_dict['result']}"
        return "Successfully pulled and processed orders from LongBridge"
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"Error = {e} - Unable to pull orders history from LongBridge"

def order_details(ctx, order_id) -> str:
    try:
        resp = ctx.order_detail(
            order_id = order_id,
        )
        return str(resp)
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"Error Thrown - Unable to pull orders details ({order_id}) from LongBridge"