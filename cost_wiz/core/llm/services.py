from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from cost_wiz.core.instances.services import InstanceService
from cost_wiz.db import InstanceStat
from cost_wiz.llm.bedrock import get_text


class LLMService:

    def predict_cost(self, session: Session, instance_service: InstanceService, *, instance_id: int, account_id: int):
        instance = instance_service.get_instance(session, account_id=account_id, instance_id=instance_id)

        today = datetime.now()
        days_30_before = today - timedelta(days=90)

        query = (
            session.query(
                InstanceStat.timestamp,
                func.avg(InstanceStat.avg_cpu_usage).label("avg_cpu_usage"),
                func.max(InstanceStat.max_cpu_usage).label("max_cpu_usage"),
                func.min(InstanceStat.min_cpu_usage).label("min_cpu_usage"),
                func.avg(InstanceStat.avg_mem_usage).label("avg_mem_usage"),
                func.max(InstanceStat.max_mem_usage).label("max_mem_usage"),
                func.min(InstanceStat.min_mem_usage).label("min_mem_usage"),
            )
            .filter(InstanceStat.timestamp.between(days_30_before, today))
            .group_by(InstanceStat.timestamp)
        )

        data = query.all()

        columns = (
            "timestamp, avg_cpu_usage, max_cpu_usage, min_cpu_usage, avg_mem_usage, max_mem_usage, min_mem_usage, n"
        )
        _data = "" + columns

        for d in data:
            _data += f"{d.timestamp}, {d.avg_cpu_usage}, {d.max_cpu_usage}, {d.min_cpu_usage}, {d.avg_mem_usage}, {d.max_mem_usage}, {d.min_mem_usage}\n"

        instance = instance.instance_type

        try:
            response = get_text(columns, _data, instance)
            return response
        except Exception as e:
            raise HTTPException(status_code=400, detail="Could not process the request at the moment")
