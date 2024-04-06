from cost_wiz.config.settings import EnvSettings
from datetime import datetime, timedelta
import pandas as pd
import random
import string
import re
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

env: EnvSettings = EnvSettings()

payload = {
    'name': 'CostWizard',
    'access_key': "GG",
    'secret_key': "GG",
    'region': "GG",
    'session_key': "GG",
    'instance': {
        'instance_stats': {}
    }
}

df = pd.read_csv('cost_wiz/seed/AmazonEC2InstanceComparison.csv')


def generate_random_instance_id():
    prefix = 'i-'
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    return prefix + suffix


for index, row in df.iterrows():
    if any(sub in row.iloc[1] for sub in ['t2.large', 't3.micro', 't4.nano']):
        payload['instance']['name'] = row.iloc[0]
        payload['instance']['instance_id'] = generate_random_instance_id()
        payload['instance']['instance_type'] = row.iloc[1]
        payload['instance']['instance_memory'] = row.iloc[2]
        payload['instance']['vcpu'] = re.sub(r'\s{2,}', ' ', row.iloc[3])
        payload['instance']['network_performance'] = row.iloc[5]
        payload['instance']['on_demand_price'] = row.iloc[6]

        end_date = datetime.now() - timedelta(days=1)
        start_date = end_date - timedelta(days=3 * 365)
        timestamps = pd.date_range(start=start_date, end=end_date, freq='H').to_list()
        for count, timestamp in enumerate(timestamps):
            print(f"Executing for {row.iloc[0]}-{count}")
            payload['instance']['instance_stats'][count] = {}
            payload['instance']['instance_stats'][count]['timestamp'] = timestamp

            cpu_usage = [random.uniform(0.1, 60) for _ in range(360)]
            payload['instance']['instance_stats'][count]['avg_cpu_usage'] = sum(cpu_usage) / len(cpu_usage)
            payload['instance']['instance_stats'][count]['max_cpu_usage'] = max(cpu_usage)
            payload['instance']['instance_stats'][count]['min_cpu_usage'] = min(cpu_usage)

            mem_usage = [random.uniform(15, 80) for _ in range(360)]
            payload['instance']['instance_stats'][count]['avg_mem_usage'] = sum(mem_usage) / len(mem_usage)
            payload['instance']['instance_stats'][count]['max_mem_usage'] = max(mem_usage)
            payload['instance']['instance_stats'][count]['min_mem_usage'] = min(mem_usage)

            network_in = [random.uniform(1660, 65000000) for _ in range(360)]
            payload['instance']['instance_stats'][count]['avg_network_in'] = sum(network_in) / len(network_in)
            payload['instance']['instance_stats'][count]['max_network_in'] = max(network_in)
            payload['instance']['instance_stats'][count]['min_network_in'] = min(network_in)

            network_out = [random.uniform(5600, 300000) for _ in range(360)]
            payload['instance']['instance_stats'][count]['avg_network_out'] = sum(network_out) / len(network_out)
            payload['instance']['instance_stats'][count]['max_network_out'] = max(network_out)
            payload['instance']['instance_stats'][count]['min_network_out'] = min(network_out)

# Create an engine to connect to your database
engine = create_engine(f'postgresql://{env.db_username}:{env.db_password}@{env.db_host_name}:{env.db_port}/{env.db_name}')

# Create all defined tables in the database
Base.metadata.create_all(engine)

# Create a sessionmaker bound to the engine
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

# Create and insert Account instance
account = Account(
    id=payload["id"],
    name=payload["name"],
    access_key=payload["access_key"],
    secret_key=payload["secret_key"],
    region=payload["region"]
)
session.add(account)
session.commit()

# Create and insert Instance instance
instance = Instance(
    name=payload["instance"]["name"],
    account=account
)
session.add(instance)
session.commit()

# Create and insert InstanceStats instances
for key, stats in payload["instance"]["instance_stats"].items():
    instance_stat = InstanceStats(
        timestamp=stats["timestamp"],
        avg_cpu_usage=stats["avg_cpu_usage"],
        max_cpu_usage=stats["max_cpu_usage"],
        instance=instance
    )
    session.add(instance_stat)

# Commit the transaction
session.commit()

# Close the session
session.close()
print("Done Hai")
