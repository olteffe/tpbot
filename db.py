from sqlalchemy import Column, ForeignKey, Integer, Text, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///tp.db', echo=True)
Base = declarative_base()


class Author(Base):
    __tablename__ = 'author'
    __tablearg__ = {'comment': 'Автор объявления'}
    author_id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        sqlite_autoincrement=True,
    )
    author_name = Column(Text, comment='Имя автора объявления')
    count_number = Column(Integer, comment='Количество совпадений телефонов')


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
    author_id = Column(Integer, ForeignKey(Author.author_id), comment='ID автора объявления')
    ad_link = Column(Text, unique=True, comment='Ссылка на объявление')
    ad_description = Column(Text, comment='Описание объявления')
    ad_date = Column(Text, comment='Дата создания объявления')
    author = relationship('Author', backref='quote_author', lazy='subquery')


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

