from sqlalchemy import text

from database.connection import engine


try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()"))

        print("✅ PostgreSQL connection successful!")
        print(result.fetchone())

except Exception as e:
    print("❌ PostgreSQL connection failed!")
    print(e)