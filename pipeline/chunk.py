from app.ai.chunker import make_product_chunks, make_review_chunk
from app.db import Base, SessionLocal, engine
from app.models.chunk import Chunk
from app.models.product import Product
from app.models.review import Review


def main():
    Chunk.__table__.drop(engine, checkfirst=True)
    Base.metadata.create_all(engine)

    db = SessionLocal()
    products = db.query(Product).all()
    name_of = {product.product_id: product.name for product in products}

    for product in products:
        db.add_all(make_product_chunks(product))

    for review in db.query(Review).all():
        db.add(make_review_chunk(review, name_of[review.product_id]))

    db.commit()
    print_result(db)
    db.close()