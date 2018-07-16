from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import firebase
import json


def start():
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')

    print("Starting..")

    driver = webdriver.Chrome(
        '/Users/yopi/Tools/chromedriver', chrome_options=options)
    # driver = webdriver.Chrome('/Users/yopi/Tools/chromedriver')
    # driver = webdriver.PhantomJS()
    wait = WebDriverWait(driver, 10)

    driver.get(
        "http://idx.co.id/id-id/beranda/anggotabursaamppartisipan/profilanggotabursa.aspx"
    )

    driver.find_element_by_id(
        'dnn_ctr541_MainView_rgBrokersProfile_ctl00_ctl04_LinkButton1').click(
        )
    print("Waiting for detail profile..")
    wait.until(
        EC.presence_of_element_located((By.ID,
                                        "dnn_ctr541_MainView_lbBrokers")))

    # Get initial profile page data
    companyName = driver.find_element_by_id(
        'dnn_ctr541_MainView_lblDetName').get_attribute('innerHTML')
    npwp = driver.find_element_by_id(
        'dnn_ctr541_MainView_lblDetNPWP').get_attribute('innerHTML')
    deedfCompany = driver.find_element_by_id(
        'dnn_ctr541_MainView_lblDetDeed').get_attribute('innerHTML')
    basicCapital = driver.find_element_by_id(
        'dnn_ctr541_MainView_lblDetAuthorizedCapital').get_attribute(
            'innerHTML')

    print companyName

    tab = 1
    for x in range(1, 4):
        driver.execute_script(
            "__doPostBack('dnn$ctr541$MainView$rtStripBrokers', '%s')" % (tab))

        print("Loading tab no %s.." % (tab))

        if (tab == 1):
            wait.until(
                EC.text_to_be_present_in_element(
                    (By.ID, "dnn_ctr541_MainView_lblAVGMKBD"),
                    "Rata-Rata MKBD"))

            time = driver.find_element_by_id(
                'dnn_ctr541_MainView_lblTime').get_attribute('innerHTML')

            print "Time : ", time
        elif (tab == 2):
            print "Tab : ", tab
        elif (tab == 3):
            print "Tab : ", tab

        tab = tab + 1

    print("===== Finished =====")

    data = firebase.getBrokers()
    data = json.dumps(data)
    x = json.loads(data)

    for item in x:
        code = item['Code']

        if (code == "PP"):
            continue

        print "Starting new scrape with code : ", code

        # Change to the next company profile
        # driver.find_element_by_id('dnn_ctr541_MainView_radComboBoxBrokers_Arrow').click()
        # driver.execute_script("document.getElementById('dnn_ctr541_MainView_radComboBoxBrokers_Input').setAttribute('value', 'BAHANA SEKURITAS')")
        asd = "document.getElementById('dnn_ctr541_MainView_radComboBoxBrokers_ClientState').setAttribute('value', '{\"logEntries\":[],\"value\":\"%s\",\"text\":\"BAHANA SEKURITAS\",\"enabled\":true,\"checkedIndices\":[],\"checkedItemsTextOverflows\":false}')" % (code)
        print asd
        driver.execute_script(asd)
        driver.execute_script(
            "__doPostBack('dnn$ctr541$MainView$radComboBoxBrokers','{\"Command\":\"Select\",\"Index\":0}')"
        )

        print("Loading page..")
        wait.until_not(
            EC.text_to_be_present_in_element(
                (By.ID, "dnn_ctr541_MainView_lblDetName"), companyName))

        # Get data from first tab
        companyName = driver.find_element_by_id(
            'dnn_ctr541_MainView_lblDetName').get_attribute('innerHTML')
        npwp = driver.find_element_by_id(
            'dnn_ctr541_MainView_lblDetNPWP').get_attribute('innerHTML')
        deedfCompany = driver.find_element_by_id(
            'dnn_ctr541_MainView_lblDetDeed').get_attribute('innerHTML')
        basicCapital = driver.find_element_by_id(
            'dnn_ctr541_MainView_lblDetAuthorizedCapital').get_attribute(
                'innerHTML')

        print "Company Name : ", companyName

        # tab = 1
        # for x in range(1, 4):
        #     # Selected tab in company profile
        #     # driver.execute_script(
        #     #     "$('#dnn_ctr541_MainView_rtStripBrokers').find('li a')[%s].setAttribute('class','rtsLink rtsSelected')"
        #     #     % (tab))
        #     driver.execute_script(
        #         "__doPostBack('dnn$ctr541$MainView$rtStripBrokers', '%s')" %
        #         (tab))

        #     print("Loading tab no %s.." % (tab))
        #     if (tab == 1):
        #         wait.until(
        #             EC.text_to_be_present_in_element(
        #                 (By.ID, "dnn_ctr541_MainView_lblAVGMKBD"),
        #                 "Rata-Rata MKBD"))

        #         time = driver.find_element_by_id(
        #             'dnn_ctr541_MainView_lblTime').get_attribute('innerHTML')

        #         print "Time : ", time
        #     elif (tab == 2):
        #         print "Tab : ", tab
        #     elif (tab == 3):
        #         print "Tab : ", tab

        #     tab = tab + 1

        print("===== Finished =====")

        # Count company list
        # $('.rgInfoPart strong:first').text()

    assert "No results found." not in driver.page_source
