from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql://ubuntu:22zigzag@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
  
class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
class Bid(Base):
    __tablename__= "bid"
    
    id=Column(Integer, primary_key=True)
    price=Column(Integer, nullable=False)
    #note, integer is required to be a floating point type (eg "FLOAT")
    
    bidder_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
    
#create a new table for each subclass of Base, ignoring tables which already exist in DB    
Base.metadata.create_all(engine)

#create 3 users
holly = User()
holly.username = "hmarshall"
holly.password = "holly123"
christian = User()
christian.username = "cmarshall"
christian.password = "christian123"
wendy = User()
wendy.username = "wmarshall"
wendy.password = "wendy123"
#add an item (a baseball)
baseball = Item()
baseball.name = "Rawlings Major League Baseball"
baseball.description = "Made to the exact specifications of Major League Baseball, 5 ounces, 108 stitches"

#a user auctions a baseball

#the other 2 users bid for the baseball

#perform a query to find out which user placed the highest bid

#add items to session
session.add(holly)
session.add(christian)
session.add(wendy)

#commit
session.commit()

