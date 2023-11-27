import csv
import requests
import time


class RequestsExtractor():
    def __init__(self) -> None:
        pass

    def get_matches(self, round_number, championship):
        url = self.resolve_url(championship, round_number)
        r = requests.get(url)
        if r.status_code != 200:
            print(r.status_code)
            print(r.text)
            raise RuntimeError("Error during requests")
        return r.json()

    def get_teams(self, match):
        mandante = match["equipes"]["mandante"]["nome_popular"]
        visitante = match["equipes"]["visitante"]["nome_popular"]
        return f"{mandante} x {visitante}"

    def get_date_time(self, match):
        return match["data_realizacao"]

    def get_result(self, match):
        placar_mandante = match["placar_oficial_mandante"]
        placar_visitante = match["placar_oficial_visitante"]
        return f"{placar_mandante} x {placar_visitante}"

    def get_match_info(self, match, round_number):
        teams = self.get_teams(match)
        date_time = self.get_date_time(match)
        result = self.get_result(match)
        return {
            'round': f"'{round_number}'",
            'teams': f"'{teams}'",
            'date_time': f"'{date_time}'",
            'result': f"'{result}'",
        }

    def get_matches_info(self, matches, round_number):
        matches_list=[]
        for match in matches:
            match_info = self.get_match_info(match, round_number)
            matches_list.append( match_info )
        print(f'Round: {round_number} | Captured matches: {len(matches_list)}')
        return matches_list

    def resolve_url(self, championship, round_number):
        championships_dict = {
            "Campeonato Brasileiro Série A 2023":f'https://api.globoesporte.globo.com/tabela/d1a37fa4-e948-43a6-ba53-ab24ab3a45b1/fase/fase-unica-campeonato-brasileiro-2023/rodada/{round_number}/jogos/',
            "Campeonato Brasileiro Série A 2022":f'https://api.globoesporte.globo.com/tabela/d1a37fa4-e948-43a6-ba53-ab24ab3a45b1/fase/fase-unica-campeonato-brasileiro-2022/rodada/{round_number}/jogos/',
            "Campeonato Brasileiro Série B 2023":f'https://api.globoesporte.globo.com/tabela/009b5a68-dd09-46b8-95b3-293a2d494366/fase/brasileiro-serie-b-2023-fase-unica/rodada/{round_number}/jogos/',
        }
        return championships_dict[championship]

    def get_championship_data(self, championship):
        # Initial parameters
        all_matches_info = []
        print(f'Getting data for {championship}')
        for round_number_idx in range(38):
            round_number = round_number_idx + 1
            round_matches = self.get_matches(round_number=str(round_number), championship=championship)
            round_matches_info = self.get_matches_info(round_matches, round_number)
            all_matches_info.extend( round_matches_info )
            time.sleep(0.2)
        return all_matches_info

    def save_data(self, data, championship):
        field_names = data[0].keys()
        with open(f'data/{championship}.csv', mode='w', newline='',encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(data)

if __name__ == '__main__':
    extractor = RequestsExtractor()
    championships_list = ['campeonato-brasileiro-2023', 'campeonato-brasileiro-serie-b-2023']
    championships_list = ['campeonato-brasileiro-serie-b-2023']

    for championship in championships_list:
        championship_data = extractor.get_championship_data(championship)
        extractor.save_data(championship_data, championship)
