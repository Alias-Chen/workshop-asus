from typing import Annotated, Literal

from fastapi import APIRouter, HTTPException, Query, status

from app.models import Product, ProductPage
from app.repository import get_product, list_products

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=ProductPage)
def read_products(
    q: str | None = None,
    sort: Annotated[Literal["name", "price"] | None, Query()] = None,
    order: Annotated[Literal["asc", "desc"], Query()] = "asc",
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=20)] = 20,
) -> ProductPage:
    items, total = list_products(q=q, sort=sort, order=order, page=page, page_size=page_size)
    return ProductPage(items=items, total=total, page=page, page_size=page_size)


@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int) -> Product:
    product = get_product(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product
