from app.models import Product

PRODUCTS = [
    Product(id=1, name="Zenbook 14 OLED", category="Laptop", price=42900),
    Product(id=2, name="ROG Zephyrus G14", category="Gaming Laptop", price=62900),
    Product(id=3, name="ProArt P16", category="Creator Laptop", price=79900),
    Product(id=4, name="TUF Gaming A15", category="Gaming Laptop", price=38900),
    Product(id=5, name="ROG Ally X", category="Handheld", price=26900),
    Product(id=6, name="ProArt Display PA279CRV", category="Monitor", price=15900),
]


def list_products(
    q: str | None = None,
    sort: str | None = None,
    order: str = "asc",
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[Product], int]:
    products: list[Product] = PRODUCTS.copy()
    if q:
        q_lower = q.lower()
        products = [
            p for p in products
            if q_lower in p.name.lower() or q_lower in p.category.lower()
        ]
    if sort:
        if sort not in ("name", "price"):
            raise ValueError(f"Invalid sort field: {sort!r}")
        products = sorted(
            products,
            key=lambda p: getattr(p, sort),
            reverse=(order == "desc"),
        )
    total = len(products)
    start = (page - 1) * page_size
    products = products[start : start + page_size]
    return products, total


def get_product(product_id: int) -> Product | None:
    return next((product for product in PRODUCTS if product.id == product_id), None)

