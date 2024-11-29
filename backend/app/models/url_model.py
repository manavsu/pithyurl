from sqlalchemy import Column, String, Integer

from app.models import DB_Base

class URL(DB_Base):
    __tablename__ = 'urls'

    short_url = Column(String, primary_key=True, index=True)
    url = Column(String, nullable=False)
    clicks = Column(Integer, default=0)

    def __repr__(self):
        return f'<URL key:{self.short_url} url:{self.url} clicks:{self.clicks}>'