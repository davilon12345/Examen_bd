from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Segment(Base):
    __tablename__ = "segments"

    segment_id = Column(Integer, primary_key=True, autoincrement=True)
    segment_name = Column(String)

    customers = relationship("Customer", back_populates="segment")


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String, primary_key=True)
    customer_name = Column(String)
    segment_id = Column(Integer, ForeignKey("segments.segment_id"))

    segment = relationship("Segment", back_populates="customers")
    orders = relationship("Order", back_populates="customer")


class ShipMode(Base):
    __tablename__ = "ship_modes"

    ship_mode_id = Column(Integer, primary_key=True, autoincrement=True)
    ship_mode_name = Column(String)

    orders = relationship("Order", back_populates="ship_mode")


class Location(Base):
    __tablename__ = "locations"

    location_id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String)
    region = Column(String)

    orders = relationship("Order", back_populates="location")


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String)

    subcategories = relationship("SubCategory", back_populates="category")


class SubCategory(Base):
    __tablename__ = "subcategories"

    subcategory_id = Column(Integer, primary_key=True, autoincrement=True)
    subcategory_name = Column(String)
    category_id = Column(Integer, ForeignKey("categories.category_id"))

    category = relationship("Category", back_populates="subcategories")
    products = relationship("Product", back_populates="subcategory")


class Product(Base):
    __tablename__ = "products"

    product_pk = Column(Integer, primary_key=True, autoincrement=True)
    product_code = Column(String)
    product_name = Column(String)
    subcategory_id = Column(Integer, ForeignKey("subcategories.subcategory_id"))

    subcategory = relationship("SubCategory", back_populates="products")
    order_details = relationship("OrderDetail", back_populates="product")


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True)
    order_date = Column(Date)
    ship_date = Column(Date)
    customer_id = Column(String, ForeignKey("customers.customer_id"))
    ship_mode_id = Column(Integer, ForeignKey("ship_modes.ship_mode_id"))
    location_id = Column(Integer, ForeignKey("locations.location_id"))

    customer = relationship("Customer", back_populates="orders")
    ship_mode = relationship("ShipMode", back_populates="orders")
    location = relationship("Location", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order")


class OrderDetail(Base):
    __tablename__ = "order_details"

    order_detail_id = Column(Integer, primary_key=True, autoincrement=True)
    row_id = Column(Integer)
    order_id = Column(String, ForeignKey("orders.order_id"))
    product_pk = Column(Integer, ForeignKey("products.product_pk"))
    sales = Column(Float)
    quantity = Column(Integer)
    discount = Column(Float)
    profit = Column(Float)

    order = relationship("Order", back_populates="order_details")
    product = relationship("Product", back_populates="order_details")


class StgSuperstore(Base):
    __tablename__ = "stg_superstore"
    __table_args__ = {"schema": "superstore"}

    no = Column(String, primary_key=True)
    row_id = Column(String)
    order_id = Column(String)
    order_date = Column(String)
    ship_date = Column(String)
    ship_mode = Column(String)
    customer_id = Column(String)
    customer_name = Column(String)
    segment = Column(String)
    country = Column(String)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String)
    region = Column(String)
    product_code = Column(String)
    category = Column(String)
    subcategory = Column(String)
    product_name = Column(String)
    sales = Column(String)
    quantity = Column(String)
    discount = Column(String)
    profit = Column(String)