from sqlalchemy import *
from sqlalchemy.orm import ( scoped_session, sessionmaker, relationship, backref)
from .configuration import  get_property_value_from_dict_name as get_property_value
from sqlalchemy.ext.declarative import  declarative_base
import cx_Oracle

from contextlib import contextmanager

host = get_property_value('BILLING', 'host')
port = get_property_value('BILLING', 'port')
svc_name = get_property_value('BILLING', 'database')
user = get_property_value('BILLING', 'db_user')
password = get_property_value('BILLING', 'db_password')
sid = cx_Oracle.makedsn(host, port, service_name=svc_name)

db_criteria = 'oracle://{user}:{password}@{sid}'.format(
    user=user,
    password=password,
    sid=sid
)

engine = create_engine(
     db_criteria,
     pool_recycle=10,
     pool_size=5,
     echo=True,
     max_overflow=0,
     convert_unicode=True
)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Department(Base):
    __tablename__ = 'DEPARTMENT'

    id = Column('ID', Integer, primary_key=True)
    name = Column('NAME', String)


class Employee(Base):
    __tablename__ = 'EMPLOYEE'
    id = Column('ID', Integer, primary_key=True)
    name = Column('NAME', String)
    hired_on = Column('HIRED_ON', DateTime, default=func.now())
    department_id = Column('DEPARTMENT_ID', Integer, ForeignKey('DEPARTMENT.ID'))
    department = relationship('Department', backref=backref('employees'))


class NewsUser(Base):
    __tablename__ = 'NEWS_USER'
    id = Column('ID', Integer, primary_key=True)
    name = Column('NAME', String)
    email = Column('EMAIL', String)
    password = Column('PASSWORD', String)

class NewsLink(Base):
    __tablename__ = 'NEWS_LINK'

    id = Column('ID', Integer, primary_key=True)
    created_at = Column('CREATED_AT',  DateTime, default=func.now())
    description = Column('DESCRIPTION', String)
    url = Column('URL', String)
    user_id = Column('USER_ID', Integer, ForeignKey('NEWS_USER.ID'))
    user = relationship('NewsUser', backref=backref('user_ref'))

# class NewsVote(Base):
#     __tablename__ = 'NEWS_VOTE'
#
#     id = Column('ID', Integer, primary_key=True)
#     user_id = Column('USER_ID', Integer, ForeignKey('NEWS_USER.ID'))
#     user = relationship('NewsUser', backref=backref('user_ref'))
#     link_id = Column('LINK_ID', Integer, ForeignKey('NEWS_LINK.ID'))
#     link = relationship('NewsLink', backref=backref('link_ref'))