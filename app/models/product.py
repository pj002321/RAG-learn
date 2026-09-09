# 상품 테이블

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(String, primary_key=True)
    name = Column(String)
    brand = Column(String)
    category = Column(String)
    price = Column(Integer)
    volume = Column(String)
    skin_type = Column(String)
    ingredient = Column(String)
    concern = Column(String)
    tags = Column(String)

    # 짧은 소개글 (3~4문장). 자를 게 없어서 청킹하지 않습니다.
    description = Column(Text)

    # 긴 상세 문서 (평균 1370자, ## 로 나뉜 9개 섹션). RAG 의 주력 재료입니다.
    detail = Column(Text)

    # 등록 시각입니다. "값이 있다 = 우리가 등록한 신상품" 이 됩니다.
    # 신상품 여부를 따로 표시하는 컬럼을 만들지 않아도 되는 이유입니다.
    #
    # default=datetime.now 를 주지 않습니다. 그러면 pipeline/load_data.py 가
    # CSV 200개를 넣을 때도 시각이 찍혀서 전부 신상품이 되어 버립니다.
    # created_at=None 을 명시해도 소용없습니다. SQLAlchemy 는 그때도 기본값을 씁니다.
    # 그래서 시각은 등록하는 자리(product_service.create_product)에서 직접 찍습니다.
    created_at = Column(DateTime)