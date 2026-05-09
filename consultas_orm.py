from sqlalchemy import func, extract
from conexion import Session
from models import (
    Segment, Customer, Location, Category, SubCategory,
    Product, Order, OrderDetail
)

session = Session()


def consulta_1():
    return (
        session.query(
            Location.region.label("region"),
            Category.category_name.label("categoria"),
            func.sum(OrderDetail.sales).label("ventas_totales"),
            func.sum(OrderDetail.profit).label("ganancias_totales"),
            func.avg(OrderDetail.discount).label("descuento_promedio"),
            func.sum(OrderDetail.quantity).label("cantidad_total")
        )
        .join(Order, Order.order_id == OrderDetail.order_id)
        .join(Location, Location.location_id == Order.location_id)
        .join(Product, Product.product_pk == OrderDetail.product_pk)
        .join(SubCategory, SubCategory.subcategory_id == Product.subcategory_id)
        .join(Category, Category.category_id == SubCategory.category_id)
        .group_by(Location.region, Category.category_name)
        .order_by(func.sum(OrderDetail.profit).desc())
        .all()
    )


def consulta_2():
    return (
        session.query(
            Customer.customer_name.label("cliente"),
            func.sum(OrderDetail.sales).label("ventas"),
            func.sum(OrderDetail.profit).label("ganancias"),
            func.count(Order.order_id.distinct()).label("pedidos"),
            func.avg(OrderDetail.sales).label("ticket_promedio"),
            func.avg(OrderDetail.discount).label("descuento_promedio")
        )
        .join(Order, Order.customer_id == Customer.customer_id)
        .join(OrderDetail, OrderDetail.order_id == Order.order_id)
        .group_by(Customer.customer_name)
        .order_by(func.sum(OrderDetail.profit).desc())
        .limit(15)
        .all()
    )


def consulta_3():
    return (
        session.query(
            Location.region.label("region"),
            SubCategory.subcategory_name.label("subcategoria"),
            func.sum(OrderDetail.profit).label("perdida_total"),
            func.count(Order.order_id.distinct()).label("pedidos_afectados"),
            func.avg(OrderDetail.discount).label("descuento_promedio")
        )
        .join(Order, Order.order_id == OrderDetail.order_id)
        .join(Location, Location.location_id == Order.location_id)
        .join(Product, Product.product_pk == OrderDetail.product_pk)
        .join(SubCategory, SubCategory.subcategory_id == Product.subcategory_id)
        .group_by(Location.region, SubCategory.subcategory_name)
        .having(func.sum(OrderDetail.profit) < 0)
        .order_by(func.sum(OrderDetail.profit))
        .all()
    )


def consulta_4():
    return (
        session.query(
            Product.product_name.label("producto"),
            func.sum(OrderDetail.sales).label("ventas"),
            func.sum(OrderDetail.profit).label("ganancia"),
            (func.sum(OrderDetail.profit) / func.sum(OrderDetail.sales)).label("margen")
        )
        .join(OrderDetail, OrderDetail.product_pk == Product.product_pk)
        .group_by(Product.product_name)
        .having(func.count(OrderDetail.order_detail_id) > 20)
        .having(func.sum(OrderDetail.profit) > 0)
        .all()
    )


def consulta_5():
    return (
        session.query(
            Customer.customer_name.label("cliente"),
            func.count(Category.category_id.distinct()).label("categorias"),
            func.sum(OrderDetail.sales).label("ventas"),
            func.sum(OrderDetail.profit).label("ganancias"),
            func.count(Order.order_id.distinct()).label("pedidos")
        )
        .join(Order, Order.customer_id == Customer.customer_id)
        .join(OrderDetail, OrderDetail.order_id == Order.order_id)
        .join(Product, Product.product_pk == OrderDetail.product_pk)
        .join(SubCategory, SubCategory.subcategory_id == Product.subcategory_id)
        .join(Category, Category.category_id == SubCategory.category_id)
        .group_by(Customer.customer_name)
        .having(func.count(Category.category_id.distinct()) > 2)
        .all()
    )


