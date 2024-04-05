from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class EnvSettings(BaseSettings):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
