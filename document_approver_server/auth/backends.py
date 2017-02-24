import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class ErpUserBackend(ModelBackend):
	# Create a User object if not already in the database?

	def authenticate(self, username=None, password=None, **kwargs):
		# base_url = 'https://erp.arungas.com'

		login_request = requests.post('{}/api/method/login'.format(settings.ERP_URL), data={
			'usr': username,
			'pwd': password
		}, verify=False)

		if login_request.status_code != 200:
			return None

		UserModel = get_user_model()

		user, created = UserModel._default_manager.get_or_create(**{
			UserModel.USERNAME_FIELD: username
		})
		if created:
			user = self.populate(user, login_request.json())

		return user if self.user_can_authenticate(user) else None

	def populate(self, user, session_data):
		user_data = requests.get(
			'{}/api/resource/User/{}'.format(settings.ERP_URL, user.username),
			params={'sid': session_data['sid']}
		)
		user_data = user_data.json()['data']

		user.first_name = user_data.get('first_name', '')
		user.last_name = user_data.get('last_name', '')
		user.email = user_data.get('email', '')

		user.is_active = user_data.get('enabled', 0) == 1

		user.save()

		return user
