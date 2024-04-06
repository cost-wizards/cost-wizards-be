from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class EnvSettings(BaseSettings):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str

    db_username: str
    db_password: str
    db_name: str
    db_port: str
    db_host_name: str
    aws_region_name: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def get_db_url(self):
        SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
        return SQLALCHEMY_DATABASE_URL
        return f"postgresql+psycopg2://{self.db_username}:{self.db_password}@{self.db_host_name}:{self.db_port}/{self.db_name}"


env: EnvSettings = EnvSettings()
