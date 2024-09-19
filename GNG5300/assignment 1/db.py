from sqlalchemy import create_engine
from sqlalchemy import String, Integer, DateTime
from sqlalchemy import Column, text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

engine = create_engine("sqlite:///Contact.db")

class Base(DeclarativeBase):
    pass
    
    
class Contact(Base):
    __tablename__ = "contact"   
    
    cid: Mapped[int] = mapped_column(Integer, primary_key=True , autoincrement=True)
    firstName: Mapped[str] = mapped_column(String(30), nullable=False)
    lastName: Mapped[str] = mapped_column(String(30), nullable=False)
    phoneNumber: Mapped[str] = mapped_column(String(14), nullable=False)
    emailAddress: Mapped[str] = mapped_column(String(50), nullable=True)
    address: Mapped[str] = mapped_column(String(100), nullable=True)
    add_ts = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    update_ts = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    
    def __repr__(self) -> str:
        return f"{self.cid!r}|| {self.firstName!r} || {self.lastName!r} || {self.phoneNumber!r} || {self.emailAddress!r} || {self.address!r} || {self.strftime("%Y-%m-%d %I:%M%p")!r}"
                
        
if __name__=="__main__":
    Base.metadata.create_all(engine)