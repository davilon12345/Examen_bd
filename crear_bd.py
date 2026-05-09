from conexion import engine
from models import (
    Base,
    Segment,
    Customer,
    ShipMode,
    Location,
    Category,
    SubCategory,
    Product,
    Order,
    OrderDetail
)

Base.metadata.create_all(
    engine,
    tables=[
        Segment.__table__,
        Customer.__table__,
        ShipMode.__table__,
        Location.__table__,
        Category.__table__,
        SubCategory.__table__,
        Product.__table__,
        Order.__table__,
        OrderDetail.__table__
    ]
)

print("Tablas creadas correctamente en Store2.")