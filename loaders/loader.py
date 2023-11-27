import csv
import os

import psycopg2

from config.config import db_credentials


class Loader():
    def __init__(self, db_credentials) -> None:
        self.db_credentials = db_credentials
        self.connection = self.create_connection()
        self.cursor = self.create_cursor()

    def create_connection(self):
        return psycopg2.connect(**self.db_credentials)

    def create_cursor(self):
        return self.connection.cursor()

    def create_table(self, csv_path, table_name, schema='raw'):
        with open(csv_path, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            create_table_query = f"CREATE TABLE IF NOT EXISTS {schema}.{table_name} ({', '.join(f'{col} TEXT' for col in header)})"
            self.cursor.execute(create_table_query)
            #self.connection.commit()

    def delete_from_table(self, table_name, schema='raw'):
        delete_query = f"delete from {schema}.{table_name}"
        self.cursor.execute(delete_query)

    # Not working
    def copy_data_from_csv(self, csv_path, table_name, schema='raw'):
        copy_data_query = f"COPY {schema}.{table_name}(round,teams,date_time,result) FROM '{csv_path}' WITH CSV HEADER DELIMITER ','"
        self.cursor.execute(copy_data_query)

    def insert_data_from_csv(self, csv_path, table_name, schema='raw'):
        with open(csv_path, 'r', encoding='utf-8', newline='\n') as f:
            csv_reader = csv.reader(f)
            header = next(csv_reader)
            lines = f.readlines()
            for line in lines:
                insert_query = f"""
                    insert into {schema}.{table_name} ({', '.join(f'{col}' for col in header)})
                    values ( {line} );
                """
                self.cursor.execute(insert_query)
        print(f"Dados inseridos na tabela {schema}.{table_name}")

if __name__ == '__main__':
    loader = Loader(db_credentials)
    files = os.listdir('data/')
    for file in files:
        full_path = f'data/{file}'
        table_name = file.replace('.csv','').replace('-','_').replace(' ','_')

        loader.create_table(full_path, table_name)
        loader.delete_from_table(table_name)
        loader.insert_data_from_csv(full_path, table_name)
        #loader.copy_data_from_csv(full_path, table_name)
        loader.connection.commit()
