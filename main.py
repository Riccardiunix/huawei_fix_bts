from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time
IP='192.168.1.1'
PSW = '123456'
ENB_ID = 1111111
with Connection('http://admin:{}@{}/'.format(PSW,IP)) as connection:
    client = Client(connection)
    if (int(hex(int(client.device.signal()["cell_id"]))[0:-2], 16) != ENB_ID):
        options = Options()
        options.add_argument('--headless')
        options.page_load_strategy = 'eager'
        driver = webdriver.Firefox(options=options)
        driver.get('http://{}/html/index.html'.format(IP))
        print("Login")
        WebDriverWait(driver,10).until(EC.element_to_be_clickable( ("id","login_btn")))
        driver.find_element("id","login_password").send_keys(PSW)
        driver.find_element("id","login_btn").click()
        WebDriverWait(driver,10).until(EC.presence_of_element_located(("id","menu_top_home")))
        driver.get('http://{}/html/content.html#systemsettings'.format(IP))
        WebDriverWait(driver,10).until(EC.element_to_be_clickable(("id","antenna_control")))
        print("Antenna 1")
        driver.find_element("id","antenna_control").click()
        driver.find_element("id","antenna_mode_select").click()
        driver.find_element("id","antenna_mode_select_list_item_1").click()
        driver.find_element("id","antenna_save_button").click()
        count = 0
        while (int(hex(int(client.device.signal()["cell_id"]))[0:-2], 16) != ENB_ID or count > 10):
            time.sleep(1)
            count += 1
        WebDriverWait(driver,10).until(EC.visibility_of_element_located(("id","antenna_mode_select")))
        print("Antenna 2")
        flag = True
        while flag:
            try:
                driver.find_element("id","antenna_mode_select").click()
                driver.find_element("id","antenna_mode_select_list_item_2").click()
                driver.find_element("id","antenna_save_button").click()
                flag = False
            except Exception as e:
                time.sleep(1)
        driver.quit()
