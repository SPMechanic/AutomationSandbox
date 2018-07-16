from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from global_data import BrokerData
from colorama import init, Fore, Back, Style
import firebase
import json

init()


def renderFirstTab(code, driver, wait):
    # Processing tab[0] Profile
    image = driver.find_element_by_id('dnn_ctr541_MainView_imgBrokers').get_attribute('src')
    companyName = driver.find_element_by_id(
        'dnn_ctr541_MainView_lblDetName').text.rstrip()
    npwp = driver.find_element_by_id('dnn_ctr541_MainView_lblDetNPWP').text
    deed = driver.find_element_by_id('dnn_ctr541_MainView_lblDetDeed').text
    basicCapital = driver.find_element_by_id(
        'dnn_ctr541_MainView_lblDetAuthorizedCapital').get_attribute(
            'innerHTML')
    paidUpCapital = driver.find_element_by_id(
        'dnn_ctr541_MainView_lblDetPaidUpCapital').get_attribute('innerHTML')
    companyStatus = driver.find_element_by_id(
        'dnn_ctr541_MainView_lblDetCompanyStatus').text
    operationalStatus = driver.find_element_by_id(
        'dnn_ctr541_MainView_lblDetOperationalStatus').get_attribute(
            'innerHTML')
    permit1 = driver.find_element_by_id('dnn_ctr541_MainView_lblPermit1').text
    permit2 = driver.find_element_by_id('dnn_ctr541_MainView_lblPermit2').text
    permit3 = driver.find_element_by_id('dnn_ctr541_MainView_lblPermit3').text
    workPermit = permit1 + permit2 + permit3
    lastMKBD = driver.find_element_by_id(
        'dnn_ctr541_MainView_lblDetLastMKBD').get_attribute('innerHTML')

    BrokerData.profiles["image"] = image
    BrokerData.profiles["companyName"] = companyName
    BrokerData.profiles["npwp"] = npwp
    BrokerData.profiles["deed"] = deed
    BrokerData.profiles["basicCapital"] = filterDigit(basicCapital)
    BrokerData.profiles["paidUpCapital"] = filterDigit(paidUpCapital)
    BrokerData.profiles["companyStatus"] = companyStatus
    BrokerData.profiles["operationalStatus"] = operationalStatus
    BrokerData.profiles["workPermit"] = workPermit
    BrokerData.profiles["lastMKBD"] = filterDigit(lastMKBD)

    # Processing Dewan Manajemen table
    tables = driver.find_element_by_id("dnn_ctr541_MainView_rgBofM_ctl00")
    rows = tables.find_elements_by_tag_name('tr')
    rows.pop(0)
    managements = []
    for row in rows:
        cols = row.find_elements_by_tag_name('td')
        managements.append("{'name':'%s','position':'%s'}" %
                           (cols[0].get_attribute('innerHTML').rstrip().replace('\'',''),
                            cols[1].get_attribute('innerHTML')))

    BrokerData.profiles["managements"] = managements

    # Processing Pemegang Saham table
    tables = driver.find_element_by_id(
        "dnn_ctr541_MainView_rgPemilikSaham_ctl00")
    rows = tables.find_elements_by_tag_name('tr')
    rows.pop(0)
    ownerships = []
    for row in rows:
        cols = row.find_elements_by_tag_name('td')
        ownerships.append("{'name':'%s','ownership':'%s'}" %
                          (
                            cols[0].get_attribute('innerHTML').rstrip().replace('\'',''),
                            cols[1].get_attribute('innerHTML').rstrip().replace(',','.')
                          )
        )

    BrokerData.profiles["ownerships"] = ownerships

    # Looping start
    tables = driver.find_element_by_id("dnn_ctr541_MainView_rgMKBD_ctl00")
    rows = tables.find_elements_by_tag_name('tr')
    rows.pop(0)
    mkbds = []
    for row in rows:
        cols = row.find_elements_by_tag_name('td')
        mkbds.append("{'month':'%s','year1':'%s','year2':'%s','year3':'%s'}" %
                     (cols[0].get_attribute('innerHTML'),
                      filterDigit(cols[1].get_attribute('innerHTML')),
                      filterDigit(cols[2].get_attribute('innerHTML')),
                      filterDigit(cols[3].get_attribute('innerHTML'))))

    BrokerData.summaries["mkbds"] = mkbds

    # Looping start
    tables = driver.find_element_by_id(
        "dnn_ctr541_MainView_rgTotalTransaksi_ctl00")
    rows = tables.find_elements_by_tag_name('tr')
    rows.pop(0)
    transactions = []
    for row in rows:
        cols = row.find_elements_by_tag_name('td')
        transactions.append(
            "{'month':'%s','year1':'%s','year2':'%s','year3':'%s'}" %
            (cols[0].get_attribute('innerHTML'),
             filterDigit(cols[1].get_attribute('innerHTML')),
             filterDigit(cols[2].get_attribute('innerHTML')),
             filterDigit(cols[3].get_attribute('innerHTML'))))

    BrokerData.summaries['transactions'] = transactions

    # Processing Branch
    # driver.execute_script("__doPostBack('dnn$ctr541$MainView$rtStripBrokers', '%s')" % (3))

    # Looping start
    tables = driver.find_element_by_id(
        "dnn_ctr541_MainView_RadGridBranch_ctl00")
    emptyRows = tables.find_elements_by_class_name('rgNoRecords')
    pagerRows = tables.find_elements_by_class_name('rgPager')

    branches = []
    if (len(emptyRows) == 1):
        print 'BRANCH - EMPTY !'
        print 'Empty Rows Count: %s' % len(emptyRows)
        BrokerData.branches = []
    elif (len(pagerRows) == 1):
        print 'BRANCH - PAGING EXIST !'
        print 'RELOAD with Paging Excluded... !'

        # Find all branches count
        items = driver.find_element_by_xpath(
            '//*[@id="dnn_ctr541_MainView_RadGridBranch_ctl00"]/tfoot/tr/td/table/tbody/tr/td/div[5]/strong[1]'
        ).get_attribute('innerHTML')

        # Reload with all branches
        driver.execute_script(
            "__doPostBack('dnn$ctr541$MainView$RadGridBranch','FireCommand:dnn$ctr541$MainView$RadGridBranch$ctl00;PageSize;%s')"
            % items)

        # Wait until last branch row is present in page
        lastRowID = 'dnn_ctr541_MainView_RadGridBranch_ctl00__%s' % (int(items) - 1)
        lastRow = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, lastRowID)))

        # Start processing rows
        tables = driver.find_element_by_id(
            "dnn_ctr541_MainView_RadGridBranch_ctl00")
        rows = tables.find_elements_by_tag_name('tr')
        rows.pop(0)
        for row in rows:
            cols = row.find_elements_by_tag_name('td')
            colAddress = (cols[1].get_attribute('innerHTML')).replace('/','-').replace(',', '').replace('\n', ' ').encode('utf-8')
            colCity = (cols[2].get_attribute('innerHTML')).encode('utf-8')
            colZipcode = (cols[3].get_attribute('innerHTML')).encode('utf-8')
            colPhone = (cols[4].get_attribute('innerHTML')).encode('utf-8')
            colFax = (cols[5].get_attribute('innerHTML')).encode('utf-8')
            branches.append(
                "{'address':'%s','city':'%s','zipcode':'%s','phone':'%s','fax':'%s'}"
                % (colAddress, colCity, colZipcode, colPhone, colFax)
            )
        BrokerData.branches = branches
    else:
        rows = tables.find_elements_by_tag_name('tr')
        rows.pop(0)
        for row in rows:
            cols = row.find_elements_by_tag_name('td')
            colAddress = (cols[1].get_attribute('innerHTML')).replace('/','-').replace(',', '').replace('\n', ' ').encode('utf-8')
            colCity = (cols[2].get_attribute('innerHTML')).encode('utf-8')
            colZipcode = (cols[3].get_attribute('innerHTML')).encode('utf-8')
            colPhone = (cols[4].get_attribute('innerHTML')).encode('utf-8')
            colFax = (cols[5].get_attribute('innerHTML')).encode('utf-8')
            branches.append(
                "{'address':'%s','city':'%s','zipcode':'%s','phone':'%s','fax':'%s'}"
                % (colAddress, colCity, colZipcode, colPhone, colFax)
            )
        BrokerData.branches = branches

    # building json
    print("======= PREVIEW data from %s =======") % companyName
    # profile = "{'profile': %s}" % (BrokerData.profiles)
    # print (Style.BRIGHT + Fore.WHITE + Back.BLUE + "PROFILE" + Style.RESET_ALL + " = " + Style.DIM + Fore.CYAN + profile + Style.RESET_ALL)

    # summary = "{summary': %s}" % (BrokerData.summaries)
    # print (Style.DIM + Fore.WHITE + Back.GREEN + "SUMMARY" + Style.RESET_ALL + " = " + Style.DIM + Fore.CYAN + summary + Style.RESET_ALL)

    # branch = "{'branch': %s}" % (BrokerData.branches)
    # print (Style.DIM + Fore.WHITE + Back.MAGENTA + "BRANCH" + Style.RESET_ALL + " = " + Style.DIM + Fore.CYAN + branch + Style.RESET_ALL)

    data = "{'profile': %s, 'summary': %s,'branch': %s}" % (
        BrokerData.profiles, BrokerData.summaries, BrokerData.branches)
    # print "=====> Data : ", data

    code = firebase.getBrokerKeyByCode(code)
    BrokerData.brokers[code] = data


