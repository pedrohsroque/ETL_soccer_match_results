from src.extractor import Extractor
from src.loader import Loader

extractor = Extractor()

championships_list = ['brasileirao-serie-a','brasileirao-serie-b']
for championship in championships_list:
    championship_data = extractor.get_championship_data(championship)
    extractor.save_data(championship_data, championship)
