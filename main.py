from unidecode import unidecode
from src.requests_extractor import RequestsExtractor
from src.loader import Loader
from config.config import db_credentials

championships_list = [
    "Campeonato Brasileiro Série A 2023",
    "Campeonato Brasileiro Série B 2023",
]

extractor = RequestsExtractor()
for championship in championships_list:
    print(championship)
    championship_data = extractor.get_championship_data(championship)
    extractor.save_data(championship_data, championship)

loader = Loader(db_credentials)
files = [f"{championship}" for championship in championships_list]
for file in files:
    full_path = f"data/{file}.csv"
    table_name = unidecode(file.replace('-','_').replace(' ','_').lower())
    loader.create_table(full_path, table_name)
    loader.delete_from_table(table_name)
    loader.insert_data_from_csv(full_path, table_name)
    loader.connection.commit()
