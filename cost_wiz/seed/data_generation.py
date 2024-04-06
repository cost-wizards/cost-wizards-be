from cost_wiz.db import Account, Instance, InstanceStat
from datetime import datetime, timedelta
import pandas as pd
import random
import string
import re
from cost_wiz.config.settings import EnvSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

env: EnvSettings = EnvSettings()

# Directly define the database connection string
DATABASE_URL = f"postgresql://{env.db_username}:{env.db_password}@{env.db_host_name}:{env.db_port}/{env.db_name}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

payload = {
    'name': 'CostWizard',
    'access_key': "GG",
    'secret_key': "GG",
    'region': "GG",
    'session_key': "GG",
    'instance': {}
}

df = pd.read_csv('cost_wiz/seed/AmazonEC2InstanceComparison.csv')


def generate_random_instance_id():
    prefix = 'i-'
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    return prefix + suffix


flag = False
instance_count = 0
for index, row in df.iterrows():
    if any(sub in row.iloc[1] for sub in ['t2.large', 't3.micro', 't4.nano']):
        payload['instance'][instance_count] = {}
        payload['instance'][instance_count]['name'] = row.iloc[0]
        payload['instance'][instance_count]['instance_id'] = generate_random_instance_id()
        payload['instance'][instance_count]['instance_type'] = row.iloc[1]
        payload['instance'][instance_count]['instance_memory'] = row.iloc[2]
        payload['instance'][instance_count]['vcpu'] = re.sub(r'\s{2,}', ' ', row.iloc[3])
        payload['instance'][instance_count]['network_performance'] = row.iloc[5]
        payload['instance'][instance_count]['on_demand_price'] = row.iloc[6]

        end_date = datetime.now() - timedelta(days=1)
        start_date = end_date - timedelta(days=3 * 365)
        timestamps = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in
                      pd.date_range(start=start_date, end=end_date, freq='H').to_list()]
        payload['instance'][instance_count]['instance_stats'] = {}
        gg = 0
        for count, timestamp in enumerate(timestamps):
            print(f"Adding for {row.iloc[0]}-{count}")
            payload['instance'][instance_count]['instance_stats'][count] = {}
            payload['instance'][instance_count]['instance_stats'][count]['timestamp'] = timestamp

            cpu_usage = [random.uniform(0.1, 60) for _ in range(360)]
            payload['instance'][instance_count]['instance_stats'][count]['avg_cpu_usage'] = sum(cpu_usage) / len(
                cpu_usage)
            payload['instance'][instance_count]['instance_stats'][count]['max_cpu_usage'] = max(cpu_usage)
            payload['instance'][instance_count]['instance_stats'][count]['min_cpu_usage'] = min(cpu_usage)

            mem_usage = [random.uniform(15, 80) for _ in range(360)]
            payload['instance'][instance_count]['instance_stats'][count]['avg_mem_usage'] = sum(mem_usage) / len(
                mem_usage)
            payload['instance'][instance_count]['instance_stats'][count]['max_mem_usage'] = max(mem_usage)
            payload['instance'][instance_count]['instance_stats'][count]['min_mem_usage'] = min(mem_usage)

            network_in = [random.uniform(1660, 65000000) for _ in range(360)]
            payload['instance'][instance_count]['instance_stats'][count]['avg_network_in'] = sum(network_in) / len(
                network_in)
            payload['instance'][instance_count]['instance_stats'][count]['max_network_in'] = max(network_in)
            payload['instance'][instance_count]['instance_stats'][count]['min_network_in'] = min(network_in)

            network_out = [random.uniform(5600, 300000) for _ in range(360)]
            payload['instance'][instance_count]['instance_stats'][count]['avg_network_out'] = sum(network_out) / len(
                network_out)
            payload['instance'][instance_count]['instance_stats'][count]['max_network_out'] = max(network_out)
            payload['instance'][instance_count]['instance_stats'][count]['min_network_out'] = min(network_out)
            gg += 1
            if gg > 1:
                flag = True
                break
        if flag:
            break
        instance_count += 1


def insert_payload(payload):
    with SessionLocal() as session:
        # Insert Account details
        account = Account(
            name=payload['name'],
            access_key=payload['access_key'],
            secret_key=payload['secret_key'],
            region=payload['region'],
            session_key=payload['session_key'],
            has_account_setup=True
        )
        session.add(account)
        session.flush()

        # Insert Instance details and stats
        for i, instance_details in payload['instance'].items():
            instance_dict = {
                "name": instance_details['name'],
                "instance_id": instance_details['instance_id'],
                "instance_type": instance_details['instance_type'],
                "vcpu": instance_details['vcpu'],
                "instance_memory": instance_details['instance_memory'],
                "network_performance": instance_details['network_performance'],
                "on_demand_price": instance_details['on_demand_price'],
                "status": "active",
                "account_id": account.id
            }
            inst = Instance(**instance_dict)
            session.add(inst)
            session.flush()

            # Insert InstanceStat details
            for j, stat in payload['instance']['instance_stats'].items():
                instance_stat = InstanceStat(
                    instance_id=inst.instance_id,
                    timestamp=stat['timestamp'],
                    avg_cpu_usage=stat['avg_cpu_usage'],
                    max_cpu_usage=stat['max_cpu_usage'],
                    min_cpu_usage=stat['min_cpu_usage'],
                    avg_mem_usage=stat['avg_mem_usage'],
                    max_mem_usage=stat['max_mem_usage'],
                    min_mem_usage=stat['min_mem_usage'],
                    avg_network_in=stat['avg_network_in'],
                    max_network_in=stat['max_network_in'],
                    min_network_in=stat['min_network_in'],
                    avg_network_out=stat['avg_network_out'],
                    max_network_out=stat['max_network_out'],
                    min_network_out=stat['min_network_out']
                )
                session.add(instance_stat)
        session.commit()


insert_payload(payload=payload)
