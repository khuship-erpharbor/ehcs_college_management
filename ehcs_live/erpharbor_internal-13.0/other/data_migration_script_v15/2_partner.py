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

FIELDS = [
    'name', 'is_company', 'parent_id', 'street', 'street2', 'city', 'zip', 'state_id', 'country_id',
    'website', 'function', 'phone', 'mobile', 'email', 'comment',
]

def create_partner(partner_ids):
    for partner_id in partner_ids:
        print("\n\nPartner++++++++++++++++++", partner_id)
        partner = sock.execute(dbname, uid, password, 'res.partner', 'read', partner_id, FIELDS)[0]
        print("\n\nPartner details.................", partner)

        country_id = False
        if partner['country_id']:
            country = l_object.execute(l_dbname, l_uid, l_password, 'res.country', 'search_read', [('name', '=', partner['country_id'][1])], ['id', 'name'])
            if country:
                country_id = country[0].get('id')

        state_id = False
        if partner['state_id']:
            state = l_object.execute(l_dbname, l_uid, l_password, 'res.country.state', 'search_read', [('name', '=', partner['state_id'][1])], ['id', 'name'])
            if state:
                state_id = state[0].get('id')
                
        vals = {
            'partner_sync_id': partner['id'],
            'name': partner['name'],
            'is_company': partner['is_company'],
            'street': partner['street'],
            'street2': partner['street2'],
            'city': partner['city'],
            'zip': partner['zip'],
            'state_id': state_id,
            'country_id': country_id,
            'website': partner['website'],
            'function': partner['function'],
            'phone': partner['phone'],
            'mobile': partner['mobile'],
            'comment': partner['comment'],
        }
        if partner['email']:
            vals.update({'email': partner['email']})
        print("\n\nFinal vals-------------------", vals)

        domain_two = [('partner_sync_id', '=', partner['id'])]
        exist_partner_id = l_object.execute(l_dbname, l_uid, l_password, 'res.partner', 'search', domain_two)

        if exist_partner_id:
            print("Updating existing data.........................")
            l_object.execute(l_dbname, l_uid, l_password, 'res.partner', 'write', [exist_partner_id[0]], vals)
        else:
            print("Creating new partner.................", vals)
            new_partner_id = l_object.execute(l_dbname, l_uid, l_password, 'res.partner', 'create', vals)
            print("\n\nPartner created####################")


partner_ids= l_object.execute(l_dbname, l_uid, l_password, 'res.partner', 'search', [])
print ("\n\nPartner ids==============", partner_ids)

part_sync_ids = []
parts_syncs = l_object.execute(l_dbname, l_uid, l_password, 'res.partner', 'search_read', [('id', 'in', partner_ids)], ['partner_sync_id'])
print("\n\nPart sync----------------------", parts_syncs)
for part_sync in parts_syncs:
    if part_sync.get('partner_sync_id'):
        part_sync_ids.append(part_sync.get('partner_sync_id'))

print("\n\nList--------------------", part_sync_ids)
partner_ids = sock.execute(dbname, uid, password, 'res.partner', 'search', [('parent_id', '=', False), ('id', 'not in', part_sync_ids)])
new_partners = create_partner(partner_ids)
