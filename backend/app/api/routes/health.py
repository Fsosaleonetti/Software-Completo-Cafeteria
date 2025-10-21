from fastapi import APIRouter

router = APIRouter()


@router.get("/healthz", summary="Estado de la API")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
