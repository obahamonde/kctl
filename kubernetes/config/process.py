from pydantic import BaseSettings, Field, BaseConfig


class Settings(BaseSettings):
    class Config(BaseConfig):
        env_file = ".env"
        env_file_encoding = "utf-8"

    AWS_ACCESS_KEY_ID: str = Field(..., env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = Field(..., env="AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = Field(..., env="AWS_REGION")
    AWS_LAMBDA_ROLE: str = Field(..., env="AWS_LAMBDA_ROLE")
    AWS_S3_BUCKET: str = Field(..., env="AWS_S3_BUCKET")
    GITHUB_TOKEN: str = Field(..., env="GITHUB_TOKEN")
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    DOCKER_HOST: str = Field(..., env="DOCKER_HOST")
    FAUNA_SECRET:str = Field(..., env="FAUNA_SECRET")
env = Settings()
