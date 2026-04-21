from fastapi import APIRouter

from db import check_db_connection

router = APIRouter(
  prefix="/health",
  tags=["Health"])


@router.get("/")
def health_check():
  return {"status": "ok"}

@router.get("/db")
def db_health_check():
  db_ok = check_db_connection()

  if db_ok:
    return {
      "status": "ok",
      "database": "connected"
    }

  return {
    "status": "error",
    "database": "not connected"
  }