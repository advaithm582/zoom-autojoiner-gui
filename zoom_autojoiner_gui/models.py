from sqlalchemy import create_engine
from sqlalchemy import (
    Column,
    Integer,
    String,
    REAL,
    DateTime
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from zoom_autojoiner_gui.constants import DB_URL


engine = create_engine(DB_URL)
# Session = sessionmaker(bind=engine)
Base = declarative_base()

class Meetings(Base):
    """Meetings 
    
    Class containing the Meetings table.
    """
    __tablename__ = 'meetings'

    id = Column(Integer, primary_key=True)
    mtg_provider = Column(String)
    mtg_id = Column(String)
    mtg_password = Column(String)
    mtg_time = Column(DateTime)
    def __repr__(self):
        return "<Meeting(mtg_provider='%s', mtg_id='%s', mtg_password='%s')>" \
            % (self.mtg_provider, self.mtg_id, self.mtg_password)

Base.metadata.create_all(engine)


