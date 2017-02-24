from rest_framework import routers
from .viewsets import DocumentViewSet, VerificationViewSet, FileViewSet
from django.conf.urls import url, include

router = routers.DefaultRouter()
router.register(r'document', DocumentViewSet)
router.register(r'file', FileViewSet)
router.register(r'verification', VerificationViewSet)

urlpatterns = [
	url(r'^', include(router.urls, namespace='arungas-document-receivings')),
]