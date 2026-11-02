from app.mock import get
def test_products(): assert get("products")[0]["id"]=="SKU-1001"
def test_order_parent_child(): 
    x=get("orders")[0]; assert x["parent"]["customer_id"]=="cust01"; assert x["children"]["entries"]
