from app.models import Product

PRODUCTS = [
    Product(id=1, name="Zenbook 14 OLED", category="Laptop", price=42900),
    Product(id=2, name="ROG Zephyrus G14", category="Gaming Laptop", price=62900),
    Product(id=3, name="ProArt P16", category="Creator Laptop", price=79900),
    Product(id=4, name="TUF Gaming A15", category="Gaming Laptop", price=38900),
    Product(id=5, name="ROG Ally X", category="Handheld", price=26900),
    Product(id=6, name="ProArt Display PA279CRV", category="Monitor", price=15900),
]


def search_products(
    q: str | None = None,
    sort: str | None = None,
    order: str = "asc",
) -> list[Product]:
    products = PRODUCTS.copy()

    if q:
        needle = q.casefold()
        products = [
            product
            for product in products
            if needle in product.name.casefold() or needle in product.category.casefold()
        ]

    if sort is not None:
        reverse = order == "desc"
        products.sort(key=lambda product: getattr(product, sort), reverse=reverse)

    return products


def get_product(product_id: int) -> Product | None:
    return next((product for product in PRODUCTS if product.id == product_id), None)

