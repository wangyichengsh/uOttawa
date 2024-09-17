from sqlalchemy import create_engine
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

engine = create_engine("sqlite:///Contact.db")

class Base(DeclarativeBase):
    pass
    
class Contact(Base):
    __tablename__ = "contact"   
    
    firstName: Mapped[str] = mapped_column(String(30), nullable=False)
    lastName: Mapped[str] = mapped_column(String(30), nullable=False)
    phoneNumber: Mapped[str] = mapped_column(primary_key=True)
    emailAddress: Mapped[str] = mapped_column(String(50), nullable=True)
    address: Mapped[str] = mapped_column(String(100), nullable=True)
    
    def __repr__(self) -> str:
        return f"|| {self.firstName!r} || {self.lastName!r} || {self.phoneNumber!r} || {self.emailAddress!r} || {self.address!r} ||"
        
if __name__=="__main__":
    Base.metadata.create_all(engine)