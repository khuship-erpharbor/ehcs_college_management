try:
    from xmlrpc import client as xmlrpclib
except ImportError:
    import xmlrpclib

server = 'pms.erpharbor.in'
# port = '1111'
username = 'abhishek@erpharbor.com'
password = 'abhi@123'
dbname = 'pms'

url = 'https://' + server
common = xmlrpclib.ServerProxy(url + '/xmlrpc/common')
uid = common.login(dbname, username, password)
sock = xmlrpclib.ServerProxy(url + '/xmlrpc/object')

################################################################################

l_server='localhost'
l_port= '1111'
l_username='admin'
l_password='admin'
l_dbname='erpharbor_v15_c_whdb_19-04-22'

l_url = 'http://' + l_server + ':' + l_port
l_common = xmlrpclib.ServerProxy(l_url + '/xmlrpc/common')
l_uid = l_common.login(l_dbname, l_username, l_password)
l_object = xmlrpclib.ServerProxy(l_url + '/xmlrpc/object')

################################################################################

v13_FIELDS = [
    'name', 'login', 'partner_id', 'password', 'email',
]

FIELDS = [
    'name', 'login', 'partner_id', 'password', 'email',
]

def create_users(user_ids):

    for user_id in user_ids:
        user = sock.execute(dbname, uid, password, 'res.users', 'read', user_id, v13_FIELDS)[0]
        print("\n\nUsers-------------", user)
        domain = [('name', '=', user['name']), ('user_sync_id', '=', False)]
        same_users = l_object.execute(l_dbname, l_uid, l_password, 'res.users', 'search', domain)
        value = {'user_sync_id': user['id']}
        if same_users:
            print("Same User ids................................", same_users)
            for same_user in same_users:
                l_object.execute(l_dbname, l_uid, l_password, 'res.users', 'write', [same_user], value)

    for user_id in user_ids:
        print("User id..................", user_id)
        user = sock.execute(dbname, uid, password, 'res.users', 'read', user_id, v13_FIELDS)[0]
        print("\n\nUser-------------------", user)
        domain = [('user_sync_id', '=', user['id'])]
        exist_user_ids = l_object.execute(l_dbname, l_uid, l_password, 'res.users', 'search', domain)
        if exist_user_ids:
            continue
        else:
            vals = {
                'user_sync_id': user['id'],
                'name': user['name'],
                'login': user['login'],
                'password': user['password'],
            }
            print("vals.........................", vals)
            new_user_id = l_object.execute(l_dbname, l_uid, l_password, 'res.users', 'create', vals)
            print("New user created...............")
            new_user = l_object.execute(l_dbname, l_uid, l_password, 'res.users', 'read', new_user_id, FIELDS)
            related_partner_id = new_user[0].get('partner_id')[0]
            value = {
                'partner_sync_id': user['partner_id'][0],
                'is_created_with_user': True,
                'email': user['email'],
            }
            l_object.execute(l_dbname, l_uid, l_password, 'res.partner', 'write', [related_partner_id], value)
            print("Partner updated>>>>>>>>>>")


user_ids = sock.execute(dbname, uid, password, 'res.users', 'search', [('login', '!=', 'admin')])
print("Total user............", len(user_ids))
new_users = create_users(user_ids)
