from fastapi import APIRouter, status

router = APIRouter(tags=["Health"])


@router.get("/health", status_code=status.HTTP_200_OK)
def read_health() -> dict[str, str]:
    return {"status": "ok", "message": "Serviço operacional"}
