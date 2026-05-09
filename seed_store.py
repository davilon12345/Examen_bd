from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Segment, Customer, ShipMode, Location, Category, SubCategory, Product, Order, OrderDetail
from datetime import date

engine = create_engine('postgresql://postgres:Davilon_123@localhost:5432/Store')
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

segments = [
    Segment(id=1, name='Consumer'),
    Segment(id=2, name='Corporate'),
    Segment(id=3, name='Home Office'),
]
session.add_all(segments)

ship_modes = [
    ShipMode(id=1, name='Standard Class'),
    ShipMode(id=2, name='Second Class'),
    ShipMode(id=3, name='First Class'),
    ShipMode(id=4, name='Same Day'),
]
session.add_all(ship_modes)

locations = [
    Location(id=1, country='United States', city='New York City', state='New York', postal_code='10001', region='East'),
    Location(id=2, country='United States', city='Los Angeles', state='California', postal_code='90001', region='West'),
    Location(id=3, country='United States', city='Chicago', state='Illinois', postal_code='60601', region='Central'),
    Location(id=4, country='United States', city='Houston', state='Texas', postal_code='77001', region='Central'),
    Location(id=5, country='United States', city='Phoenix', state='Arizona', postal_code='85001', region='West'),
    Location(id=6, country='United States', city='Philadelphia', state='Pennsylvania', postal_code='19019', region='East'),
    Location(id=7, country='United States', city='San Antonio', state='Texas', postal_code='78201', region='Central'),
    Location(id=8, country='United States', city='San Diego', state='California', postal_code='92101', region='West'),
    Location(id=9, country='United States', city='Dallas', state='Texas', postal_code='75201', region='Central'),
    Location(id=10, country='United States', city='Miami', state='Florida', postal_code='33101', region='East'),
]
session.add_all(locations)

customers = [
    Customer(id=1, customer_id='C-001', name='Juan Perez', segment_id=1),
    Customer(id=2, customer_id='C-002', name='Maria Garcia', segment_id=2),
    Customer(id=3, customer_id='C-003', name='Carlos Lopez', segment_id=3),
    Customer(id=4, customer_id='C-004', name='Ana Martinez', segment_id=1),
    Customer(id=5, customer_id='C-005', name='Pedro Rodriguez', segment_id=2),
    Customer(id=6, customer_id='C-006', name='Laura Sanchez', segment_id=3),
    Customer(id=7, customer_id='C-007', name='Diego Hernandez', segment_id=1),
    Customer(id=8, customer_id='C-008', name='Sofia Diaz', segment_id=2),
    Customer(id=9, customer_id='C-009', name='Alejandro Torres', segment_id=3),
    Customer(id=10, customer_id='C-010', name='Valentina Ramirez', segment_id=1),
]
session.add_all(customers)

categories = [
    Category(id=1, name='Technology'),
    Category(id=2, name='Furniture'),
    Category(id=3, name='Office Supplies'),
]
session.add_all(categories)

subcategories = [
    SubCategory(id=1, name='Phones', category_id=1),
    SubCategory(id=2, name='Computers', category_id=1),
    SubCategory(id=3, name='Chairs', category_id=2),
    SubCategory(id=4, name='Tables', category_id=2),
    SubCategory(id=5, name='Paper', category_id=3),
    SubCategory(id=6, name='Binders', category_id=3),
    SubCategory(id=7, name='Accessories', category_id=1),
    SubCategory(id=8, name='Bookcases', category_id=2),
    SubCategory(id=9, name='Appliances', category_id=3),
    SubCategory(id=10, name='Art', category_id=3),
]
session.add_all(subcategories)

products = [
    Product(id=1, product_id='P-001', name='iPhone 14 Pro', subcategory_id=1),
    Product(id=2, product_id='P-002', name='Samsung Galaxy S23', subcategory_id=1),
    Product(id=3, product_id='P-003', name='MacBook Pro 16', subcategory_id=2),
    Product(id=4, product_id='P-004', name='Dell XPS 15', subcategory_id=2),
    Product(id=5, product_id='P-005', name='Oficina Chair', subcategory_id=3),
    Product(id=6, product_id='P-006', name='Ergonomic Chair', subcategory_id=3),
    Product(id=7, product_id='P-007', name='Desk Table', subcategory_id=4),
    Product(id=8, product_id='P-008', name='Conference Table', subcategory_id=4),
    Product(id=9, product_id='P-009', name='A4 Paper Box', subcategory_id=5),
    Product(id=10, product_id='P-010', name='Staples', subcategory_id=6),
    Product(id=11, product_id='P-011', name='Mouse Pad', subcategory_id=7),
    Product(id=12, product_id='P-012', name='USB Hub', subcategory_id=7),
    Product(id=13, product_id='P-013', name='Bookshelf', subcategory_id=8),
    Product(id=14, product_id='P-014', name='Microwave', subcategory_id=9),
    Product(id=15, product_id='P-015', name='Canvas Set', subcategory_id=10),
]
session.add_all(products)
session.commit()

