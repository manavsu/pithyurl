from sqlalchemy import Column, String, Integer
import time

from app.models import DB_Base

class LogEntry(DB_Base):
    __tablename__ = 'log'

    id = Column(String, primary_key=True, index=True)
    timestamp = Column(Integer, default=time.time_ns(), index=True)
    message = Column(String, nullable=False)

    def __repr__(self):
        return f'<Log Entry id:{self.id} timestamp:{self.timestamp} message:{self.message}>'