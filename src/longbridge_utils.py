import re
import ast
from src.stockscafe_utils import push_data, process_data
from longport.openapi import TradeContext, Config, OrderStatus

def get_orders_history(ctx) -> str:
    try:
        resp = ctx.history_orders(status = [OrderStatus.Filled])
        return str(resp)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def parse_orders_history() -> str:
    try:
        config = Config.from_env()
        ctx = TradeContext(config)
        data = get_orders_history(ctx)
        if data:
            order_ids = re.findall(r'order_id:\s*"(\d+)"', data)
            # Insert orders into DB
            for order_id in order_ids:
                details = order_details(ctx, order_id)
                response = push_data(order_id, details)
                response_dict = ast.literal_eval(response)
                if not response_dict['result_boolean']:
                    return f"Error: {response_dict['result']}"
            # Process orders
            response = process_data()
            response_dict = ast.literal_eval(response)
            if not response_dict['result_boolean']:
                    return f"Error: {response_dict['result']}"
            return "Successfully pulled and processed orders from LongBridge"
        else:
            return "Error Thrown - Unable to pull orders history from LongBridge"
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