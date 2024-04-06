import datetime

import boto3

AWS_PRICES = {
    "t2.micro": {
        "on_demand_price": "$0.0116 hourly",
        "instance_memory": "1GB",
        "network_performance": "Low to Moderate",
    },
    "t3.large": {
        "on_demand_price": "$0.0832 hourly",
        "instance_memory": "8GB",
        "network_performance": "Upto 5 Gigabit",
    },
}


def get_instances(access_key: str, secret_key: str, session_token: str, region: str):
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=session_token,
        region_name=region,
    )

    ec2_client = session.client("ec2")

    response = ec2_client.describe_instances()

    instances = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instances.append(
                {
                    "instance_id": instance["InstanceId"],
                    "instance_type": instance["InstanceType"],
                    "status": instance["State"]["Name"],
                    "vcpu": str(instance["CpuOptions"]["CoreCount"]),
                    "instance_memory": AWS_PRICES.get(instance["InstanceType"], {}).get("instance_memory"),
                    "on_demand_price": AWS_PRICES.get(instance["InstanceType"], {}).get("on_demand_price"),
                    "network_performance": AWS_PRICES.get(instance["InstanceType"], {}).get("network_performance"),
                }
            )

    return instances


def billing_data(access_key, secret_key, session_token, region):

    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=session_token,
        region_name=region,
    )

    ce_client = session.client("ce")

    # Set the time period for which you want to retrieve billing information
    start_date = datetime.datetime.utcnow() - datetime.timedelta(days=2)  # Example: last 30 days
    end_date = datetime.datetime.utcnow()

    request_params = {
        "TimePeriod": {"Start": start_date.strftime("%Y-%m-%d"), "End": end_date.strftime("%Y-%m-%d")},
        "Granularity": "MONTHLY",  # You can adjust the granularity as needed
        "Metrics": ["UnblendedCost"],
        "GroupBy": [{"Type": "DIMENSION", "Key": "SERVICE"}, {"Type": "DIMENSION", "Key": "INSTANCE_TYPE"}],
        "Filter": {
            "Dimensions": {"Key": "SERVICE", "Values": ["Amazon Elastic Compute Cloud - Compute"]}
        },  # Filter by EC2 service
    }

    # Get the cost and usage data
    response = ce_client.get_cost_and_usage(**request_params)

    total = 0
    # Process the response to extract cost data for EC2 instances
    for result_by_time in response["ResultsByTime"]:
        for group in result_by_time["Groups"]:
            cost = group["Metrics"]["UnblendedCost"]["Amount"]
            try:
                total += int(cost)
            except:
                total += 0

    return total
