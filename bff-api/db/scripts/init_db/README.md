# Connection Test

This script is used to initialise the database instance of [koyeb db](https://www.koyeb.com/docs/databases) called `mom-2025-team13-db`.

## Pre-requisites

To run this script you need to create a `.env` file in the same directory as this `README.md`.

The contents of the `.env` should be as follows:

```
DATABASE_HOST=ep-aged-forest-a2sd5mrk.eu-central-1.pg.koyeb.app
DATABASE_USER=koyeb-adm
DATABASE_PASSWORD=ASK_LARRY_IN_CHAT
DATABASE_NAME=koyebdb
DATA_PATH = "db/scripts/init-db/dist/your_data_file.csv"
MIGRATIONS_PATH = "db/migrations/V1__create_initial_schema.sql"
FLAG_INIT_DB=DISABLED
```

## Running

Navigate to the `bff-api` directory, execute `make init-db`.
