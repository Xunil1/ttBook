from db.base_class import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ARRAY
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class SectionCompany(Base):
    id = Column(Integer, primary_key=True)
    notes = Column(String, nullable=True)
    section_id = Column(Integer, ForeignKey('section.id'))
    company_id = Column(Integer, ForeignKey('company.id'))


class SectionDepartment(Base):
    id = Column(Integer, primary_key=True)
    notes = Column(String, nullable=True)
    section_id = Column(Integer, ForeignKey('section.id'))
    department_id = Column(Integer, ForeignKey('department.id'))


class SectionPosition(Base):
    id = Column(Integer, primary_key=True)
    notes = Column(String, nullable=True)
    section_id = Column(Integer, ForeignKey('section.id'))
    position_id = Column(Integer, ForeignKey('position.id'))


class SectionUser(Base):
    id = Column(Integer, primary_key=True)
    notes = Column(String, nullable=True)
    section_id = Column(Integer, ForeignKey('section.id'))
    user_id = Column(Integer, ForeignKey('user.id'))