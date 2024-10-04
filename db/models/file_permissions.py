from db.base_class import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ARRAY
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class FileCompany(Base):
    id = Column(Integer, primary_key=True)
    notes = Column(String, nullable=True)
    file_id = Column(Integer, ForeignKey('file.id'))
    company_id = Column(Integer, ForeignKey('company.id'))


class FileDepartment(Base):
    id = Column(Integer, primary_key=True)
    notes = Column(String, nullable=True)
    file_id = Column(Integer, ForeignKey('file.id'))
    department_id = Column(Integer, ForeignKey('department.id'))


class FilePosition(Base):
    id = Column(Integer, primary_key=True)
    notes = Column(String, nullable=True)
    file_id = Column(Integer, ForeignKey('file.id'))
    position_id = Column(Integer, ForeignKey('position.id'))


class FileUser(Base):
    id = Column(Integer, primary_key=True)
    notes = Column(String, nullable=True)
    file_id = Column(Integer, ForeignKey('file.id'))
    user_id = Column(Integer, ForeignKey('user.id'))