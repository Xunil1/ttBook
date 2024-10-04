from db.base_class import Base
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Department(Base):
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False, unique=True)                          # Имя

    company_id = Column(Integer, ForeignKey("company.id"))

    company = relationship("Company", back_populates="departments")
    positions = relationship("Position", back_populates="department")
    users = relationship("User", back_populates="department")

    sections = relationship('Section', secondary='sectiondepartment', back_populates='departments')
    files = relationship('File', secondary='filedepartment', back_populates='departments')




