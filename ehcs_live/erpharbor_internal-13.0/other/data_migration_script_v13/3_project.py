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

FIELDS = [
    'id', 'name', 'privacy_visibility',
]

def create_projects(project_ids):
    for project_id in project_ids:
        project = sock.execute(dbname, uid, password, 'project.project', 'read', project_id, FIELDS)
        print "\n\nProject...........................", project
        
        vals = {
            'project_sync_id': project[0]['id'],
            'name': project[0]['name'],
            'privacy_visibility': project[0]['privacy_visibility'],
        }
        print "\n\nValues-----------------------", vals
        domain = [('project_sync_id', '=', project[0]['id'])]
        exist_project_id = l_object.execute(l_dbname, l_uid, l_password, 'project.project', 'search', domain)
        if exist_project_id:
            print "\n\nProject exist !!!!!!!!!!!!!!!!!!!!!!!!!!"
            l_object.execute(l_dbname, l_uid, l_password, 'project.project', 'write', [exist_project_id[0]], vals)
        else:
            print "Vals-------------------", vals
            new_project_id = l_object.execute(l_dbname, l_uid, l_password, 'project.project', 'create', vals)
            print "New project--------------------", new_project_id


project_ids = sock.execute(dbname, uid, password, 'project.project', 'search', [])
print ("\n\nPPPPPPPPPPPPPppppp    ", project_ids, len(project_ids))
new_projects = create_projects(project_ids)
