from db.base_class import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ARRAY
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class File(Base):
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False, unique=True)

    url = Column(String, nullable=True)

    code = Column(String, nullable=True)

    allowed_all = Column(Boolean, default=False)

    section_id = Column(Integer, ForeignKey("section.id"))

    section = relationship("Section", back_populates="files")

    users = relationship('User', secondary='fileuser', back_populates='files')
    positions = relationship('Position', secondary='fileposition', back_populates='files')
    departments = relationship('Department', secondary='filedepartment', back_populates='files')
    companies = relationship('Company', secondary='filecompany', back_populates='files')







