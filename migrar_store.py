from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from conexion import engine as engine_destino, Session
from models import (
    Base,
    StgSuperstore,
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

engine_origen = create_engine("postgresql://postgres:Davilon_123@localhost:5432/Store")
SessionOrigen = sessionmaker(bind=engine_origen)


def convertir_fecha(valor):
    if valor is None:
        return None

    valor = str(valor).strip()

    formatos = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%m-%d-%Y",
        "%d-%m-%Y"
    ]

    for formato in formatos:
        try:
            return datetime.strptime(valor, formato).date()
        except ValueError:
            pass

    return None


def convertir_float(valor):
    if valor is None or str(valor).strip() == "":
        return 0.0

    valor = str(valor).replace(",", ".").strip()
    return float(valor)


def convertir_int(valor):
    if valor is None or str(valor).strip() == "":
        return 0

    return int(float(str(valor).strip()))


def migrar():
    src = SessionOrigen()
    dst = Session()

    Base.metadata.create_all(
    engine_destino,
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

    rows = src.query(StgSuperstore).all()

    print("Total filas encontradas:", len(rows))

    seg_map = {}
    ship_map = {}
    loc_map = {}
    cat_map = {}
    sub_map = {}
    prod_map = {}

    for r in rows:

        if r.segment not in seg_map:
            seg = Segment(segment_name=r.segment)
            dst.add(seg)
            dst.flush()
            seg_map[r.segment] = seg.segment_id

        if r.ship_mode not in ship_map:
            ship = ShipMode(ship_mode_name=r.ship_mode)
            dst.add(ship)
            dst.flush()
            ship_map[r.ship_mode] = ship.ship_mode_id

        loc_key = (r.country, r.city, r.state, r.postal_code, r.region)

        if loc_key not in loc_map:
            loc = Location(
                country=r.country,
                city=r.city,
                state=r.state,
                postal_code=r.postal_code,
                region=r.region
            )
            dst.add(loc)
            dst.flush()
            loc_map[loc_key] = loc.location_id

        if r.category not in cat_map:
            cat = Category(category_name=r.category)
            dst.add(cat)
            dst.flush()
            cat_map[r.category] = cat.category_id

        sub_key = (r.subcategory, r.category)

        if sub_key not in sub_map:
            sub = SubCategory(
                subcategory_name=r.subcategory,
                category_id=cat_map[r.category]
            )
            dst.add(sub)
            dst.flush()
            sub_map[sub_key] = sub.subcategory_id

        if r.product_code not in prod_map:
            prod = Product(
                product_code=r.product_code,
                product_name=r.product_name,
                subcategory_id=sub_map[sub_key]
            )
            dst.add(prod)
            dst.flush()
            prod_map[r.product_code] = prod.product_pk

        cliente = dst.query(Customer).filter_by(customer_id=r.customer_id).first()

        if cliente is None:
            cliente = Customer(
                customer_id=r.customer_id,
                customer_name=r.customer_name,
                segment_id=seg_map[r.segment]
            )
            dst.add(cliente)
            dst.flush()

        orden = dst.query(Order).filter_by(order_id=r.order_id).first()

        if orden is None:
            orden = Order(
                order_id=r.order_id,
                order_date=convertir_fecha(r.order_date),
                ship_date=convertir_fecha(r.ship_date),
                customer_id=r.customer_id,
                ship_mode_id=ship_map[r.ship_mode],
                location_id=loc_map[loc_key]
            )
            dst.add(orden)
            dst.flush()

        detalle = OrderDetail(
            row_id=convertir_int(r.row_id),
            order_id=r.order_id,
            product_pk=prod_map[r.product_code],
            sales=convertir_float(r.sales),
            quantity=convertir_int(r.quantity),
            discount=convertir_float(r.discount),
            profit=convertir_float(r.profit)
        )

        dst.add(detalle)

    dst.commit()

    src.close()
    dst.close()

    print("Migración completada correctamente.")


if __name__ == "__main__":
    migrar()