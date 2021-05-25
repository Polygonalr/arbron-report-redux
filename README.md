# arbron-router-redux

#### _Because storing xlsx files in a bucket is very inefficient._

This aims to replace a weirdly-written private project called arbron-router that isn't on Github. The intend of this project is to generate reports of hashes of malicious files so that we can send it to people at Deer Hill.

A change from the original project is storing raw data of reports within SQLite instead of directly storing the `xlsx` report files in Minio. This allows easier maintenance and extrapolation of data.

## Running
---
### Directly with Python

The whole thing is built around Flask with SQLAlchemy (using SQLite backend), making set-up as hassle-free as possible.

1. Make sure you have at least __Python 3.6__ installed.
2. (Optional) Create a virtual environment with `venv`.
3. Do `pip install -r requirements.txt` to install the necessary components.
4. Rename `.env.example` to `.env`. Configure `.env` file if needed. Default values are fine.
5. Execute `python initialize_database.py` to create the SQLite db file.
6. Execute `flask run` to run the development server.

Follow [Flask's deployment guide](https://flask.palletsprojects.com/en/2.0.x/tutorial/deploy/) to deploy the project to production instead.

### Docker

`docker build . --tag arbron-report-redux`

## Options
---
These are the options that can be changed in `.env` file.
| Name | Default | Description |
| --- | --- | --- |
| `SQLALCHEMY_DATABASE_FILENAME` | `app.db` | Name of the SQLite database file to be created. |
