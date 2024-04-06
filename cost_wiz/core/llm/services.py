from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from cost_wiz.core.instances.services import InstanceService
from cost_wiz.db import InstanceStat
from cost_wiz.llm.bedrock import get_text


class LLMService:

    def predict_cost(self, session: Session, instance_service: InstanceService, *, instance_id: int, account_id: int):
        instance = instance_service.get_instance(session, instance_id=instance_id)

        today = datetime.now()
        days_before = today - timedelta(days=90)

        data = (
            session.query(
                func.date_trunc("day", InstanceStat.timestamp).label("timestamp"),
                func.avg(InstanceStat.avg_cpu_usage),
                func.max(InstanceStat.max_cpu_usage),
                func.min(InstanceStat.min_cpu_usage),
                func.avg(InstanceStat.avg_mem_usage),
                func.max(InstanceStat.max_mem_usage),
                func.min(InstanceStat.min_mem_usage),
            )
            .filter(InstanceStat.timestamp.between(days_before, today))
            .group_by(func.date_trunc("day", InstanceStat.timestamp))
            .all()
        )
        columns = (
            "\ntimestamp, avg_cpu_usage, max_cpu_usage, min_cpu_usage, avg_mem_usage, max_mem_usage, min_mem_usage\n"
        )
        _data = columns
        for d in data:
            _data += f"{d[0].strftime('%Y-%m-%d %H:%M:%S')},{round(d[1], 2)},{round(d[2], 2)},{round(d[3], 2)},{round(d[4], 2)},{round(d[5], 2)},{round(d[6], 2)}\n"
        instance = instance.instance_type

        try:
            response = get_text(columns, _data, instance)
            return response
        except Exception as e:
            raise HTTPException(status_code=400, detail="Could not process the request at the moment")
