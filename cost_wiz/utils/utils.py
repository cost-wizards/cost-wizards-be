import datetime

import boto3

AWS_PRICES = {
    "t2.micro": {"price": 0.0116, "memory": "1GB"},
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
                    "cpu": instance["CpuOptions"]["CoreCount"],
                    "ram": AWS_PRICES.get(instance["InstanceType"], {}).get("memory"),
                    "price": AWS_PRICES.get(instance["InstanceType"], {}).get("price"),
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

    # Format the dates as strings
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # Retrieve billing information
    response = ce_client.get_cost_and_usage(
        TimePeriod={"Start": start_date_str, "End": end_date_str},
        Granularity="DAILY",  # You can change the granularity as needed (e.g., HOURLY, MONTHLY)
        Metrics=["BlendedCost"],  # You can specify other metrics like UnblendedCost, AmortizedCost, etc.
    )

    # Print the billing information
    for result_by_time in response["ResultsByTime"]:
        total_cost = result_by_time["Total"]["BlendedCost"]["Amount"]
        print(f"Date: {result_by_time['TimePeriod']['Start']} - Total Cost: {total_cost}")