def consulta_6():
    return (
        session.query(
            extract("year", Order.order_date).label("anio"),
            extract("month", Order.order_date).label("mes"),
            Location.region.label("region"),
            func.sum(OrderDetail.sales).label("ventas"),
            func.avg(OrderDetail.profit).label("ganancia_promedio"),
            func.avg(OrderDetail.sales).label("ticket_promedio"),
            func.count(Order.order_id.distinct()).label("pedidos"),
            func.count(Customer.customer_id.distinct()).label("clientes")
        )
        .join(OrderDetail, OrderDetail.order_id == Order.order_id)
        .join(Location, Location.location_id == Order.location_id)
        .join(Customer, Customer.customer_id == Order.customer_id)
        .group_by(extract("year", Order.order_date), extract("month", Order.order_date), Location.region)
        .order_by(extract("year", Order.order_date), extract("month", Order.order_date), Location.region)
        .all()
    )


def consulta_7():
    return (
        session.query(
            Product.product_name.label("producto"),
            func.count(Location.city.distinct()).label("ciudades"),
            func.count(Location.region.distinct()).label("regiones"),
            func.sum(OrderDetail.sales).label("ventas"),
            func.sum(OrderDetail.profit).label("ganancias")
        )
        .join(OrderDetail, OrderDetail.product_pk == Product.product_pk)
        .join(Order, Order.order_id == OrderDetail.order_id)
        .join(Location, Location.location_id == Order.location_id)
        .group_by(Product.product_name)
        .order_by(func.count(Location.city.distinct()).desc())
        .all()
    )


def consulta_8():

    subquery = (
        session.query(
            Order.location_id,
            func.count(Order.order_id).label("total_pedidos")
        )
        .group_by(Order.location_id)
        .subquery()
    )

    promedio_pedidos = (
        session.query(
            func.avg(subquery.c.total_pedidos)
        )
        .scalar()
    )

    return (
        session.query(
            Location.region.label("region"),
            func.avg(OrderDetail.discount).label("descuento_promedio"),
            func.sum(OrderDetail.profit).label("ganancias"),
            func.count(Order.order_id.distinct()).label("pedidos")
        )
        .join(Order, Order.location_id == Location.location_id)
        .join(OrderDetail, OrderDetail.order_id == Order.order_id)
        .group_by(Location.region)
        .having(func.avg(OrderDetail.discount) > 0.25)
        .having(func.sum(OrderDetail.profit) < 0)
        .having(func.count(Order.order_id.distinct()) > promedio_pedidos)
        .all()
    )


def consulta_9():
    return (
        session.query(
            Segment.segment_name.label("segmento"),
            Location.region.label("region"),
            func.avg(OrderDetail.sales).label("ticket_promedio"),
            func.sum(OrderDetail.sales).label("ventas"),
            func.sum(OrderDetail.profit).label("ganancias"),
            func.count(Order.order_id.distinct()).label("pedidos")
        )
        .join(Customer, Customer.segment_id == Segment.segment_id)
        .join(Order, Order.customer_id == Customer.customer_id)
        .join(Location, Location.location_id == Order.location_id)
        .join(OrderDetail, OrderDetail.order_id == Order.order_id)
        .group_by(Segment.segment_name, Location.region)
        .all()
    )


def consulta_10():
    return (
        session.query(
            Customer.customer_name.label("cliente"),
            Location.region.label("region"),
            Category.category_name.label("categoria"),
            Product.product_name.label("producto"),
            OrderDetail.profit.label("perdida_total"),
            OrderDetail.discount.label("descuento")
        )
        .join(Order, Order.order_id == OrderDetail.order_id)
        .join(Customer, Customer.customer_id == Order.customer_id)
        .join(Location, Location.location_id == Order.location_id)
        .join(Product, Product.product_pk == OrderDetail.product_pk)
        .join(SubCategory, SubCategory.subcategory_id == Product.subcategory_id)
        .join(Category, Category.category_id == SubCategory.category_id)
        .filter(OrderDetail.profit < 0)
        .order_by(OrderDetail.profit.asc())
        .all()
    )
    
