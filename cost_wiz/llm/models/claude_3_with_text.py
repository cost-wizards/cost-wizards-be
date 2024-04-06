import json
import re

from botocore.exceptions import ClientError


class Claude3Wrapper:
    def __init__(self, client, logger):
        self.client = client
        self.logger = logger
        self.model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

    def invoke_claude_3_with_text(self, prompt, max_tokens=2048):
        try:
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(
                    {
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": max_tokens,
                        "messages": [
                            {
                                "role": "user",
                                "content": [{"type": "text", "text": prompt}],
                            }
                        ],
                    }
                ),
            )
            result = json.loads(response.get("body").read())
            input_tokens = result["usage"]["input_tokens"]
            output_tokens = result["usage"]["output_tokens"]
            output_list = result.get("content", [])

            self.logger.success("Invocation details:")
            self.logger.success(f"- The input length is {input_tokens} tokens.")
            self.logger.success(f"- The output length is {output_tokens} tokens.")
            self.logger.success(f"- The model returned {len(output_list)} response(s):")
            for output in output_list:
                self.logger.info(output["text"])

            if "```json" in output_list[0]["text"]:
                return json.loads(re.search(r"```json(.*?)```", output_list[0]["text"], re.DOTALL).group(1).strip())
            else:
                return json.loads(output_list[0]["text"])
        except ClientError as err:
            self.logger.error(f"Couldn't invoke Claude 3 Sonnet. Here's why: {err}")
            raise err
