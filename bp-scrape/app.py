import firebase
import idx_scrap
import json
import re
import traceback
import ast
from global_data import BrokerData

try:
    idx_scrap.start()
    idx_scrap.stop()

    for key, value in BrokerData.brokers.iteritems():
        value = value.replace('u"', '').replace('"','')
        result = ast.literal_eval(value)
        assert type(result) is dict

        firebase.updateBroker(key, result)
except:
    print "Error: ", traceback.format_exc()
    idx_scrap.stop()

# print(firebase.getUsers())
# a = "1"
# b = "2"
# c = "3"

# data = {
#         'a': a,
#         'b': b,
#         'c': c
#     }

# data = '{"a": "%s", "b": "%s", "c": "%s"}' % (a, b, c)
# firebase.foo(data)

# data = {'Code': 'YP', 'Name': 'Test', 'License': 'Ijin'}

# firebase.addBroker(data)

# data = firebase.getBrokers()
# data = json.dumps(data)
# x = json.loads(data)
# for item in x:
#     print item['Code']

# data = {'profile': {'workPermit': u'PEE,PPE', 'managements': [u"{'name':'FERITA','position':'Komisaris Utama'}", u"{'name':'FRANS WIDJAJA','position':'Komisaris'}", u"{'name':'LEWI SASMITA KOSASIH','position':'Direktur Utama'}", u"{'name':'EDDY SUMARLI','position':'Direktur'}", u"{'name':'HERI INDARNO SULISTYANTO','position':'Direktur'}"], 'ownerships': [u"{'name':'PT NIRMALA TARUNA','ownership':'99,99'}", u"{'name':'JENARDI PURNAMA','ownership':'0,01'}"], 'basicCapital': u'Rp 100.000.000.000,00', 'companyStatus': u'Lokal', 'companyName': u'ALDIRACITA SEKURITAS INDONESIA', 'operationalStatus': u'Aktif', 'paidUpCapital': u'Rp 84.750.000.000,00', 'deed': u'No. 378 Tgl. 28 Juni 1990', 'lastMKBD': u'Rp101.261.746.743,00', 'npwp': u'01.357.581.6-054.000'}, 'summary': {'mkbds': [u"{'month':'January','year1':'111.128.476.551','year2':'104.064.354.732','year3':'74.633.716.621'}", u"{'month':'February','year1':'100.311.596.274','year2':'111.653.726.433','year3':'81.019.948.911'}", u"{'month':'March','year1':'&nbsp;','year2':'122.065.430.978','year3':'82.565.746.534'}", u"{'month':'April','year1':'&nbsp;','year2':'129.516.365.103','year3':'85.426.097.652'}", u"{'month':'May','year1':'&nbsp;','year2':'140.966.492.729','year3':'86.170.193.456'}", u"{'month':'June','year1':'&nbsp;','year2':'137.656.854.221','year3':'82.765.264.715'}", u"{'month':'July','year1':'&nbsp;','year2':'141.703.418.232','year3':'102.449.439.242'}", u"{'month':'August','year1':'&nbsp;','year2':'147.683.642.999','year3':'115.539.133.213'}", u"{'month':'September','year1':'&nbsp;','year2':'152.061.778.816','year3':'102.798.915.948'}", u"{'month':'October','year1':'&nbsp;','year2':'148.192.269.718','year3':'102.759.953.336'}", u"{'month':'November','year1':'&nbsp;','year2':'142.677.058.567','year3':'104.194.942.915'}", u"{'month':'December','year1':'0','year2':'124.812.436.962','year3':'101.829.136.440'}"], 'transactions': [u"{'month':'January','year1':'365.005.028.100','year2':'175.190.744.400','year3':'123.165.638.200'}", u"{'month':'February','year1':'&nbsp;','year2':'169.142.394.900','year3':'201.423.808.718'}", u"{'month':'March','year1':'&nbsp;','year2':'78.205.387.900','year3':'393.972.833.800'}", u"{'month':'April','year1':'&nbsp;','year2':'54.489.843.200','year3':'390.107.448.300'}", u"{'month':'May','year1':'&nbsp;','year2':'139.357.699.200','year3':'138.501.883.600'}", u"{'month':'June','year1':'&nbsp;','year2':'73.382.067.300','year3':'409.267.636.600'}", u"{'month':'July','year1':'&nbsp;','year2':'56.029.235.600','year3':'138.842.608.700'}", u"{'month':'August','year1':'&nbsp;','year2':'853.206.512.700','year3':'241.356.802.900'}", u"{'month':'September','year1':'&nbsp;','year2':'303.668.139.100','year3':'879.342.528.700'}", u"{'month':'October','year1':'&nbsp;','year2':'267.036.713.300','year3':'175.020.569.500'}", u"{'month':'November','year1':'&nbsp;','year2':'190.717.726.000','year3':'34.291.121.600'}", u"{'month':'December','year1':'0','year2':'472.798.239.010','year3':'102.265.496.700'}"]},'branch': {}}
# firebase.updateBroker(0, data)