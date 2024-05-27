from sqlalchemy.orm import Session
from database import db
from models.product import Product
from sqlalchemy import select

def save(product_data):
    with Session(db.engine) as session:
        with session.begin():
            new_product = Product(name=product_data['name'], price=product_data['price'])
            session.add(new_product)
            session.commit()
        session.refresh(new_product)
        return new_product
    
def find_all(page=1, per_page=10):
    query = select(Product).offset((page-1) * per_page).limit(per_page)
    products = db.session.execute(query).scalars().all()
    return products