import json
import os

from django.conf import settings
from django.db.models import Q
from django.http import Http404
from django.utils import timezone
from django.views.static import serve
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .erp_api import get_document_details
from .models import Document, Verification, File
from .serializers import (
	DocumentSerializer, DocumentRelatedSerializer, VerificationSerializer,
	VerificationCreationSerializer, FileSerializer
)


class CanVerifyDocumentPermission(permissions.BasePermission):
	def has_permission(self, request, view):
		has_perm = request.user.has_perm('document_receivings.can_verify_document')
		return has_perm


class DocumentViewSet(viewsets.ModelViewSet):
	queryset = Document.objects.all()
	serializer_class = DocumentSerializer
	http_method_names = ['get', 'post']
	filter_backends = (DjangoFilterBackend,)
	filter_fields = ('status',)
	ordering = ('-created_on',)

	@detail_route(methods=['get'], url_path='details')
	def get_document_details(self, request, pk=None):
		document_object = self.get_object()
		return Response(get_document_details(document_object.doctype, document_object.docname))

	@list_route(methods=['get'], url_path='search')
	def search(self, request):
		qs = self.get_queryset().filter(doctype='Indent Invoice')
		query = request.GET.get('q', '')

		try:
			query = json.loads(query)
		except:
			pass

		if isinstance(query, dict):
			result_qs = qs.filter(**query)
		else:
			result_qs = qs.filter(Q(docname__iendswith=query) | Q(ref_no__iendswith=query))

		page = self.paginate_queryset(result_qs)
		if page is not None:
			serializer = DocumentRelatedSerializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = DocumentRelatedSerializer(result_qs, many=True)
		return Response(serializer.data)


class VerificationViewSet(viewsets.ModelViewSet):
	queryset = Verification.objects.prefetch_related('document').prefetch_related('files').prefetch_related(
		'created_by').all()
	http_method_names = ['get', 'post']
	filter_backends = (DjangoFilterBackend,)
	filter_fields = ('status',)
	ordering = ('-created_on',)

	def get_serializer_class(self):
		if self.request.method == 'POST':
			return VerificationCreationSerializer
		else:
			return VerificationSerializer

	@detail_route(methods=['post'], url_path='approve', permission_classes=[CanVerifyDocumentPermission])
	def approve_verification(self, request, pk=None):
		# Update status of Verification Request
		verification_object = self.get_object()

		# Approve is an expensive task with all Remote api calls, skip it if already approved
		if verification_object.status == 1:
			return Response(status=status.HTTP_200_OK)

		verification_object.status = 1
		verification_object.verified_by = request.user
		verification_object.verified_on = timezone.now()
		verification_object.save()

		document = verification_object.document
		all_files = verification_object.files.all()
		# Link files with document and update status of document
		document.status = 1
		document.verified_by = request.user
		document.verified_on = timezone.now()
		document.files = all_files
		document.save()

		# Upload file to alfresco and update its link in ERP.
		full_path = os.path.join(settings.MEDIA_ROOT, all_files[0].file.url)

		from .alfresco_upload import pushdoc
		pushdoc(document.doctype, document.docname, document.ref_no, full_path)

		return Response(status=status.HTTP_200_OK)

	@detail_route(methods=['post'], url_path='reject', permission_classes=[CanVerifyDocumentPermission])
	def reject_verification(self, request, pk=None):
		verification_object = self.get_object()
		verification_object.status = 2
		verification_object.verified_by = request.user
		verification_object.verified_on = timezone.now()
		verification_object.save()

		verification_object.document.status = 2
		verification_object.document.verified_by = request.user
		verification_object.document.verified_on = timezone.now()
		verification_object.document.save()

		return Response(status=status.HTTP_200_OK)


class FileViewSet(viewsets.ModelViewSet):
	parser_classes = (MultiPartParser,)

	queryset = File.objects.all()
	serializer_class = FileSerializer
	http_method_names = ['post', 'get']

	def perform_create(self, obj):
		file_object = obj.validated_data['file']
		obj.validated_data['size'] = file_object.size
		obj.validated_data['filename'] = os.path.splitext(file_object.name)[0]
		obj.validated_data['type'] = file_object.content_type
		return super(FileViewSet, self).perform_create(obj)

	@detail_route(methods=['get'], url_path='download', permission_classes=[AllowAny])
	def download_file(self, request, pk=None):
		try:
			file_object = self.get_object()
			return serve(request, file_object.file.url, document_root=settings.MEDIA_ROOT)
		except Http404 as e:
			content = {'error': ['File Not Found.']}
			return Response(content, status=status.HTTP_404_NOT_FOUND)
		except Exception as e:
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
