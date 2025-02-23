"""
This script reads event data from a CSV file and inserts it into a PostgreSQL database.
It uses the psycopg library to connect to the database and the loguru library for logging.
The script expects database credentials to be provided in a .env file.
Functions:
- insert_data(connection, csv_text): Inserts data from the CSV text into the database.
- main(): Main function that loads database credentials, connects to the database, and calls insert_data.

"""

import os

import psycopg
from dotenv import load_dotenv
from loguru import logger
from utils import insert_data, read_raw_data


def attempt_db_initialization(conn, migrations_path):
    with conn.cursor() as cur:
        logger.info("Creating tables")
        with open(migrations_path, "r", encoding="utf-8") as sql_file:
            sql_script = sql_file.read()
        cur.execute(sql_script)


def insert_raw_data(conn, init_data_path):
    csv_data = read_raw_data(init_data_path)
    insert_data(conn, csv_data, logger)
    logger.info("Data inserted successfully!")


def main():
    # Load database credentials from the .env file
    load_dotenv()
    db_name = os.getenv("DATABASE_NAME")
    db_user = os.getenv("DATABASE_USER")
    db_password = os.getenv("DATABASE_PASSWORD")
    db_host = os.getenv("DATABASE_HOST", "localhost")
    migrations_path = os.getenv("MIGRATIONS_PATH")
    init_data_path = os.getenv("DATA_PATH")
    flag_init_db = os.getenv("FLAG_INIT_DB")

    if not all(
        [
            db_name,
            db_user,
            db_password,
            db_host,
            migrations_path,
            init_data_path,
            flag_init_db,
        ]
    ):
        logger.error("Database credentials are not fully provided in the .env file")
        return

    dsn = f"dbname={db_name} user={db_user} password={db_password} host={db_host}"
    try:
        logger.info("Connecting to the database")
        with psycopg.connect(dsn) as conn:
            if flag_init_db == "ENABLED":
                attempt_db_initialization(conn, migrations_path)
            insert_raw_data(conn, init_data_path)
    except psycopg.Error:
        logger.exception("Error inserting data")


if __name__ == "__main__":
    main()
