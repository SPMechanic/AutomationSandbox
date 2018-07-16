import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import db
import json

firebase_url = 'https://broker-pages-f0804.firebaseio.com'

cred = credentials.Certificate('broker-pages-16aa4b322a1b.json')
firebase_admin.initialize_app(cred, {'databaseURL': firebase_url})


def getUsers():
    return db.reference('users').get()


def getBrokers():
    brokers = db.reference('brokers')
    return brokers.order_by_child('Name').limit_to_first(15).get()
    # return brokers.order_by_child('Name').get()



def getBrokerKeyByCode(code):
    ref = db.reference('brokers')
    broker = ref.order_by_child('Code').equal_to(code).get()
    dumps = json.dumps(broker)
    result = json.loads(dumps)
    return result.keys()[0]


def addBroker(data):
    ref = db.reference('brokers').push()
    ref.set(data)
    return ref.key


def updateBroker(code, data):
    print "Update to firebase brokers with code : ", code
    code = "brokers/%s" % code
    ref = db.reference(code)
    ref.update(data)


# foreach data from json
# def foo(theList):
#     theList = json.dumps(theList)
#     print theList
#     a = json.loads(theList)
#     print a
#     for n, v in a.iteritems():
#         print n, v

# user = auth.get_user_by_email('yopi.cahya@gmail.com')
# print 'Successfully fetched user data: {0}'.format(user.uid)

# Update data
# root = db.reference()
# # Add a new user under /users.
# new_user = root.child('users').push({
#     'name' : 'Mary Anning',
#     'since' : 1700
# })

# # Update a child attribute of the new user.
# new_user.update({'since' : 1799})

# # Obtain a new reference to the user, and retrieve child data.
# # Result will be made available as a Python dict.
# mary = db.reference('users/{0}'.format(new_user.key)).get()
# print 'Name:', mary['name']
# print 'Since:', mary['since']