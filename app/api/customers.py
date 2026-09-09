# 고객 관련 HTTP 엔드포인트입니다.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.customer import CustomerDetailOut, CustomerOut
from app.services import customer_service

router = APIRouter()


@router.get("/customers", response_model=list[CustomerOut])
def get_customers(skin_type: str = None, limit: int = 20, db: Session = Depends(get_db)):
    return customer_service.get_customers(db, skin_type, limit)


@router.get("/customers/{customer_id}", response_model=CustomerDetailOut)
def get_customer_detail(customer_id: str, db: Session = Depends(get_db)):
    detail = customer_service.get_customer_detail(db, customer_id)

    if detail is None:
        raise HTTPException(status_code=404, detail="그런 고객 번호가 없습니다.")

    return detail