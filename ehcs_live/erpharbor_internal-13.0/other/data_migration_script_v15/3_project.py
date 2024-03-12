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
    'id', 'name', 'privacy_visibility',
]

def create_projects(project_ids):
    for project_id in project_ids:
        project = sock.execute(dbname, uid, password, 'project.project', 'read', project_id, FIELDS)
        print("\n\nProject...........................", project)
        
        vals = {
            'project_sync_id': project[0]['id'],
            'name': project[0]['name'],
            'privacy_visibility': project[0]['privacy_visibility'],
        }
        print("\n\nValues-----------------------", vals)
        domain = [('project_sync_id', '=', project[0]['id'])]
        exist_project_id = l_object.execute(l_dbname, l_uid, l_password, 'project.project', 'search', domain)
        if exist_project_id:
            print("\n\nProject exist !!!!!!!!!!!!!!!!!!!!!!!!!!")
            l_object.execute(l_dbname, l_uid, l_password, 'project.project', 'write', [exist_project_id[0]], vals)
        else:
            print("Vals-------------------", vals)
            new_project_id = l_object.execute(l_dbname, l_uid, l_password, 'project.project', 'create', vals)
            print("New project--------------------", new_project_id)


project_ids = sock.execute(dbname, uid, password, 'project.project', 'search', [])
print ("\n\nPPPPPPPPPPPPPppppp    ", project_ids, len(project_ids))
new_projects = create_projects(project_ids)
