import time

import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By

mysqlCon = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="123321",
    database="lol_op"
)
queue_type = ['ranked', 'flex', 'aram']
tier = ['all', 'iron', 'bronze', 'silver', 'gold', 'platinum', 'emerald', 'diamond', 'master', 'grandmaster',
        'challenger']


driver = webdriver.Chrome()

for q in queue_type:
    for t in tier:
        driver.get('https://www.op.gg/statistics/champions?mode=' + q + '&position=&tier=' + t)
        time.sleep(4)
        tr_list = driver.find_elements(By.XPATH, '//*[@id="content-container"]/div[2]/table/tbody/tr')
        for tr in tr_list:
            hero = tr.find_element(By.XPATH, './/td[2]/a/strong').text
            games_played = int(tr.find_element(By.XPATH, './/td[3]').text.replace(",", ""))
            kda = float(tr.find_element(By.XPATH, './/td[4]/span').text.replace(":1", ""))
            cs = float(tr.find_element(By.XPATH, './/td[8]').text)
            gold = float(tr.find_element(By.XPATH, './/td[9]').text.replace(",", ""))
            win = float(tr.find_element(By.XPATH, './/td[5]/div/div[2]').text.replace("%", ""))
            pick = float(tr.find_element(By.XPATH, './/td[6]/div/div[2]').text.replace("%", ""))
            ban = float(tr.find_element(By.XPATH, './/td[7]').text.replace("%", ""))
            cursor = mysqlCon.cursor()
            cursor.execute(
                "insert into analysis_hero_statistics(hero, games_played, kda, cs, gold, win, pick, ban, queue_type, tier, region) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (hero, games_played, kda, cs, gold, win, pick, ban, q, t, 'global'))
            mysqlCon.commit()





