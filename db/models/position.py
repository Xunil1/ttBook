from db.base_class import Base
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Position(Base):
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False, unique=True)                          # Имя

    company_id = Column(Integer, ForeignKey("company.id"))
    department_id = Column(Integer, ForeignKey("department.id"))

    company = relationship("Company", back_populates="positions")
    department = relationship("Department", back_populates="positions")
    users = relationship("User", back_populates="position")

    sections = relationship('Section', secondary='sectionposition', back_populates='positions')
    files = relationship('File', secondary='fileposition', back_populates='positions')





