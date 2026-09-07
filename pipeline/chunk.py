# Last updated: 2026-09-07
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


def print_result(db):
    total = db.query(Chunk).count()
    products = db.query(Chunk).filter(Chunk.source == "product").count()
    reviews = db.query(Chunk).filter(Chunk.source == "review").count()
    print("청킹 완료")
    print(f"  청크 {total}개  (상품 {products}개 + 후기 {reviews}개)")

    sample = db.query(Chunk).filter(Chunk.source == "product").first()
    if sample:
        print()
        print("  예시 :", sample.content.splitlines()[0])


if __name__ == "__main__":
    main()