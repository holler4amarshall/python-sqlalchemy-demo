from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

engine = create_engine('postgresql://ubuntu:22zigzag@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    
    owner_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    bids = relationship("Bid", backref="item")
  
class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    item = relationship("Item", uselist=False, backref="seller")
    bids = relationship("Bid", backref="bidder")
    
class Bid(Base):
    __tablename__= "bid"
    
    id=Column(Integer, primary_key=True)
    price=Column(Integer, nullable=False)
    #note, integer is required to be a floating point type (eg "FLOAT")
    
    bidder_id = Column(Integer, ForeignKey('user.id'),nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    
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
baseball.seller = holly
sellerbid = Bid(item = baseball, price = 15, bidder = holly)

#the other 2 users bid for the baseball
bid1 = Bid(item = baseball, price = 20, bidder = wendy)
bid2 = Bid(item = baseball, price = 25, bidder = christian)

#add items to session
session.add(holly)
session.add(christian)
session.add(wendy)
session.add(baseball)
session.add(sellerbid)
session.add(bid1)
session.add(bid2)

#commit
session.commit()

#debug
print ("starting price = ${}, bid1 = ${}, bid2 = ${}".format(sellerbid.price, bid1.price, bid2.price))

#perform a query to find out which user placed the highest bid
winner = (session.query(Bid.price, Bid.bidder_id).order_by(Bid.price.desc()).first()) #.bidder.username
winning_bidder = (winner[1].bidder.username)
#print (winner)



