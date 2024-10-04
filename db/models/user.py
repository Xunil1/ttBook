from db.base_class import Base
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    id = Column(Integer, primary_key=True, index=True)

    firstname = Column(String, nullable=False)                          # Имя
    lastname = Column(String, nullable=False)                           # Фамилия
    middlename = Column(String, nullable=False)                         # Отчество

    company_id = Column(Integer, ForeignKey("company.id"))
    department_id = Column(Integer, ForeignKey("department.id"))
    position_id = Column(Integer, ForeignKey("position.id"))

    company = relationship("Company", back_populates="users")                            # Компания
    department = relationship("Department", back_populates="users")                         # Отдел
    position = relationship("Position", back_populates="users")                          # Должность

    email = Column(String, nullable=False, unique=True, index=True)     # Почта
    password = Column(String, nullable=False)                           # Хэш пароля

    office_phone = Column(String, nullable=False)                       # Рабочий телефон
    phone = Column(String, nullable=False, unique=True, index=True)     # Личный телефон

    is_admin = Column(Boolean, default=False)

    status = Column(String, nullable=False, default="На работе")        # Статус

    token = Column(String, nullable=True)                               # Токен

    sections = relationship('Section', secondary='sectionuser', back_populates='users')
    files = relationship('File', secondary='fileuser', back_populates='users')



