from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column 
import uuid 

class Base(DeclarativeBase): 
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)