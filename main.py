from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time
IP='192.168.1.1'
PSW='123456'
ENB_ID=111111
with Connection(f'http://admin:{PSW}@{IP}/') as connection:
    client = Client(connection)
    enbid = int(hex(int(client.device.signal()["cell_id"]))[0:-2], 16)
    ant_type = int(client.device.antenna_set_type()['antennasettype'])
    if enbid != ENB_ID or ant_type != 2:
        options = Options()
        options.add_argument('--headless')
        options.page_load_strategy = 'eager'
        driver = webdriver.Firefox(options=options)
        driver.get(f'http://{IP}/html/index.html')
        print("Login")
        WebDriverWait(driver,15).until(EC.element_to_be_clickable( ("id","login_btn")))
        driver.find_element("id","login_password").send_keys(PSW)
        driver.find_element("id","login_btn").click()
        WebDriverWait(driver,15).until(EC.presence_of_element_located(("id","menu_top_home")))
        driver.get(f'http://{IP}/html/content.html#systemsettings')
        WebDriverWait(driver,15).until(EC.element_to_be_clickable(("id","antenna_control")))
        driver.find_element("id","antenna_control").click()
        if enbid != ENB_ID:
            print("Set Antenna EXT")
            driver.find_element("id","antenna_mode_select").click()
            driver.find_element("id","antenna_mode_select_list_item_1").click()
            driver.find_element("id","antenna_save_button").click()
            count = 0
            while (int(hex(int(client.device.signal()["cell_id"]))[0:-2], 16) != ENB_ID or count > 15):
                time.sleep(1)
                count += 1
            WebDriverWait(driver,15).until(EC.visibility_of_element_located(("id","antenna_mode_select")))
        print("Set Antenna INT")
        count = 0
        while count < 15:
            try:
                driver.find_element("id","antenna_mode_select").click()
                driver.find_element("id","antenna_mode_select_list_item_2").click()
                driver.find_element("id","antenna_save_button").click()
                count = 15
            except Exception as e:
                time.sleep(1)
                count += 1
        driver.quit()
