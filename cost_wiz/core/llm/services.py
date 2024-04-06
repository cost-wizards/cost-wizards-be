from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from cost_wiz.core.instances.services import InstanceService
from cost_wiz.db import InstanceStat
from cost_wiz.llm.bedrock import get_text


class LLMService:

    def predict_cost(self, session: Session, instance_service: InstanceService, *, instance_id: int, account_id: int):
        instance = instance_service.get_instance(session, account_id=account_id, instance_id=instance_id)

        today = datetime.now()
        days_30_before = today - timedelta(days=30)

        data = (
            session.query(InstanceStat)
            .filter(
                InstanceStat.timestamp > days_30_before,
                InstanceStat.timestamp < today,
                InstanceStat.instance_id == instance_id,
            )
            .all()
        )

        columns = "timestamp, avg_cpu_usage, max_cpu_usage, min_cpu_usage, avg_mem_usage, max_mem_usage, min_mem_usage, avg_network_in, max_network_in, min_network_in, min_network_out, avg_network_out, max_network_out"
        _data = ""

        for d in data:
            _data += f"{d.timestamp}, {d.avg_cpu_usage}, {d.max_cpu_usage}, {d.min_cpu_usage}, {d.avg_mem_usage}, {d.max_mem_usage}, {d.min_mem_usage}, {d.avg_network_in}, {d.max_network_in}, {d.min_network_in}, {d.min_network_out}, {d.avg_network_out}, {d.max_network_out}\n"

        instance = instance.instance_type

        try:
            response = get_text(columns, _data, instance)
            return response
        except:
            raise HTTPException(status_code=400, detail="Could not process the request at the moment")
