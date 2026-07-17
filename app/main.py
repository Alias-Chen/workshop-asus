from fastapi import FastAPI

from app.routers import products, reports

app = FastAPI(
    title="ASUS Product Catalog",
    version="1.0.0",
    description="Sample API for the ASUS AI Coding Agent Workshop.",
)

app.include_router(products.router)
app.include_router(reports.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
