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
    'name', 'address_id', 'work_email', 'work_phone', 'mobile_phone', 'work_location', 'user_id',
    'department_id', 'job_id', 'parent_id', 'notes', 'work_phone', 'coach_id',
    'country_id', 'identification_id', 'passport_id', 'address_home_id',
    'gender', 'marital', 'children', 'birthday', 'joining_date', 'skype', 'parent_id',
]


def create_employee(employee_ids):
#    for employee_id in employee_ids:
#        employee = sock.execute(dbname, uid, password, 'hr.employee', 'read', employee_id, FIELDS)[0]
#        print "\n\nEmployee-------------------", employee
#        domain = [('name', '=', employee['name']), ('hr_employee_sync_id', '=', False)]
#        same_employees = l_object.execute(l_dbname, l_uid, l_password, 'hr.employee', 'search', domain)
#        print "\n\nSame employee---------------------", same_employees
#        value = {'hr_employee_sync_id': employee['id']}
#        if same_employees:
#            print("Same Emloyee ids................................", same_employees)
#            for same_employee in same_employees:
#                l_object.execute(l_dbname, l_uid, l_password, 'hr.employee', 'write', [same_employee], value)

    for employee_id in employee_ids:
        employee = sock.execute(dbname, uid, password, 'hr.employee', 'read', employee_id, FIELDS)[0]
        domain = [('hr_employee_sync_id', '=', employee['id'])]
        skip_employee_id = l_object.execute(l_dbname, l_uid, l_password, 'hr.employee', 'search', domain)
        address_id = False
        if employee['address_id']:
            add_id = l_object.execute(l_dbname, l_uid, l_password, 'res.partner','search',[('partner_sync_id', '=', employee['address_id'][0])])
            if add_id:
                address_id = add_id[0]

        address_home_id = False
        if employee['address_home_id']:
            add_home_id = l_object.execute(l_dbname, l_uid, l_password, 'res.partner','search',[('partner_sync_id', '=', employee['address_home_id'][0])])
            if add_home_id:
                address_home_id = add_home_id[0]

        department_id = False
        if employee['department_id']:
            dept_id = l_object.execute(l_dbname, l_uid, l_password, 'hr.department','search',[('hr_dept_sync_id', '=', employee['department_id'][0])])
            if dept_id:
                department_id = dept_id[0]

        country_id = False
        if employee['country_id']:
            country = l_object.execute(l_dbname, l_uid, l_password, 'res.country', 'search_read', [('name', '=', employee['country_id'][1])], ['id', 'name'])
            if country:
                country_id = country[0].get('id')

        user_id = False
        if employee['user_id']:
            user = l_object.execute(l_dbname, l_uid, l_password, 'res.users','search',[('user_sync_id', '=', employee['user_id'][0])])
            if user:
                user_id = user[0]

        print "\n\nAddress id------------------", address_id
        parent_id = False
        if employee['parent_id']:
            parent_id = l_object.execute(l_dbname, l_uid, l_password, 'hr.employee', 'search', [('hr_employee_sync_id', '=', employee['parent_id'][0])])[0]

        coach_id = False
        if employee['coach_id']:
            coach_id = l_object.execute(l_dbname, l_uid, l_password, 'hr.employee', 'search', [('hr_employee_sync_id', '=', employee['coach_id'][0])])[0]

        vals = {
            'hr_employee_sync_id': employee['id'],
            'name': employee['name'],
            'address_id': address_id,
            'work_email': employee['work_email'],
            'work_phone': employee['work_phone'],
            'mobile_phone': employee['mobile_phone'],
            'work_location': employee['work_location'],
            'user_id': user_id,
            'department_id': department_id,
            'notes': employee['notes'],
            'country_id': country_id,
            'identification_id': employee['identification_id'],
            'passport_id': employee['passport_id'],
            'address_home_id': address_home_id,
            'gender': employee['gender'],
            'marital': employee['marital'],
            'birthday': employee['birthday'],
            'joining_date': employee['joining_date'],
            'skype': employee['skype'],
            'work_phone': employee['work_phone'],
            'parent_id': parent_id,
            'coach_id': coach_id,
        }
        if skip_employee_id:
            print("Employee already exist!!!!!!!!!!!!!!", skip_employee_id)
            l_object.execute(l_dbname, l_uid, l_password, 'hr.employee', 'write', skip_employee_id, vals)
        else:
            l_object.execute(l_dbname, l_uid, l_password, 'hr.employee', 'create', vals)
            print("Employee created.........................")


employee_ids = sock.execute(dbname, uid, password, 'hr.employee', 'search', [('active', '=', True)])
print("Employee.........................", employee_ids, len(employee_ids))
new_departments = create_employee(employee_ids)
