import boto3
import logging
from cost_wiz.config.settings import EnvSettings
from cost_wiz.llm.prompt import get_prompt
from cost_wiz.llm.models.claude_3_with_text import Claude3Wrapper
logger = logging.getLogger(__name__)


def get_text(env: EnvSettings):
    client = boto3.client(service_name="bedrock-runtime",
                          aws_access_key_id=env.aws_access_key_id,
                          aws_secret_access_key=env.aws_secret_access_key,
                          aws_session_token=env.aws_secret_access_key,
                          region_name=env.aws_region_name)
    wrapper = Claude3Wrapper(client, logger)
    prompt = get_prompt()
    wrapper.invoke_claude_3_with_text(prompt)
