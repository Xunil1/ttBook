from db.base_class import Base
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Company(Base):
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False, unique=True)                          # Имя

    departments = relationship("Department", back_populates="company")
    positions = relationship("Position", back_populates="company")
    users = relationship("User", back_populates="company")

    sections = relationship('Section', secondary='sectioncompany', back_populates='companies')
    files = relationship('File', secondary='filecompany', back_populates='companies')