def consulta_11():
    return (
        session.query(
            Customer.customer_name.label("cliente"),
            func.count(Location.region.distinct()).label("regiones_distintas"),
            func.count(SubCategory.subcategory_id.distinct()).label("subcategorias_distintas"),
            func.sum(OrderDetail.sales).label("ventas_acumuladas")
        )
        .join(Order, Order.customer_id == Customer.customer_id)
        .join(Location, Location.location_id == Order.location_id)
        .join(OrderDetail, OrderDetail.order_id == Order.order_id)
        .join(Product, Product.product_pk == OrderDetail.product_pk)
        .join(SubCategory, SubCategory.subcategory_id == Product.subcategory_id)
        .group_by(Customer.customer_name)
        .having(func.count(SubCategory.subcategory_id.distinct()) > 5)
        .having(func.count(Location.region.distinct()) > 2)
        .having(func.count(Order.order_id.distinct()) > 10)
        .all()
    )


def consulta_12():
    subq = (
        session.query(
            Location.region.label("region"),
            Category.category_name.label("categoria"),
            func.sum(OrderDetail.profit).label("ganancia"),
            func.sum(OrderDetail.sales).label("ventas"),
            func.count(Order.order_id.distinct()).label("pedidos")
        )
        .join(Order, Order.order_id == OrderDetail.order_id)
        .join(Location, Location.location_id == Order.location_id)
        .join(Product, Product.product_pk == OrderDetail.product_pk)
        .join(SubCategory, SubCategory.subcategory_id == Product.subcategory_id)
        .join(Category, Category.category_id == SubCategory.category_id)
        .group_by(Location.region, Category.category_name)
        .subquery()
    )

    maxq = (
        session.query(
            subq.c.region,
            func.max(subq.c.ganancia).label("max_ganancia")
        )
        .group_by(subq.c.region)
        .subquery()
    )

    return (
        session.query(
            subq.c.region,
            subq.c.categoria,
            subq.c.ganancia,
            subq.c.ventas,
            subq.c.pedidos
        )
        .join(
            maxq,
            (subq.c.region == maxq.c.region) &
            (subq.c.ganancia == maxq.c.max_ganancia)
        )
        .order_by(subq.c.region)
        .all()
    )


def consulta_13():
    ventas_categoria = (
        session.query(
            Location.region.label("region"),
            Category.category_name.label("categoria"),
            func.sum(OrderDetail.sales).label("ventas_categoria")
        )
        .join(Order, Order.order_id == OrderDetail.order_id)
        .join(Location, Location.location_id == Order.location_id)
        .join(Product, Product.product_pk == OrderDetail.product_pk)
        .join(SubCategory, SubCategory.subcategory_id == Product.subcategory_id)
        .join(Category, Category.category_id == SubCategory.category_id)
        .group_by(Location.region, Category.category_name)
        .subquery()
    )

    ventas_region = (
        session.query(
            Location.region.label("region"),
            func.sum(OrderDetail.sales).label("ventas_region")
        )
        .join(Order, Order.order_id == OrderDetail.order_id)
        .join(Location, Location.location_id == Order.location_id)
        .group_by(Location.region)
        .subquery()
    )

    return (
        session.query(
            ventas_categoria.c.region,
            ventas_categoria.c.categoria,
            ((ventas_categoria.c.ventas_categoria / ventas_region.c.ventas_region) * 100).label("participacion_porcentual"),
            ventas_region.c.ventas_region,
            ventas_categoria.c.ventas_categoria
        )
        .join(
            ventas_region,
            ventas_categoria.c.region == ventas_region.c.region
        )
        .order_by(ventas_categoria.c.region, ventas_categoria.c.categoria)
        .all()
    )


