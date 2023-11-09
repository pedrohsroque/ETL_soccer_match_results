import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class Extractor():
    def __init__(self) -> None:
        pass

    def get_round_number(self, driver):
        round_element = driver.find_element(by=By.XPATH,value='//*[@id="classificacao__wrapper"]/section/nav/span[2]')
        return int(round_element.text.split('ª')[0])

    def get_matches(self, driver):
        return driver.find_elements(by=By.CLASS_NAME,value="lista-jogos__jogo")

    def go_to_previous_round(self, driver):
        navigation = driver.find_elements(by=By.TAG_NAME,value="nav")[0]
        navigation.find_elements(by=By.TAG_NAME,value="span")[0].click()
        time.sleep(3)

    def get_teams(self, match):
        meta_info = match.find_elements(by=By.TAG_NAME,value="meta")
        return meta_info[0].get_attribute("content")

    def get_date_time(self, match):
        meta_info = match.find_elements(by=By.TAG_NAME,value="meta")
        return meta_info[1].get_attribute("content")

    def get_result(self, match):
        return match.find_element(by=By.CLASS_NAME,value="placar-box").text.replace('\n',' x ')

    def get_match_info(self, match, round_number):
        teams = self.get_teams(match)
        date_time = self.get_date_time(match)
        result = self.get_result(match)
        return {
            'round':round_number,
            'teams':teams,
            'date_time':date_time,
            'result':result,
        }

    def get_matches_info(self, matches, round_number):
        matches_list=[]
        for match in matches:
            match_info = self.get_match_info(match, round_number)
            matches_list.append( match_info )
        print(f'Round: {round_number} | Captured matches: {len(matches_list)}')
        return matches_list

    def get_championship_data(self, championship):
        # Initial parameters
        url = f'https://ge.globo.com/futebol/{championship}/'
        round_number = 0
        all_matches_info = []

        print(f'Getting data for {championship}')
        with webdriver.Chrome(service=Service()) as gc:
            gc.minimize_window()
            gc.maximize_window()
            gc.get(url)
            while round_number != 1:
                round_number = self.get_round_number(gc)
                round_matches = self.get_matches(gc)
                round_matches_info = self.get_matches_info(round_matches, round_number)
                all_matches_info.extend( round_matches_info )
                self.go_to_previous_round(gc)
        return all_matches_info

    def save_data(self, data, championship):
        field_names = data[0].keys()
        with open(f'data/{championship}.csv', mode='w', newline='',encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(data)
