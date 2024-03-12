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
    'id', 'name', 'date', 'user_id', 'project_id', 'task_id', 'unit_amount', 'is_invoiced',
]


def create_analytic_line(analytic_line_ids):
    for analytic_line_id in analytic_line_ids:
        print("\n\nLines...................", analytic_line_id)
        analytic_line = sock.execute(dbname, uid, password, 'account.analytic.line', 'read', analytic_line_id, FIELDS)[0]
        print("\n\nAnalytic-----------", analytic_line)
        domain = [('analytic_line_sync_id', '=', analytic_line['id'])]
        skip_line_id = l_object.execute(l_dbname, l_uid, l_password, 'account.analytic.line', 'search', domain)
        if skip_line_id:
            print("Line already exist!!!!!!!!!!!!!!")
            continue
        else:

            user_id = False
            if analytic_line['user_id']:
                user = l_object.execute(l_dbname, l_uid, l_password, 'res.users','search',[('user_sync_id', '=', analytic_line['user_id'][0])])
                if user:
                    user_id = user[0]
                else:
                    continue

            employee_id = False
            if user_id:
                employee = l_object.execute(l_dbname, l_uid, l_password, 'hr.employee','search',[('user_id', '=', user_id)])
                if employee:
                    employee_id = employee[0]
                else:
                    continue

            project_id = False
            if analytic_line['project_id']:
                project = l_object.execute(l_dbname, l_uid, l_password, 'project.project','search',[('project_sync_id', '=', analytic_line['project_id'][0])])
                if project:
                    project_id = project[0]
                else:
                    continue

            task_id = False
            if analytic_line['task_id']:
                task = l_object.execute(l_dbname, l_uid, l_password, 'project.task','search',[('project_task_sync_id', '=', analytic_line['task_id'][0])])
                if task:
                    task_id = task[0]
                else:
                    continue

            vals = {
                'analytic_line_sync_id': analytic_line['id'],
                'name': analytic_line['name'],
                'date': analytic_line['date'],
                'user_id': user_id,
                'employee_id': employee_id,
                'project_id': project_id,
                'task_id': task_id,
                'unit_amount': analytic_line['unit_amount'],
                'is_invoiced': analytic_line['is_invoiced'],
            }
            print("\n\nFinal vals---------------------", vals)
            new_analytic_id = l_object.execute(l_dbname, l_uid, l_password, 'account.analytic.line', 'create', vals)
            print("Analytic created.........................")


user_ids = l_object.execute(l_dbname, l_uid, l_password, 'res.users', 'search', [])
user_sync_ids = []
user_syncs = l_object.execute(l_dbname, l_uid, l_password, 'res.users', 'search_read', [('id', 'in', user_ids)], ['user_sync_id'])
for user_sync in user_syncs:
    if user_sync.get('user_sync_id'):
        user_sync_ids.append(user_sync.get('user_sync_id'))



analytic_line_ids = sock.execute(dbname, uid, password, 'account.analytic.line', 'search', [('user_id', 'in', user_sync_ids)])
print("Lines.........................", len(analytic_line_ids))
new_departments = create_analytic_line(analytic_line_ids)
