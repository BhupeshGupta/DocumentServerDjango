from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers


class FilesKeyRelatedField(serializers.HyperlinkedRelatedField):
	default_error_messages = {
		'required': 'This field is required.',
		'does_not_exist': 'Invalid pk "{pk_value}" - object does not exist.',
		'incorrect_type': 'Incorrect type. Expected pk value, received {data_type}.',
	}

	def __init__(self, **kwargs):
		self.pk_field = kwargs.pop('pk_field', None)
		super(FilesKeyRelatedField, self).__init__(**kwargs)

	def to_internal_value(self, data):
		if self.pk_field is not None:
			data = self.pk_field.to_internal_value(data)
		try:
			return self.get_queryset().get(pk=data)
		except ObjectDoesNotExist:
			self.fail('does_not_exist', pk_value=data)
		except (TypeError, ValueError):
			self.fail('incorrect_type', data_type=type(data).__name__)