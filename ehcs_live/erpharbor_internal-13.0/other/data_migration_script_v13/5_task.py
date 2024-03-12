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
    'id', 'name', 'stage_id', 'project_id', 'user_id', 'date_deadline', 'description', 'parent_id',
    'planned_hours'
]

def create_tasks(task_ids):
    for task_id in task_ids:
        task = sock.execute(dbname, uid, password, 'project.task', 'read', task_id, FIELDS)[0]
        print "\n\nProject...........................", task

        parent_id = False
        if task['parent_id']:
            parent = l_object.execute(l_dbname, l_uid, l_password, 'project.task','search',[('project_task_sync_id', '=', task['parent_id'][0])])
            if parent:
                parent_id = parent[0]

        stage_id = False
        if task['stage_id']:
            stage = l_object.execute(l_dbname, l_uid, l_password, 'project.task.type','search',[('task_type_sync_id', '=', task['stage_id'][0])])
            if stage:
                stage_id = stage[0]

        user_id = False
        if task['user_id']:
            user = l_object.execute(l_dbname, l_uid, l_password, 'res.users','search',[('user_sync_id', '=', task['user_id'][0])])
            if user:
                user_id = user[0]

        project_id = False
        if task['project_id']:
            project = l_object.execute(l_dbname, l_uid, l_password, 'project.project','search',[('project_sync_id', '=', task['project_id'][0])])
            if project:
                project_id = project[0]

        vals = {
            'project_task_sync_id': task['id'],
            'name': task['name'],
            'project_id': project_id,
            'user_id': user_id,
            'date_deadline': task['date_deadline'],
            'description': task['description'],
            'stage_id': stage_id,
            'parent_id': parent_id,
            'planned_hours': task['planned_hours'],
        }
        domain = [('project_task_sync_id', '=', task['id'])]
        exist_task_ids = l_object.execute(l_dbname, l_uid, l_password, 'project.task', 'search', domain)
        if exist_task_ids:
            print "\n\nAlready exist *******************************"
            l_object.execute(l_dbname, l_uid, l_password, 'project.task', 'write', [exist_task_ids[0]], vals)
        else:
            print "\n\nVals-------------------", vals
            new_task_id = l_object.execute(l_dbname, l_uid, l_password, 'project.task', 'create', vals)
            print "Task Created++++++++++++++++++++++++++"

task_ids = sock.execute(dbname, uid, password, 'project.task', 'search', [])
print ("\n\nTask ids------    ", task_ids, len(task_ids))
new_tasks = create_tasks(task_ids)
