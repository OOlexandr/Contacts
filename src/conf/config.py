from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str = 'postgresql+psycopg2://postgres:contactspassword@localhost:5432/postgres'
    secret_key: str = 'secret_key'
    algorithm: str = 'HS256'
    mail_username: str = 'artassmail@gmail.com'
    mail_password: str = 'eswlehvqcqjkktkk'
    mail_from: str = 'artassmail@gmail.com'
    mail_port: int = 465
    mail_server: str = 'smtp.gmail.com'
    redis_host: str = 'localhost'
    redis_port: int = 6379
    cloudinary_name: str = 'deyixrowa'
    cloudinary_api_key: str = '484422946837465'
    cloudinary_api_secret: str = '5knN_1ll5bFM_y5JK2aVPXH-w-k'

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = 'allow'


settings = Settings() #pyright: ignore