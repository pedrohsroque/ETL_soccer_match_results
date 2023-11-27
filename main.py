from unidecode import unidecode
from extractors.requests_extractor import RequestsExtractor
from loaders.loader import Loader
from config.config import db_credentials

def is_data_incomplete(filename: str) -> bool:
    with open(f"data/{filename}.csv", "r", encoding='utf-8') as f:
        return any(['None x None' in linha for linha in f.readlines()])

championships_list = []

extract_a = input("Extrair dados Série A? S/n ")
if extract_a == "S":
    championship_name = "Campeonato Brasileiro Série A 2023"
    if is_data_incomplete(championship_name):
        championships_list.append(championship_name)

extract_b = input("Extrair dados Série B? S/n ")
if extract_b == "S":
    championship_name = "Campeonato Brasileiro Série B 2023"
    if is_data_incomplete(championship_name):
        championships_list.append(championship_name)

extractor = RequestsExtractor()
for championship in championships_list:
    print(championship)
    championship_data = extractor.get_championship_data(championship)
    extractor.save_data(championship_data, championship)

load = input("Carregar dados? S/n ")
if load == "S":
    loader = Loader(db_credentials)
    files = [f"{championship}" for championship in championships_list]
    for file in files:
        full_path = f"data/{file}.csv"
        table_name = unidecode(file.replace('-','_').replace(' ','_').lower())
        loader.create_table(full_path, table_name)
        loader.delete_from_table(table_name)
        loader.insert_data_from_csv(full_path, table_name)
        loader.connection.commit()
