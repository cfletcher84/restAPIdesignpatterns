from sqlalchemy.orm import Session
from database import db
from models.production import Production
from sqlalchemy import select

def save(production_data):
    with Session(db.engine) as session:
        with session.begin():
            new_production_data = Production(product_id=production_data['product_id'], quantity_produced=production_data['quantity_produced'], date_produced=production_data['date_produced'])
            session.add(new_production_data)
            session.commit()
        session.refresh(new_production_data)
        return new_production_data
    
def find_all():
    query = select(Production)
    productions = db.session.execute(query).scalars().all()
    return productions