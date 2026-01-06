from fastapi import APIRouter, HTTPException, Response, status

from app.core.config import get_settings

from .repository import create_client, get_client, init_db, list_clients, soft_delete_client, update_client
from .schemas import ClientCreate, ClientOut, ClientUpdate

router = APIRouter(prefix="/api/clients", tags=["clients"])


def _database_url() -> str:
    return get_settings().database_url


def init_module() -> None:
    init_db(_database_url())


@router.get("", response_model=list[ClientOut])
def list_clients_route() -> list[ClientOut]:
    return list_clients(_database_url())


@router.post("", response_model=ClientOut, status_code=status.HTTP_201_CREATED)
def create_client_route(payload: ClientCreate) -> ClientOut:
    return create_client(_database_url(), payload)


@router.get("/{client_id}", response_model=ClientOut)
def get_client_route(client_id: str) -> ClientOut:
    client = get_client(_database_url(), client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.put("/{client_id}", response_model=ClientOut)
def update_client_route(client_id: str, payload: ClientUpdate) -> ClientOut:
    client = update_client(_database_url(), client_id, payload)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client_route(client_id: str) -> Response:
    deleted = soft_delete_client(_database_url(), client_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Client not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
