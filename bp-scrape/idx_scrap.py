from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import firebase
import json

import idx_scrap_tab

options = webdriver.ChromeOptions()
options.add_argument('headless')

print("Starting..")

driver = webdriver.Chrome(
    '/usr/local/bin/chromedriver', chrome_options=options)
# driver = webdriver.Chrome('/Users/yopi/Tools/chromedriver')
# driver = webdriver.PhantomJS()
wait = WebDriverWait(driver, 60)


def start():
    driver.get(
        "http://idx.co.id/id-id/beranda/anggotabursaamppartisipan/profilanggotabursa.aspx"
    )

    driver.find_element_by_id('dnn_ctr541_MainView_rgBrokersProfile_ctl00_ctl04_LinkButton1').click()

    print("Waiting for detail profile..")

    wait.until(EC.presence_of_element_located((By.ID,"dnn_ctr541_MainView_lbBrokers")))

    # Position of NPWP

    # Process tab for first company
    idx_scrap_tab.renderFirstTab("PP", driver, wait)
    # idx_scrap_tab.renderTab(driver, wait, isFinished)

    print("===== Finished =====")

    data = firebase.getBrokers()
    data = json.dumps(data)
    brokerList = json.loads(data)

    for item in brokerList:
        code = item['Code']

        if (code == "PP"):
          continue
        
        # Temporary skip processing for MNC SEKURITAS
        if (code == "EP"):
          continue

        # Load first page in tab[0], by selecting dropdownlist
        print "Starting new scrape with code : ", code
        driver.execute_script(
            "document.getElementById('dnn_ctr541_MainView_radComboBoxBrokers_ClientState').setAttribute('value', '{\"logEntries\":[],\"value\":\"%s\",\"text\":\"BAHANA SEKURITAS\",\"enabled\":true,\"checkedIndices\":[],\"checkedItemsTextOverflows\":false}')"
            % (code))
        driver.execute_script("__doPostBack('dnn$ctr541$MainView$radComboBoxBrokers','{\"Command\":\"Select\",\"Index\":0}')")

        # Wait until page finished loading, by disappearance on element innerHTML in DOM
        print("Loading page..")
        npwpValue = driver.find_element_by_id('dnn_ctr541_MainView_lblDetNPWP').text
        wait.until_not(EC.text_to_be_present_in_element((By.ID, "dnn_ctr541_MainView_lblDetNPWP"), npwpValue))

        # Update company name
        companyName = driver.find_element_by_id('dnn_ctr541_MainView_lblDetName').get_attribute('innerHTML')
        npwp = driver.find_element_by_id('dnn_ctr541_MainView_lblDetNPWP').get_attribute('innerHTML')

        # Process tab for company in list
        print "The next company is : ", companyName
        idx_scrap_tab.renderTab(code, driver, wait, False)
        print("===== Finished =====")

        # Count company list
        # $('.rgInfoPart strong:first').text()

    assert "No results found." not in driver.page_source


def stop():
    driver.quit()