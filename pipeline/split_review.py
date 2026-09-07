import csv
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"
PURCHASES = DATA / "purchases.csv"
REVIEWS = DATA / "reviews.csv"

PURCHASE_COLUMNS = ["purchase_id", "customer_id", "product_id", "purchased_at", "quantity"]
REVIEW_COLUMNS = ["review_id", "purchase_id", "customer_id", "product_id", "rating", "content", "written_at"]

def read_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

print(read_csv(PURCHASES))