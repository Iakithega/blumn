
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def get_db_config() -> dict:
    db_config = {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT", "5432"),
        "database": os.getenv("DB_NAME"),
        "username": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }
    return db_config

def validate(db_config: dict) -> None:
    required = ("DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD")
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")

def build_url(db_config: dict) -> str:
    connection_string = (
        f"postgresql://{db_config['username']}:{db_config['password']}"
        f"@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    )
    return connection_string

def main() -> None:
    load_dotenv()  # load .env from project root
    db_cfg = get_db_config()
    validate(db_cfg)

    print(f"Connecting to {db_cfg['host']}:{db_cfg['port']} / {db_cfg['database']} as {db_cfg['username']}")
    engine = create_engine(build_url(db_cfg), echo=True, pool_pre_ping=True, pool_recycle=3600)

    try:
        with engine.connect() as conn:
            ok = conn.execute(text("SELECT 1")).scalar() == 1
            version = conn.execute(text("SELECT version()")).scalar()
            user = conn.execute(text("SELECT current_user")).scalar()
            print(f"SELECT 1 -> {'OK' if ok else 'FAILED'}")
            print(f"PostgreSQL version: {version}")
            print(f"Current user: {user}")
        print("✅ Success: database connection works.")
    except SQLAlchemyError as exc:
        print(f"❌ Connection failed: {exc}")
        raise

if __name__ == "__main__":
    main()