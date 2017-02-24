from alfresco import AlfrescoRestApi
import json
from django.db import connections
import datetime
import decimal

alfresco = AlfrescoRestApi('admin', 'root', 'http://docs.arungas.com:8080')
alfresco.login()


PROPERTY_MAP = {
	'sales': ['company', 'name', 'posting_date', 'customer', 'ship_to', 'grand_total_export'],
	'Indent': ['item', 'actual_amount', 'invoice_number', 'supplier', 'transaction_date', 'sales_tax', 'qty', 'customer', 'ship_to'],
	'Excise_Invoice': ['supplier', 'customer', 'invoice_number'],
	'Form_XII': ['supplier', 'customer', 'invoice_number']
}


def pushdoc(doctype, docname, ref_no, file_path):
	def map_erp_doctype(doctype):
		if doctype in ('Indent Invoice', 'Excise Invoice', 'VAT Form XII'):
			return 'Indent Invoice'
		if doctype == 'Consignment Note':
			return 'Sales Invoice'

	def get_conditions(erp_doctype, docname):
		cond = []
		if erp_doctype == 'Indent Invoice':
			cond.append('transportation_invoice = "{docname}"')
			cond.append('transportation_invoice like "{docname}-%"')
		if erp_doctype == 'Sales Invoice':
			cond.append('name = "{docname}"')
			cond.append('name like "{docname}-%"')
		return ' or '.join(cond).format(docname=docname, doctype=doctype)

	def map_alfresco(doctype):
		if doctype == 'Indent Invoice':
			return 'II', 'Indent'
		if doctype == 'Excise Invoice':
			return 'EI', 'Excise_Invoice'
		if doctype == 'Consignment Note':
			return 'SI', 'sales'
		if doctype == 'VAT Form XII':
			return 'VXII', 'Form_XII'

	def find_doc(doctype):
		return 'receiving_file' if doctype == 'Indent Invoice' or doctype == 'Consignment Note' else 'data_bank'

	def update_rec_file(doctype, cursor):
		if find_doc(doctype) == 'receiving_file':
			return alfresco.get_public_link(upload['nodeRef'])
		else:
			sql = """
            select data_bank
            from `tab{}` where ({})
            and docstatus = 1
            """.format(erp_doctype, get_conditions(erp_doctype, docname))
			cursor.execute(sql)
			results = cursor.fetchall()
			result = json.loads(results[0][0])
			result.setdefault('receivings', {})
			result['receivings'].update({doctype: alfresco.get_public_link(upload['nodeRef'])})
			return json.dumps(result)

	connection = connections['erp']

	try:

		with connection.cursor() as cursor:
			erp_doctype = map_erp_doctype(doctype)
			sql = """
            select *
            from `tab{}`
            where ({})
            and docstatus = 1
            """.format(erp_doctype, get_conditions(erp_doctype, ref_no))

			cursor.execute(sql)
			results = cursor.fetchall()
			columns = [x[0] for x in cursor.description]
			results = [{columns[index]: value for index, value in enumerate(result)} for result in results]
			for result in results:
				update = {}
				for key, value in result.iteritems():
					if isinstance(value, datetime.date):
						update[key] = value.strftime("%Y-%m-%d")
					if isinstance(value, decimal.Decimal):
						update[key] = str(value)
					if isinstance(value, datetime.timedelta) or isinstance(value, datetime.time):
						update[key] = ''
				result.update(update)

			result = results[0]

			if 'indent' in result:
				del result['indent']

			prefix, alfresco_model = map_alfresco(doctype)

			upload = alfresco.upload(
				file_path,
				'{}.jpg'.format(docname),
				{
					'contenttype': '{}:{}'.format(prefix, alfresco_model),
					'siteid': "receivings",
					'containerid': "documentLibrary"
				}
			)

			update_properties = alfresco.update_properties({
				"properties": {
					'{}:{}'.format(prefix, key): result[key]
					for key in PROPERTY_MAP[alfresco_model] if key in result and result[key]
					}
			},
				upload['nodeRef']
			)

			sql = """
            update
            `tab{}`
            set {} = '{}'
            where ({})
            and docstatus = 1
            """.format(
				map_erp_doctype(doctype),
				find_doc(doctype),
				update_rec_file(doctype, cursor),
				get_conditions(erp_doctype, ref_no)
			)

			cursor.execute(sql)

	except Exception as e:
		print e
		raise
