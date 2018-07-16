'''
requirement: sudo pip install schedule
usage: python idx_scheduler.py
'''
import schedule
import time
import firebase
import ast

import idx_scrap
from global_data import BrokerData

def firebase_update():
    for key, value in BrokerData.brokers.iteritems():
        result = ast.literal_eval(value)
        assert type(result) is dict
        firebase.updateBroker(key, result)

def job():
    idx_scrap.start()
    firebase_update()
    idx_scrap.stop()

schedule.every(30).minutes.do(job)
#schedule.every().day.at("13:66").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

