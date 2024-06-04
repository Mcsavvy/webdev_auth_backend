import dotenv
import os

dotenv.load_dotenv(".env")

JWT_SECRET = os.getenv("JWT_SECRET", "secret")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite")
