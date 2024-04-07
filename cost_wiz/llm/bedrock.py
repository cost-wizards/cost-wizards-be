import boto3
from loguru import logger

from cost_wiz.config.settings import env
from cost_wiz.llm.models.claude_3_with_text import Claude3Wrapper
from cost_wiz.llm.prompt import get_prompt


def get_text(columns, data, instance):
    client = boto3.client(
        service_name="bedrock-runtime",
        aws_access_key_id=env.aws_access_key_id,
        aws_secret_access_key=env.aws_secret_access_key,
        aws_session_token=env.aws_session_token,
        region_name=env.aws_region_name,
    )
    wrapper = Claude3Wrapper(client, logger)
    prompt = get_prompt(data=data, instance=instance)
    return wrapper.invoke_claude_3_with_text(prompt)


# columns = """timestamp,Average_CPUUtilization,Maximum_CPUUtilization,Minimum_CPUUtilization"""
# data = """
#             timestamp,Average_CPUUtilization,Maximum_CPUUtilization,Minimum_CPUUtilization
#             2024-03-10,0.2393241832,0.5084095948,0.2083472231
#             2024-03-11,0.2198618488,0.2499333511,0.1999533442
#             2024-03-12,0.2630860413,2.760357596,0.1999666722
#             2024-03-13,0.2329128924,0.366568915,0.1917145953
#         """
# instance = "t3.nano"
# gg = get_text(columns=columns, data=data, instance=instance)