orders_data = [
    (1, 'ORD-001', date(2023, 1, 15), date(2023, 1, 20), 1, 1, 1),
    (2, 'ORD-002', date(2023, 2, 10), date(2023, 2, 14), 2, 2, 2),
    (3, 'ORD-003', date(2023, 3, 5), date(2023, 3, 8), 3, 3, 3),
    (4, 'ORD-004', date(2023, 4, 20), date(2023, 4, 25), 4, 1, 4),
    (5, 'ORD-005', date(2023, 5, 12), date(2023, 5, 16), 5, 2, 5),
    (6, 'ORD-006', date(2023, 6, 8), date(2023, 6, 11), 6, 3, 6),
    (7, 'ORD-007', date(2023, 7, 3), date(2023, 7, 7), 7, 4, 7),
    (8, 'ORD-008', date(2023, 8, 15), date(2023, 8, 19), 8, 1, 8),
    (9, 'ORD-009', date(2023, 9, 1), date(2023, 9, 5), 9, 2, 9),
    (10, 'ORD-010', date(2023, 10, 10), date(2023, 10, 14), 10, 3, 10),
    (11, 'ORD-011', date(2024, 1, 10), date(2024, 1, 15), 1, 1, 2),
    (12, 'ORD-012', date(2024, 2, 5), date(2024, 2, 9), 2, 2, 4),
    (13, 'ORD-013', date(2024, 3, 18), date(2024, 3, 22), 3, 3, 6),
    (14, 'ORD-014', date(2024, 4, 25), date(2024, 4, 29), 4, 4, 8),
    (15, 'ORD-015', date(2024, 5, 30), date(2024, 6, 3), 5, 1, 10),
]

orders = []
for oid, oref, od, sd, cid, smid, lid in orders_data:
    orders.append(Order(id=oid, order_id=oref, order_date=od, ship_date=sd,
                        customer_id=cid, ship_mode_id=smid, location_id=lid))
session.add_all(orders)

order_details = [
    OrderDetail(id=1, order_id=1, product_id=1, sales=1000, quantity=2, discount=0.0, profit=300),
    OrderDetail(id=2, order_id=1, product_id=11, sales=50, quantity=5, discount=0.1, profit=10),
    OrderDetail(id=3, order_id=2, product_id=3, sales=2500, quantity=1, discount=0.0, profit=750),
    OrderDetail(id=4, order_id=2, product_id=12, sales=80, quantity=3, discount=0.05, profit=20),
    OrderDetail(id=5, order_id=3, product_id=5, sales=450, quantity=3, discount=0.0, profit=150),
    OrderDetail(id=6, order_id=3, product_id=9, sales=120, quantity=10, discount=0.0, profit=40),
    OrderDetail(id=7, order_id=4, product_id=2, sales=900, quantity=2, discount=0.15, profit=100),
    OrderDetail(id=8, order_id=4, product_id=14, sales=200, quantity=1, discount=0.0, profit=60),
    OrderDetail(id=9, order_id=5, product_id=4, sales=1800, quantity=1, discount=0.0, profit=500),
    OrderDetail(id=10, order_id=5, product_id=7, sales=600, quantity=2, discount=0.1, profit=120),
    OrderDetail(id=11, order_id=6, product_id=6, sales=350, quantity=2, discount=0.0, profit=100),
    OrderDetail(id=12, order_id=6, product_id=10, sales=30, quantity=6, discount=0.2, profit=-10),
    OrderDetail(id=13, order_id=7, product_id=8, sales=1200, quantity=1, discount=0.0, profit=400),
    OrderDetail(id=14, order_id=7, product_id=13, sales=400, quantity=2, discount=0.25, profit=-50),
    OrderDetail(id=15, order_id=8, product_id=1, sales=950, quantity=1, discount=0.0, profit=285),
    OrderDetail(id=16, order_id=8, product_id=15, sales=80, quantity=4, discount=0.3, profit=-20),
    OrderDetail(id=17, order_id=9, product_id=3, sales=2400, quantity=1, discount=0.0, profit=720),
    OrderDetail(id=18, order_id=9, product_id=5, sales=400, quantity=2, discount=0.35, profit=-80),
    OrderDetail(id=19, order_id=10, product_id=2, sales=850, quantity=1, discount=0.0, profit=250),
    OrderDetail(id=20, order_id=10, product_id=6, sales=320, quantity=2, discount=0.4, profit=-100),
    OrderDetail(id=21, order_id=11, product_id=4, sales=1700, quantity=1, discount=0.0, profit=510),
    OrderDetail(id=22, order_id=11, product_id=9, sales=60, quantity=5, discount=0.0, profit=20),
    OrderDetail(id=23, order_id=12, product_id=1, sales=1050, quantity=2, discount=0.0, profit=315),
    OrderDetail(id=24, order_id=12, product_id=7, sales=550, quantity=1, discount=0.0, profit=165),
    OrderDetail(id=25, order_id=13, product_id=3, sales=2600, quantity=1, discount=0.0, profit=780),
    OrderDetail(id=26, order_id=13, product_id=11, sales=45, quantity=3, discount=0.0, profit=15),
    OrderDetail(id=27, order_id=14, product_id=5, sales=480, quantity=3, discount=0.0, profit=160),
    OrderDetail(id=28, order_id=14, product_id=10, sales=25, quantity=5, discount=0.5, profit=-15),
    OrderDetail(id=29, order_id=15, product_id=2, sales=920, quantity=2, discount=0.0, profit=276),
    OrderDetail(id=30, order_id=15, product_id=8, sales=1100, quantity=1, discount=0.0, profit=330),
    OrderDetail(id=31, order_id=1, product_id=14, sales=180, quantity=1, discount=0.0, profit=54),
    OrderDetail(id=32, order_id=2, product_id=15, sales=60, quantity=3, discount=0.1, profit=5),
    OrderDetail(id=33, order_id=3, product_id=13, sales=350, quantity=1, discount=0.0, profit=105),
    OrderDetail(id=34, order_id=4, product_id=12, sales=70, quantity=2, discount=0.0, profit=21),
    OrderDetail(id=35, order_id=5, product_id=9, sales=100, quantity=8, discount=0.0, profit=35),
]
session.add_all(order_details)

session.commit()
session.close()
print("Datos de ejemplo insertados exitosamente en Store.")
