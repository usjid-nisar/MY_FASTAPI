from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


settings = Settings()

# Print loaded settings for debugging
print("Database Hostname:", settings.database_hostname)
print("Database Port:", settings.database_port)
print("Database Username:", settings.database_username)
print("Database Name:", settings.database_name)
print("Secret Key:", settings.secret_key)
print("Algorithm:", settings.algorithm)
print("Access Token Expire Minutes:", settings.access_token_expire_minutes)


print(settings.database_username)
