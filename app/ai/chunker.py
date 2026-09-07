def split_detail(product_name, detail):
    """상품 상세 문서를 ## 섹션 단위로 자릅니다."""
    sections = []

    for block in detail.split("\n## "):
        block = block.strip()
        if block.startswith("## "):
            block = block[3:]  # 맨 첫 섹션에만 "## " 가 남아 있습니다
        if not block:
            continue

        title, _, body = block.partition("\n")
        title = title.strip()
        sections.append(
            {
                "section": title,
                "content": f"{product_name} - {title}\n{body.strip()}",
            }
        )

    return sections