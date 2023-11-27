This is a Data project.

1. Collects data from a brazilian sports' website.
2. Load the data into a CSV file and database.
3. Transform the data.
4. Reports the data.

- Extractor
    - Options
        1. It uses `selenium` to navigate throug the webpage, and to collect the data, which is stored in a CSV file.
        2. It uses `requests` to interact with the webpage, and to collect the data, which is stored in a CSV file.
- Loader
    - It uses `psycopg2` to load the CSV data into a `PostgreSQL` database.
- Transformer
    - It uses `dbt` to transform the raw data into a well defined data model.
    - It uses `pandas` to transform the raw data into a final table.
- Reporting
    - Options
        1. It uses `Power BI` to report the collected data.
        2. It uses `streamlit` to report the collected data.

Diagram:
    globoesporte -> CSV -> PostgreSQL (dbt) -> Power BI

Run the project:
- create a virtualenviroment
    - `python -m venv venv`
- Install the requirements
    - `pip install -r requirements.txt`
- Install PostgreSQL
- Set pythonpath
    - Powershell `$env:PYTHONPATH = $PWD`
- Run the code
    - `python main.py`
