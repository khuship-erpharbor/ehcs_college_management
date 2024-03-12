import xmlrpclib

server = 'pms.erpharbor.com'
#port = '8010'
username = 'admin'
password = 'erpharbor2018'
dbname = 'pms'

url = 'http://' + server
common = xmlrpclib.ServerProxy(url + '/xmlrpc/common')
uid = common.login(dbname, username, password)
sock = xmlrpclib.ServerProxy(url + '/xmlrpc/object')

################################################################################

l_server='localhost'
l_port= '8069'
l_username='admin'
l_password='a'
l_dbname='website_erpharbor_test'

l_url = 'http://' + l_server + ':' + l_port
l_common = xmlrpclib.ServerProxy(l_url + '/xmlrpc/common')
l_uid = l_common.login(l_dbname, l_username, l_password)
l_object = xmlrpclib.ServerProxy(l_url + '/xmlrpc/object')

################################################################################

v10_FIELDS = [
    'name', 'login', 'partner_id', 'password_crypt', 'email',
]

FIELDS = [
    'name', 'login', 'partner_id', 'password', 'email',
]

def create_users(user_ids):

    for user_id in user_ids:
        user = sock.execute(dbname, uid, password, 'res.users', 'read', user_id, v10_FIELDS)[0]
        print "\n\nUsers-------------", user
        domain = [('name', '=', user['name']), ('user_sync_id', '=', False)]
        same_users = l_object.execute(l_dbname, l_uid, l_password, 'res.users', 'search', domain)
        value = {'user_sync_id': user['id']}
        if same_users:
            print("Same User ids................................", same_users)
            for same_user in same_users:
                l_object.execute(l_dbname, l_uid, l_password, 'res.users', 'write', [same_user], value)

    for user_id in user_ids:
        print("User id..................", user_id)
        user = sock.execute(dbname, uid, password, 'res.users', 'read', user_id, v10_FIELDS)[0]
        print "\n\nUser-------------------", user
        domain = [('user_sync_id', '=', user['id'])]
        exist_user_ids = l_object.execute(l_dbname, l_uid, l_password, 'res.users', 'search', domain)
        if exist_user_ids:
            continue
        else:
            vals = {
                'user_sync_id': user['id'],
                'name': user['name'],
                'login': user['login'],
                'password': user['password_crypt'],
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
