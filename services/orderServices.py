from sqlalchemy.orm import Session
from database import db
from models.order import Order
from sqlalchemy import select

def save(order_data):
    with Session(db.engine) as session:
        with session.begin():
            new_order = Order(customer_id=order_data['customer_id'], product_id=order_data['product_id'], quantity=order_data['quantity'], total_price=order_data['total_price'])
            session.add(new_order)
            session.commit
        session.refresh(new_order)
        return new_order
    
def find_all(page=1, per_page=10):
    query = select(Order).offset((page-1) * per_page).limit(per_page)
    orders = db.session.execute(query).scalars().all()
    return orders
