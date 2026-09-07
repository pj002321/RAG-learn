"""
벡터를 저장합니다.

chunks 테이블을 다루는 곳은 이 파일 하나뿐입니다. (pipeline 스크립트만 예외)
SQLite 와 Supabase 의 차이를 전부 이 파일 안에 가둬 두려는 것입니다.
마지막에 Supabase 로 옮길 때 고치는 파일이 여기 하나로 끝납니다.

지금은 SQLite 라서 벡터를 JSON 문자열로 저장합니다.
"""

import json

from app.models.chunk import Chunk


def find_chunks_to_embed(db):
    """아직 벡터가 없는 청크만 가져옵니다.

    이 함수 덕분에 나중에 증분 임베딩이 가능합니다.
    새 상품을 추가해도 그 상품의 청크만 벡터가 없으니, 그것만 임베딩하면 됩니다.
    """
    # SQLAlchemy 에서 "값이 비어 있다" 는 is None 이 아니라 is_(None) 으로 씁니다.
    return db.query(Chunk).filter(Chunk.embedding.is_(None)).all()


def save_embeddings(db, chunks, vectors):
    """청크에 벡터를 붙여 저장합니다."""
    for chunk, vector in zip(chunks, vectors):
        chunk.embedding = json.dumps(vector)
    db.commit()


def count_all(db):
    return db.query(Chunk).count()


def count_embedded(db):
    return db.query(Chunk).filter(Chunk.embedding.is_not(None)).count()


def find_first_embedded(db):
    """벡터가 어떻게 생겼는지 확인해 볼 때 씁니다."""
    return db.query(Chunk).filter(Chunk.embedding.is_not(None)).first()