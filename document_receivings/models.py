from __future__ import unicode_literals

from django.conf import settings
from django.db import models


class Document(models.Model):
	ref_no = models.CharField(max_length=255, null=False, blank=True)

	doctype = models.CharField(max_length=255)
	docname = models.CharField(max_length=255)
	date = models.DateField()

	status = models.IntegerField(
		choices=((0, 'Pending'), (1, 'Verified'), (2, 'Rejected'), (3, 'Decision Pending')),
		default=0
	)

	created_on = models.DateTimeField(auto_now_add=True)
	verified_on = models.DateTimeField(null=True)

	created_by = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.PROTECT,
		null=True,
		related_name='documents_created'
	)
	verified_by = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.PROTECT,
		null=True,
		related_name='documents_verified'
	)

	@property
	def related_docs(self):
		return Document.objects.filter(ref_no=self.ref_no)

	class Meta:
		unique_together = (('ref_no', 'doctype'),)


class Verification(models.Model):
	document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='verifications')

	status = models.IntegerField(choices=((0, 'Pending'), (1, 'Verified'), (2, 'Rejected')), default=0)

	created_on = models.DateTimeField(auto_now_add=True)
	verified_on = models.DateTimeField(null=True)

	created_by = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.PROTECT,
		null=True,
		related_name='document_verifications_created'
	)
	verified_by = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.PROTECT,
		null=True,
		related_name='document_verifications_verified'
	)

	class Meta:
		permissions = (("can_verify_document", "Can Verify Document"),)


class File(models.Model):
	file = models.FileField()

	size = models.CharField(max_length=255)
	type = models.CharField(max_length=255)
	filename = models.CharField(max_length=255)

	verification = models.ForeignKey(Verification, on_delete=models.CASCADE, related_name="files", null=True)
	document = models.ForeignKey(Document, on_delete=models.CASCADE, null=True, related_name="files")
