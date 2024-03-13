from database import Base
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String)
    #address_id = Column(Integer, ForeignKey("address.id"), nullable= True)


class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relatonshup("Users", back_populates = "todos")

# class Address(Base):
#     __tablename__ = 'address'

#     address1 = Column(String)
#     address2 = Column(String)
#     city = Column(String)
#     state = Column(String)
#     country = Column(String)
#     postalcode = Column(String)
#      apt_num =  Column(integer) 

#     owner = relationship("Users", back_populates = "address")