def renderTab(code, driver, wait, isFirstTab):
    if isFirstTab == False:
        renderFirstTab(code, driver, wait)
    tab = 1

    while (tab < 4):
        if (tab == 1):
            # Looping start
            tables = driver.find_element_by_id(
                "dnn_ctr541_MainView_rgMKBD_ctl00")
            rows = tables.find_elements_by_tag_name('tr')
            rows.pop(0)
            mkbds = []
            for row in rows:
                cols = row.find_elements_by_tag_name('td')
                mkbds.append(
                    "{'month':'%s','year1':'%s','year2':'%s','year3':'%s'}" %
                    (cols[0].get_attribute('innerHTML'),
                     filterDigit(cols[1].get_attribute('innerHTML')),
                     filterDigit(cols[2].get_attribute('innerHTML')),
                     filterDigit(cols[3].get_attribute('innerHTML'))))

            BrokerData.summaries['mkbds'] = mkbds

            # Looping start
            tables = driver.find_element_by_id(
                "dnn_ctr541_MainView_rgTotalTransaksi_ctl00")
            rows = tables.find_elements_by_tag_name('tr')
            rows.pop(0)
            transactions = []
            for row in rows:
                cols = row.find_elements_by_tag_name('td')
                transactions.append(
                    "{'month':'%s','year1':'%s','year2':'%s','year3':'%s'}" %
                    (cols[0].get_attribute('innerHTML'),
                     filterDigit(cols[1].get_attribute('innerHTML')),
                     filterDigit(cols[2].get_attribute('innerHTML')),
                     filterDigit(cols[3].get_attribute('innerHTML'))))

            BrokerData.summaries['transactions'] = transactions

        elif (tab == 2):
            print "*** Tab[%s] is still Under Construction ***" % (tab)
        elif (tab == 3):
            print "*** Tab[%s] is still Under Construction ***" % (tab)
            # Looping start
            tables = driver.find_element_by_id(
                "dnn_ctr541_MainView_RadGridBranch_ctl00")
            emptyRows = tables.find_elements_by_class_name('rgNoRecords')
            pagerRows = tables.find_elements_by_class_name('rgPager')

            branches = []
            if (len(emptyRows) == 1):
                print 'BRANCH - EMPTY !'
                print 'Empty Rows Count: %s' % len(emptyRows)
                BrokerData.branches = []
            elif (len(pagerRows) == 1):
                print 'BRANCH - PAGING EXIST !'
                print 'RELOAD with Paging Excluded... !'

                # Find all branches count
                items = driver.find_element_by_xpath(
                    '//*[@id="dnn_ctr541_MainView_RadGridBranch_ctl00"]/tfoot/tr/td/table/tbody/tr/td/div[5]/strong[1]'
                ).get_attribute('innerHTML')

                # Reload with all branches
                driver.execute_script(
                    '__doPostBack("dnn$ctr541$MainView$RadGridBranch","FireCommand:dnn$ctr541$MainView$RadGridBranch$ctl00;PageSize;%s")'
                    % items)

                # Wait until last branch row is present in page
                lastRowID = "dnn_ctr541_MainView_RadGridBranch_ctl00__%s" % (
                    int(items) - 1)
                lastRow = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, lastRowID)))

                # Start processing rows
                tables = driver.find_element_by_id(
                    "dnn_ctr541_MainView_RadGridBranch_ctl00")
                rows = tables.find_elements_by_tag_name('tr')
                rows.pop(0)
                for row in rows:
                    cols = row.find_elements_by_tag_name('td')
                    colAddress = (cols[1].get_attribute('innerHTML')).replace('/','-').replace(',', '').replace('\n', ' ').encode('utf-8')
                    colCity = (cols[2].get_attribute('innerHTML')).encode('utf-8')
                    colZipcode = (cols[3].get_attribute('innerHTML')).encode('utf-8')
                    colPhone = (cols[4].get_attribute('innerHTML')).encode('utf-8')
                    colFax = (cols[5].get_attribute('innerHTML')).encode('utf-8')
                    branches.append(
                        "{'address':'%s','city':'%s','zipcode':'%s','phone':'%s','fax':'%s'}"
                        % (colAddress, colCity, colZipcode, colPhone, colFax)
                    )
                BrokerData.branches = branches
            else:
                rows = tables.find_elements_by_tag_name('tr')
                rows.pop(0)
                for row in rows:
                    cols = row.find_elements_by_tag_name('td')
                    colAddress = (cols[1].get_attribute('innerHTML')).replace('/','-').replace(',', '').replace('\n', ' ').encode('utf-8')
                    colCity = (cols[2].get_attribute('innerHTML')).encode('utf-8')
                    colZipcode = (cols[3].get_attribute('innerHTML')).encode('utf-8')
                    colPhone = (cols[4].get_attribute('innerHTML')).encode('utf-8')
                    colFax = (cols[5].get_attribute('innerHTML')).encode('utf-8')
                    branches.append(
                        "{'address':'%s','city':'%s','zipcode':'%s','phone':'%s','fax':'%s'}"
                        % (colAddress, colCity, colZipcode, colPhone, colFax)
                    )
                BrokerData.branches = branches

        tab = tab + 1

    data = "{'profile': %s, 'summary': %s,'branch': %s}" % (
        BrokerData.profiles, BrokerData.summaries, BrokerData.branches)
    # print "=====> Data : %s", data

    code = firebase.getBrokerKeyByCode(code)
    BrokerData.brokers[code] = data


def filterDigit(data):
    if data == '&nbsp;':
        return 0

    if ",00" in data:
        data = data.replace(',00', '')

    return int(filter(unicode.isdigit, data))
