import requests
from lxml import etree


class AlfrescoRestApi(object):
    def __init__(self, user, password, url):
        self.user = user
        self.password = password
        self.url = url
        self.ticket = None

    def login(self):
        req = requests.get('{}/alfresco/service/api/login?u={}&pw={}'.format(
            self.url, self.user, self.password
        ))
        # TODO Check error code and raise exceptions
        xmldoc = etree.XML(req.content)
        if xmldoc.tag == 'ticket':
            self.ticket = xmldoc.text

        if not self.ticket:
            raise Exception('Unable to login')

    def upload(self, file_path, file_name, alfersco_properties):
        req = requests.post(
            '{}/alfresco/service/api/upload'.format(self.url),
            auth=(self.user, self.password),
            files=[
                ('filedata', (file_name, open(file_path, 'rb')))
            ],
            data=alfersco_properties
        )

        if req.status_code != 200:

            raise Exception('Alfresco upload returned {}'.format(req.status_code))

        req = req.json()
        return req

    def update_properties(self, data, node_ref):
        url = '{}/alfresco/service/api/metadata/node/{}'.format(
            self.url,
            '/'.join(AlfrescoRestApi.parse_node_ref(node_ref))
        )

        req = requests.post(
            url,
            auth=(self.user, self.password),
            json=data
        )
        if req.status_code != 200:

            raise Exception('Alfresco property update returned {}'.format(req.status_code))
        return req.json()

    def get_public_link(self, node_ref):
        public_file_url = "{}/share/proxy/alfresco/api/node/{}/{}/{}/content/thumbnails/imgpreview"
        return public_file_url.format(self.url, *AlfrescoRestApi.parse_node_ref(node_ref))

    @staticmethod
    def parse_node_ref(node_ref):
        storage_type, _ = node_ref.split('://')
        storage_id, file_id = _.split('/')
        return storage_type, storage_id, file_id

