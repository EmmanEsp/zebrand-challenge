import boto3

from pydantic_settings import BaseSettings, SettingsConfigDict


class AWSSetting(BaseSettings):
    
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_default_region: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


def get_ses_client():
    aws_settings = AWSSetting()

    return boto3.client(
        "ses",
        aws_access_key_id=aws_settings.aws_access_key_id,
        aws_secret_access_key=aws_settings.aws_secret_access_key,
        region_name=aws_settings.aws_default_region
    )
