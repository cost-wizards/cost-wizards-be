import re
from datetime import date, datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from cost_wiz.core.instances.services import InstanceService
from cost_wiz.db import Instance, InstanceStat


class StatService:

    def __get_cpu_utilization(self, session, _instance):
        end_date = date.today()
        start_date = end_date - timedelta(days=2)  # 90 days ago

        hourly_cpu_utilization = (
            session.query(
                InstanceStat.timestamp,
                func.extract("minute", InstanceStat.timestamp).label("minute"),
                func.avg(InstanceStat.avg_cpu_usage).label("avg_cpu_usage"),
                func.max(InstanceStat.max_cpu_usage).label("max_cpu_usage"),
                func.min(InstanceStat.min_cpu_usage).label("min_cpu_usage"),
            )
            .filter(InstanceStat.instance_id == _instance.instance_id)
            .filter(InstanceStat.timestamp.between(start_date, end_date))
            .group_by(InstanceStat.timestamp, func.extract("minute", InstanceStat.timestamp))
            .order_by(InstanceStat.timestamp)
            .all()
        )

        cpu_utilization = []
        for result in hourly_cpu_utilization:
            cpu_utilization.append(
                {
                    "timestamp": result.timestamp.strftime("%I:%M%p"),
                    "value": result.avg_cpu_usage,
                    "category": "avg_cpu_usage",
                }
            )
            cpu_utilization.append(
                {
                    "timestamp": result.timestamp.strftime("%I:%M%p"),
                    "value": result.max_cpu_usage,
                    "category": "max_cpu_usage",
                }
            )
            cpu_utilization.append(
                {
                    "timestamp": result.timestamp.strftime("%I:%M%p"),
                    "value": result.min_cpu_usage,
                    "category": "min_cpu_usage",
                }
            )

        return cpu_utilization

    def __get_memory_utilization(self, session, _instance):

        end_date = date.today()
        start_date = end_date - timedelta(days=2)  # 90 days ago

        hourly_memory_utilization = (
            session.query(
                InstanceStat.timestamp,
                func.extract("minute", InstanceStat.timestamp).label("minute"),
                func.avg(InstanceStat.avg_mem_usage).label("avg_mem_usage"),
                func.max(InstanceStat.max_mem_usage).label("max_mem_usage"),
                func.min(InstanceStat.min_mem_usage).label("min_mem_usage"),
            )
            .filter(InstanceStat.instance_id == _instance.instance_id)
            .filter(InstanceStat.timestamp.between(start_date, end_date))
            .group_by(InstanceStat.timestamp, func.extract("minute", InstanceStat.timestamp))
            .order_by(InstanceStat.timestamp)
            .all()
        )

        memory_utilization = []
        for result in hourly_memory_utilization:
            memory_utilization.append(
                {
                    "timestamp": result.timestamp.strftime("%I:%M%p"),
                    "value": result.avg_mem_usage,
                    "category": "avg_mem_usage",
                }
            )

            memory_utilization.append(
                {
                    "timestamp": result.timestamp.strftime("%I:%M%p"),
                    "value": result.max_mem_usage,
                    "category": "max_mem_usage",
                }
            )
            memory_utilization.append(
                {
                    "timestamp": result.timestamp.strftime("%I:%M%p"),
                    "value": result.min_mem_usage,
                    "category": "min_mem_usage",
                }
            )

        return memory_utilization

    def __get_cumulative_price(self, _instance):

        try:
            price = float(re.search(r"(\d+\.\d+)", _instance.on_demand_price).group(1))
        except:
            price = 0

        # Define the start and end timestamps
        end_timestamp = datetime.now()
        start_timestamp = end_timestamp - timedelta(days=2)  # Previous 3 months

        # Generate timestamps and calculate cumulative hourly prices
        timestamp = start_timestamp
        cumulative_prices = []
        cumulative_price = 0
        while timestamp <= end_timestamp:
            cumulative_price += price
            cumulative_prices.append((timestamp, cumulative_price))
            timestamp += timedelta(hours=1)

        data = []
        for timestamp, price in cumulative_prices:
            data.append({"timestamp": timestamp.strftime("%I:%M%p"), "value": price, "category": price})

        return data

    def get_stats(self, session: Session, instance_id: int):

        _instance = session.query(Instance).filter(Instance.id == instance_id).one_or_none()

        if not _instance:
            raise HTTPException(status_code=400, detail="No instance found")

        cpu_utilization = self.__get_cpu_utilization(session, _instance)
        memory_utilization = self.__get_memory_utilization(session, _instance)
        cumulative_price = self.__get_cumulative_price(_instance)

        return {"cpu": cpu_utilization, "memory": memory_utilization, "cumulative_price": cumulative_price}
