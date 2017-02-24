from knox.settings import knox_settings
from rest_framework import serializers

from .models import Document, Verification, File
from .relations import FilesKeyRelatedField

UserSerializer = knox_settings.USER_SERIALIZER


class DocumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Document
		fields = '__all__'
		read_only_fields = ('status', 'created_by', 'verified_by', 'created_on', 'verified_on', 'related_docs')

	def create(self, validated_data):
		validated_data['created_by'] = self.context['request'].user
		return super(DocumentSerializer, self).create(validated_data)


class DocumentRelatedSerializer(DocumentSerializer):
	related_docs = serializers.SerializerMethodField()

	def get_related_docs(self, doc):
		return DocumentSerializer(doc.related_docs, many=True).data


class FileSerializer(serializers.ModelSerializer):
	class Meta:
		model = File
		fields = ('id', 'file', 'size', 'type', 'filename', 'verification', 'document')
		read_only_fields = ('id', 'size', 'type', 'filename', 'verification', 'document')


class VerificationSerializer(serializers.ModelSerializer):
	document = DocumentSerializer(many=False)
	files = FilesKeyRelatedField(
		many=True,
		view_name='arungas-document-receivings:file-download',
		queryset=File.objects.all()
	)
	created_by = UserSerializer(many=False)

	depth = 3

	class Meta:
		model = Verification
		fields = '__all__'
		read_only_fields = ('status', 'created_by', 'verified_by', 'created_on', 'verified_on')


class VerificationCreationSerializer(VerificationSerializer):
	document = serializers.PrimaryKeyRelatedField(
		queryset=Document.objects.all()
	)

	created_by = serializers.PrimaryKeyRelatedField(read_only=True)

	def validate_document(self, document):
		"""
		Verifies that document is in Rejected or Pending state before creating verification
		"""
		if document.status == 1:
			raise serializers.ValidationError("Document is already verified and approved")
		elif document.status == 3:
			raise serializers.ValidationError(
				"Document is pending for review. Another verification request already pending.")
		return document

	def create(self, validated_data):
		"""
		Upadate document status ro 3 indicating that a verification is pending against the said document
		"""
		document = validated_data['document']
		document.status = 3
		document.save()

		validated_data['created_by'] = self.context['request'].user

		return super(VerificationSerializer, self).create(validated_data)
