from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class OrderRequest(Base):
    """ Blood Pressure """

    __tablename__ = "order_request"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)
    order_id = Column(String(250), nullable=False)
    date = Column(String(250), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, customer_id, order_id, date):
        """ Initializes a blood pressure reading """
        self.customer_id = customer_id
        self.order_id = order_id
        self.date = date
        self.date_created = datetime.datetime.now() # Sets the date/time record is created


    def to_dict(self):
        """ Dictionary Representation of a blood pressure reading """
        dict = {}
        dict['id'] = self.id
        dict['customer_id'] = self.customer_id
        dict['order_id'] = self.order_id
        dict['date'] = self.date
        dict['date_created'] = self.date_created

        return dict
