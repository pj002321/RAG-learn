# FastAPI 애플리케이션입니다.

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api import ask, customers, products

WEB = Path(__file__).parent.parent / "web"

app = FastAPI(title="화장품 AI 관리자")

app.include_router(products.router)
app.include_router(customers.router)
app.include_router(ask.router)

# web 폴더의 html, css, js 를 그대로 내보냅니다.
app.mount("/web", StaticFiles(directory=WEB, html=True), name="web")


@app.get("/")
def home():
    return RedirectResponse("/web/")