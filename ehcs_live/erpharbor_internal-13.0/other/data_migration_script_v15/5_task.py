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
    'id', 'name', 'stage_id', 'project_id', 'user_id', 'date_deadline', 'description', 'parent_id',
    'planned_hours'
]

def create_tasks(task_ids):
    for task_id in task_ids:
        task = sock.execute(dbname, uid, password, 'project.task', 'read', task_id, FIELDS)[0]
        print("\n\n Task...........................", task)

        parent_id = False
        if task['parent_id']:
            parent = l_object.execute(l_dbname, l_uid, l_password, 'project.task','search',[('project_task_sync_id', '=', task['parent_id'][0])])
            if parent:
                parent_id = parent[0]

        user_id = []
        if task['user_id']:
            user = l_object.execute(l_dbname, l_uid, l_password, 'res.users','search',[('user_sync_id', '=', task['user_id'][0])])
            if user:
                user_id = user

        stage_id = False
        if task['stage_id']:
            stage = l_object.execute(l_dbname, l_uid, l_password, 'project.task.type','search',[('task_type_sync_id', '=', task['stage_id'][0])])
            if stage:
                stage_id = stage[0]

        project_id = False
        if task['project_id']:
            project = l_object.execute(l_dbname, l_uid, l_password, 'project.project','search',[('project_sync_id', '=', task['project_id'][0])])
            if project:
                project_id = project[0]

        vals = {
            'project_task_sync_id': task['id'],
            'name': task['name'],
            'project_id': project_id,
            'date_deadline': task['date_deadline'],
            'description': task['description'],
            'stage_id': stage_id,
            'parent_id': parent_id,
            'planned_hours': task['planned_hours'],
            'user_ids': user_id,
        }
        print('\n\n Task Values',vals)
        domain = [('project_task_sync_id', '=', task['id'])]
        exist_task_ids = l_object.execute(l_dbname, l_uid, l_password, 'project.task', 'search', domain)
        if exist_task_ids:
            print("\n\nAlready exist *******************************")
            l_object.execute(l_dbname, l_uid, l_password, 'project.task', 'write', [exist_task_ids[0]], vals)
        else:
            print("\n\nVals-------------------", vals)
            new_task_id = l_object.execute(l_dbname, l_uid, l_password, 'project.task', 'create', vals)
            print("Task Created++++++++++++++++++++++++++")

task_ids = sock.execute(dbname, uid, password, 'project.task', 'search', [])
print ("\n\nTask ids------    ", task_ids, len(task_ids))
new_tasks = create_tasks(task_ids)
