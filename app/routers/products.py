from enum import Enum
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from app.models import Product, ProductPage
from app.repository import get_product, search_products

router = APIRouter(prefix="/products", tags=["products"])


class SortField(str, Enum):
    name = "name"
    price = "price"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


@router.get("", response_model=ProductPage)
def read_products(
    q: Annotated[str | None, Query()] = None,
    sort: Annotated[SortField | None, Query()] = None,
    order: Annotated[SortOrder, Query()] = SortOrder.asc,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=20)] = 20,
) -> ProductPage:
    matches = search_products(
        q=q,
        sort=sort.value if sort is not None else None,
        order=order.value,
    )
    start = (page - 1) * page_size
    items = matches[start : start + page_size]
    return ProductPage(
        items=items,
        total=len(matches),
        page=page,
        page_size=page_size,
    )


@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int) -> Product:
    product = get_product(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product
