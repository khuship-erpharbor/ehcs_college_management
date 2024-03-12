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
    'id', 'name', 'fold', 'project_ids',
]

FIELDS_PROJECT = ['id', 'project_sync_id']

def create_task_type(task_type_ids):
    for task_type_id in task_type_ids:
        task_type = sock.execute(dbname, uid, password, 'project.task.type', 'read', task_type_id, FIELDS)[0]
        print("\n\nTask type----------------------", task_type)
        domain = [('task_type_sync_id', '=', task_type['id'])]
        task_type_ids = l_object.execute(l_dbname, l_uid, l_password, 'project.task.type', 'search', domain)
        if task_type_ids:
            continue
        else:

            new_project_ids = []
            if task_type['project_ids']:
                print("\n\nProjects----------------------", task_type['project_ids'])
                new_project_ids = get_projects(task_type['project_ids'])
                print("\n\nProject list--------------------", new_project_ids)

            vals = {
                'task_type_sync_id': task_type['id'],
                'name': task_type['name'],
                'fold': task_type['fold'],
                'project_ids': [(6, 0, new_project_ids)],
            }
            new_task_type_id = l_object.execute(l_dbname, l_uid, l_password, 'project.task.type', 'create', vals)
            print("Task Type Created++++++++++++++++++++++++++")

def get_projects(project_ids):
    project_list = []
    for project_id in project_ids:
        project = sock.execute(dbname, uid, password, 'project.project', 'read', project_id, FIELDS_PROJECT)[0]
        domain = [('project_sync_id', '=', project['id'])]
        new_project = l_object.execute(l_dbname, l_uid, l_password, 'project.project', 'search', domain)
        if new_project:
            project_list.append(new_project[0])
    return project_list


task_type_ids = sock.execute(dbname, uid, password, 'project.task.type', 'search', [])
print ("\n\nTask ids------    ", task_type_ids, len(task_type_ids))
new_tasks = create_task_type(task_type_ids)
