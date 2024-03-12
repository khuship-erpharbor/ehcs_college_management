try:
    from xmlrpc import client as xmlrpclib
except ImportError:
    import xmlrpclib

server = 'pms.erpharbor.in'
# port = '1111'
username = 'hitesh.j.erpharbor@gmail.com'
password = 'erpharbor@2022'
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

FIELDS = [
    'id', 'res_model', 'res_id', 'partner_id',
]

def create_folowers(follower_ids):
    for follower_id in follower_ids:
        print("\n\nFollow........................", follower_id)
        follower = sock.execute(dbname, uid, password, 'mail.followers', 'read', follower_id, FIELDS)[0]
        print("\n\nFollower data-------------------", follower)
        domain = [('follower_sync_id', '=', follower['id'])]
        exist_follower_id = l_object.execute(l_dbname, l_uid, l_password, 'mail.followers', 'search', domain)
        if exist_follower_id:
            print("\n\nAlready exist *******************************")
            continue
        else:
            res_id = False
            if follower['res_id']:
                record = l_object.execute(l_dbname, l_uid, l_password, 'project.project','search',[('project_sync_id', '=', follower['res_id'])])
                if record:
                    res_id = record[0]
                else:
                    continue

            partner_id = False
            if follower['partner_id']:
                partner = l_object.execute(l_dbname, l_uid, l_password, 'res.partner','search',[('partner_sync_id', '=', follower['partner_id'][0])])
                if partner:
                    print("\n\nPartner-----------------", partner)
                    partner_id = partner[0]
                else:
                    continue

            vals = {
                'follower_sync_id': follower['id'],
                'res_model': follower['res_model'],
                'res_id': res_id,
                'partner_id': partner_id,
            }
            print("\n\nVals-----------------", vals)
            if vals['partner_id']:
                new_follower_id = l_object.execute(l_dbname, l_uid, l_password, 'mail.followers', 'create', vals)
                print("Follower Created++++++++++++++++++++++++++")


follower_ids = sock.execute(dbname, uid, password, 'mail.followers', 'search', [('res_model', '=', 'project.project')])
print ("\n\nFollowers ids------    ", len(follower_ids))
new_followers = create_folowers(follower_ids)
