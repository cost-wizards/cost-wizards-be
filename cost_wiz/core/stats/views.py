from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from cost_wiz.core.stats.services import StatService
from cost_wiz.deps import get_db

router = APIRouter()


@router.get("/instance/{instance_id}/stats")
def predict_cost(
    instance_id: int,
    session: Session = Depends(get_db),
    service: StatService = Depends(),
):
    return service.get_stats(session, instance_id)
