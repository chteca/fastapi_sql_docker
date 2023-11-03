from datetime import date, datetime
from sqlalchemy import Date, DateTime, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Publisher(Base):
    __tablename__ = 'publishers'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    book: Mapped[list['Book']] = relationship('Book', cascade='all, delete')



class Book(Base):
    __tablename__ = 'books'
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    id_publisher: Mapped[int] = mapped_column(Integer, ForeignKey('publishers.id'))

    publisher: Mapped['Publisher'] = relationship('Publisher', back_populates='book')
    stock: Mapped[list['Stock']] = relationship('Stock', cascade='all, delete')


class Shop(Base):
    __tablename__ = 'shops'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    stock: Mapped[list['Stock']] = relationship('Stock', cascade='all, delete')




class Stock(Base):
    __tablename__ = 'stocks'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_book: Mapped[int] = mapped_column(Integer, ForeignKey('books.id'))
    id_shop: Mapped[int] = mapped_column(Integer, ForeignKey('shops.id'))
    count: Mapped[int] = mapped_column(Integer)

    book: Mapped['Book'] = relationship('Book', back_populates='stock')
    shop: Mapped['Shop'] = relationship('Shop', back_populates='stock')

    sale: Mapped[list['Sale']] = relationship('Sale', cascade='all, delete')

class Sale(Base):
    __tablename__ = 'sales'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    data_sale: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    id_stock: Mapped[int] = mapped_column(Integer, ForeignKey('stocks.id'))
    count: Mapped[int] = mapped_column(Integer)

    stock: Mapped['Stock'] = relationship('Stock', back_populates='sale')

