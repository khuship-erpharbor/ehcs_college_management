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
    'id', 'name', 'type', 'datas', 'res_model', 'res_id', 'res_name',
]

sync_id = {
    'project.project': 'project_sync_id',
    'project.task': 'project_task_sync_id',
    'res.partner': 'partner_sync_id',
    'hr.employee': 'hr_employee_sync_id',
    'res.users': 'user_sync_id',
}


def create_attachments(attachment_ids):
    for attachment_id in attachment_ids:
        attachment = sock.execute(dbname, uid, password, 'ir.attachment', 'read', attachment_id, FIELDS)[0]
        print("\n\nAttachment------------------", attachment)
        domain = [('attachment_sync_id', '=', attachment['id'])]
        exist_attach_id = l_object.execute(l_dbname, l_uid, l_password, 'ir.attachment', 'search', domain)
        if exist_attach_id:
            print "\n\nAlready exist *******************************"
            continue
        else:

            res_id = False
            if attachment['res_id']:
                record = l_object.execute(l_dbname, l_uid, l_password, attachment['res_model'],'search',[(sync_id[attachment['res_model']], '=', attachment['res_id'])])
                if record:
                    res_id = record[0]
                else:
                    continue

            vals = {
                'attachment_sync_id': attachment['id'],
                'name': attachment['name'],
                'type': attachment['type'],
                'res_id': res_id,
                'res_model': attachment['res_model'],
                'res_name': attachment['res_name'],
                'datas': attachment['datas'],
            }
            new_attach_id = l_object.execute(l_dbname, l_uid, l_password, 'ir.attachment', 'create', vals)


attachment_ids = sock.execute(dbname, uid, password, 'ir.attachment', 'search',
                              [('res_model', 'in', ['project.project', 'project.task', 'res.partner', 'res.users', 'hr.employee'])])
print ("\n\nFollowers ids------    ", len(attachment_ids))
new_attachment = create_attachments(attachment_ids)
