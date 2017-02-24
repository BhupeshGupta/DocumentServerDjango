from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny


class LoginView(KnoxLoginView):
	authentication_classes = ()
	permission_classes = (AllowAny,)

	def post(self, request, format=None):
		serializer = AuthTokenSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		request.user = serializer.validated_data['user']
		return super(LoginView, self).post(request, format)
