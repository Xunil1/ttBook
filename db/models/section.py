from db.base_class import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ARRAY
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Section(Base):
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False, unique=True)

    allowed_all = Column(Boolean, default=True)

    files = relationship("File", back_populates="section")

    users = relationship('User', secondary='sectionuser', back_populates='sections')
    positions = relationship('Position', secondary='sectionposition', back_populates='sections')
    departments = relationship('Department', secondary='sectiondepartment', back_populates='sections')
    companies = relationship('Company', secondary='sectioncompany', back_populates='sections')







