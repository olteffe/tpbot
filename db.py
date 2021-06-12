from sqlalchemy import Column, ForeignKey, Integer, Text, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Ad(Base):
    __tablename__ = 'ad'
    __tablearg__ = {'comment': 'Объявления'}
    ad_id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        sqlite_autoincrement=True
    )
    ad_author = Column(Text, comment='Имя автора объявления')
    ad_link = Column(Text, unique=True, comment='Ссылка на объявление')
    ad_description = Column(Text, comment='Описание объявления')
    ad_phone = Column(Text, comment='Номер телефона пользователя')
    ad_date = Column(Text, comment='Описание объявления')


class Agency(Base):
    __tablename__ = 'agency'
    __tablearg__ = {'comment': 'Агентства'}
    agency_id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        sqlite_autoincrement=True
    )
    agency_name = Column(Text, comment='Название агентства')
    agency_phone = Column(Text, comment='Номер телефона агентства')


class Author(Base):
    __tablename__ = 'author'
    __tablearg__ = {'comment': 'Количество объявлений пользователя'}
    ad_id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        sqlite_autoincrement=True
    )
    ad_author = Column(Text, ForeignKey('ad.ad_author'), comment='Имя автора объявления')
    count_number = Column(Integer, comment='Количество совпадений телефонов')
