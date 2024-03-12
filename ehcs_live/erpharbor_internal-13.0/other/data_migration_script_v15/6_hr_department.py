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
    'name', 'parent_id', 'note',
]

def create_department(department_ids, parent_id):
    for department_id in department_ids:
        print("department id.............", department_id)
        department = sock.execute(dbname, uid, password, 'hr.department', 'read', department_id, FIELDS)[0]

        vals = {
            'hr_dept_sync_id': department['id'],
            'name': department['name'],
            'parent_id': parent_id,
            'note': department.get('note', ''),
        }

        domain = [('hr_dept_sync_id', '=', department['id'])]
        skip_department_id = l_object.execute(l_dbname, l_uid, l_password, 'hr.department', 'search', domain)

        if skip_department_id:
            print("Department is already created.........", skip_department_id, vals)
            l_object.execute(l_dbname, l_uid, l_password, 'hr.department', 'write', [skip_department_id[0]], vals)
            new_department_id = skip_department_id[0]
        else:
            print("Value of dept.......................", vals)
            new_department_id = l_object.execute(l_dbname, l_uid, l_password, 'hr.department', 'create', vals)
            print("Dept created>>>>>>>>>>>")
        child_department_ids = sock.execute(dbname, uid, password, 'hr.department', 'search', [('parent_id', '=', department['id'])])
        if child_department_ids:
            print("Child record found!!!!!!!!!!!!!......", child_department_ids, new_department_id)
            create_department(child_department_ids, new_department_id)


department_ids = sock.execute(dbname, uid, password, 'hr.department', 'search', [('parent_id', '=', False), ('id','!=',1)])
new_departments = create_department(department_ids, False)
