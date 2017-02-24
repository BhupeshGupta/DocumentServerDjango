import json

import requests


def get_document_details(doctype, docname):
	url = 'http://127.0.0.1:8080'

	docdata = requests.post(url, data={
		"cmd": "flows.flows.controller.ephesoft_integration.get_meta",
		"doc": json.dumps({
			"id": docname,
			"type": doctype
		})
	})

	if docdata.status_code != 200:
		return {}

	docdata = json.loads(docdata.json()['message'])

	if docdata['$bill_amended_from']:
		docdata['Bill Number'] = docdata['Bill Number'].rsplit('-', 1)[0]
	if docdata['$consignment_amended_from']:
		docdata['Consignment Name'] = docdata['Consignment Name'].rsplit('-', 1)[0]

	docdata.pop('$consignment_amended_from')
	docdata.pop('$bill_amended_from')

	return docdata
