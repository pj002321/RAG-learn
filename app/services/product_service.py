# Last updated: 2026-09-07
"""
상품 관련 업무 규칙을 담는 곳입니다.

API 는 여기를 부르고, 여기서 Repository 를 부릅니다.
지금은 category 유무로 조회 방법만 나눕니다.
"""

from app.repositories import product_repository


def get_products(db, category=None, limit=20):
    if category:
        return product_repository.find_by_category(db, category, limit)
    return product_repository.find_all(db, limit)
