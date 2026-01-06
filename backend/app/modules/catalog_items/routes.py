from fastapi import APIRouter, HTTPException, status

from app.core.config import get_settings

from .repository import (
    create_catalog_item,
    get_catalog_item,
    init_db,
    list_catalog_items,
    soft_delete_catalog_item,
    update_catalog_item,
)
from .schemas import CatalogItemCreate, CatalogItemOut, CatalogItemUpdate

router = APIRouter(prefix="/api/catalog-items", tags=["catalog-items"])


def _database_url() -> str:
    return get_settings().database_url


def init_module() -> None:
    init_db(_database_url())


@router.get("", response_model=list[CatalogItemOut])
def list_catalog_items_route() -> list[CatalogItemOut]:
    return list_catalog_items(_database_url())


@router.post("", response_model=CatalogItemOut, status_code=status.HTTP_201_CREATED)
def create_catalog_item_route(payload: CatalogItemCreate) -> CatalogItemOut:
    return create_catalog_item(_database_url(), payload)


@router.get("/{item_id}", response_model=CatalogItemOut)
def get_catalog_item_route(item_id: str) -> CatalogItemOut:
    item = get_catalog_item(_database_url(), item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Catalog item not found")
    return item


@router.put("/{item_id}", response_model=CatalogItemOut)
def update_catalog_item_route(item_id: str, payload: CatalogItemUpdate) -> CatalogItemOut:
    item = update_catalog_item(_database_url(), item_id, payload)
    if not item:
        raise HTTPException(status_code=404, detail="Catalog item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_catalog_item_route(item_id: str) -> None:
    deleted = soft_delete_catalog_item(_database_url(), item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Catalog item not found")
    return None
