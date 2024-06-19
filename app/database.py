from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# PostgreSQL DB adapter:
# import psycopg2
# from psycopg2.extras import RealDictCursor


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:helloPostgresql@localhost/api_dev"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
# Function helps to get a connection to our Database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# DB stuff(psycopg2):
# while True:
#     try:
#         connnection = psycopg2.connect(
#             host="localhost",
#             dbname="api_dev",
#             user="postgres",
#             password="helloPostgresql",
#             cursor_factory=RealDictCursor,
#         )  # to also get 'col-names' along with rows.
#         cursor = connnection.cursor()
#         print("\nDatabase connection successfull!!\n")
#         break
#     except Exception as error:
#         print("\nDatabase connnection failed")
#         print(f"Error: {error}\n")
#         time.sleep(3)