def consulta_14():
    pedidos_producto = (
        session.query(
            Product.product_pk.label("producto_id"),
            func.count(Order.order_id.distinct()).label("pedidos")
        )
        .join(OrderDetail, OrderDetail.product_pk == Product.product_pk)
        .join(Order, Order.order_id == OrderDetail.order_id)
        .group_by(Product.product_pk)
        .subquery()
    )

    promedio_pedidos = session.query(func.avg(pedidos_producto.c.pedidos)).scalar()

    return (
        session.query(
            Product.product_name.label("producto"),
            func.avg(OrderDetail.discount).label("descuento_promedio"),
            func.sum(OrderDetail.profit).label("ganancia_total"),
            func.sum(OrderDetail.sales).label("ventas_acumuladas"),
            func.count(Order.order_id.distinct()).label("pedidos")
        )
        .join(OrderDetail, OrderDetail.product_pk == Product.product_pk)
        .join(Order, Order.order_id == OrderDetail.order_id)
        .group_by(Product.product_name)
        .having(func.avg(OrderDetail.discount) > 0.25)
        .having(func.sum(OrderDetail.profit) < 0)
        .having(func.sum(OrderDetail.sales) > 1000)
        .having(func.count(Order.order_id.distinct()) > promedio_pedidos)
        .order_by(func.sum(OrderDetail.sales).desc())
        .all()
    )


def consulta_15():
    return (
        session.query(
            Location.region.label("region"),
            Category.category_name.label("categoria"),
            SubCategory.subcategory_name.label("subcategoria"),
            extract("year", Order.order_date).label("anio"),
            extract("month", Order.order_date).label("mes"),
            func.sum(OrderDetail.sales).label("ventas_acumuladas"),
            func.sum(OrderDetail.profit).label("ganancias_acumuladas"),
            func.avg(OrderDetail.sales).label("ticket_promedio"),
            func.avg(OrderDetail.discount).label("descuento_promedio"),
            func.count(Order.order_id.distinct()).label("cantidad_pedidos"),
            func.count(Customer.customer_id.distinct()).label("cantidad_clientes"),
            func.count(Product.product_pk.distinct()).label("cantidad_productos"),
            (func.sum(OrderDetail.profit) / func.sum(OrderDetail.sales)).label("margen_rentabilidad")
        )
        .join(Order, Order.order_id == OrderDetail.order_id)
        .join(Customer, Customer.customer_id == Order.customer_id)
        .join(Location, Location.location_id == Order.location_id)
        .join(Product, Product.product_pk == OrderDetail.product_pk)
        .join(SubCategory, SubCategory.subcategory_id == Product.subcategory_id)
        .join(Category, Category.category_id == SubCategory.category_id)
        .group_by(
            Location.region,
            Category.category_name,
            SubCategory.subcategory_name,
            extract("year", Order.order_date),
            extract("month", Order.order_date)
        )
        .order_by(
            Location.region,
            Category.category_name,
            SubCategory.subcategory_name,
            extract("year", Order.order_date),
            extract("month", Order.order_date)
        )
        .all()
    )


def mostrar(nombre, datos):
    print("\n" + nombre)

    for r in datos[:15]:
        print(r)


if __name__ == "__main__":
    mostrar("CONSULTA 1", consulta_1())
    mostrar("CONSULTA 2", consulta_2())
    mostrar("CONSULTA 3", consulta_3())
    mostrar("CONSULTA 4", consulta_4())
    mostrar("CONSULTA 5", consulta_5())
    mostrar("CONSULTA 6", consulta_6())
    mostrar("CONSULTA 7", consulta_7())
    mostrar("CONSULTA 8", consulta_8())
    mostrar("CONSULTA 9", consulta_9())
    mostrar("CONSULTA 10", consulta_10())
    mostrar("CONSULTA 11", consulta_11())
    mostrar("CONSULTA 12", consulta_12())
    mostrar("CONSULTA 13", consulta_13())
    mostrar("CONSULTA 14", consulta_14())
    mostrar("CONSULTA 15", consulta_15())

    session.close()