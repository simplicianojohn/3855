from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class FoodDeliveryRequest(Base):
    """ Blood Pressure """

    __tablename__ = "food_delivery_request"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)
    driver_id = Column(String(250), nullable=False)
    customer_address = Column(String(250), nullable=False)
    order_id = Column(String(250), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, customer_id, driver_id, customer_address, order_id):
        """ Initializes a blood pressure reading """
        self.customer_id = customer_id
        self.driver_id = driver_id
        self.customer_address = customer_address
        self.order_id = order_id
        self.date_created = datetime.datetime.now() # Sets the date/time record is created


    def to_dict(self):
        """ Dictionary Representation of a blood pressure reading """
        dict = {}
        dict['id'] = self.id
        dict['customer_id'] = self.customer_id
        dict['driver_id'] = self.driver_id
        dict['customer_address'] = self.customer_address
        dict['order_id'] = self.order_id
        dict['date_created'] = self.date_created

        return dict
