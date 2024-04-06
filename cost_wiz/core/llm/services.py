from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from cost_wiz.core.instances.services import InstanceService
from cost_wiz.db import Instance, InstanceStat


class LLMService:

    def predict_cost(self, session: Session, instance_service: InstanceService, *, instance_id: int):
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

        columns = "timestamp, avg_cpu_usage, max_cpu_usage, min_cpu_usage, avg_mem_usage, max_mem_usage, min_mem_usage, avg_network_in, max_network_in, max_network_in, min_network_out, avg_network_out, max_network_out"

        # print(data)
