# Last updated: 2026-09-09
# 상품 테이블에 접근하는 곳입니다.

from datetime import datetime, timedelta

from sqlalchemy import desc, func

from app.models.product import Product


def find_all(db, limit=20):
    return db.query(Product).limit(limit).all()


def find_by_category(db, category, limit=20, sort=None):
    query = db.query(Product).filter(Product.category == category)
    if sort == "price_desc":
        query = query.order_by(desc(Product.price))
    elif sort == "price_asc":
        query = query.order_by(Product.price.asc())
    return query.limit(limit).all()


def find_by_id(db, product_id):
    return db.query(Product).filter(Product.product_id == product_id).first()


# 최근에 등록된 상품을 최신순으로 찾습니다.
def find_recent(db, limit=5, days=None):
    query = db.query(Product).filter(Product.created_at.isnot(None))

    if days:
        query = query.filter(Product.created_at >= datetime.now() - timedelta(days=days))

    return query.order_by(desc(Product.created_at)).limit(limit).all()


# 최근에 등록된 상품을 비싼 순으로 찾습니다.
def find_recent_expensive(db, limit=3, days=None):
    query = db.query(Product).filter(Product.created_at.isnot(None))

    if days:
        query = query.filter(Product.created_at >= datetime.now() - timedelta(days=days))

    return query.order_by(desc(Product.price), desc(Product.created_at)).limit(limit).all()


# 한 카테고리의 가격 통계를 한 줄로 냅니다.
def get_category_price_stats(db, category):
    return (
        db.query(
            func.count(Product.product_id).label("count"),
            func.avg(Product.price).label("avg_price"),
            func.min(Product.price).label("min_price"),
            func.max(Product.price).label("max_price"),
        )
        .filter(Product.category == category)
        .first()
    )


# 같은 카테고리에서 기준 가격보다 싼 상품을 비싼 순으로 찾습니다.
def find_cheaper_in_category(db, category, max_price, limit=3):
    return (
        db.query(Product)
        .filter(Product.category == category, Product.price < max_price)
        .order_by(desc(Product.price))
        .limit(limit)
        .all()
    )


def save(db, product):
    db.add(product)
    db.commit()
    return product