from django.db import models
from django.core.exceptions import ValidationError

class Tag(models.Model):

	# def validate_manga(value):
	# 	try:
	# 		if type(value) != list:
	# 			raise ValidationError("manga must be list")
	# 	except KeyError:
	# 		raise ValidationError("input error")

	tag_id = models.PositiveIntegerField(primary_key=True, blank=True)
	type = models.CharField(null=False, blank=True, max_length=255)
	name = models.CharField(null=False, blank=True, unique=True, max_length=255)

	class Meta:
		ordering = ['tag_id', 'type', 'name']

	def __str__(self):
		return self.name

	# @classmethod
	# def can_add_manga(self, tag_id: int, manga_id: int) -> bool:
	# 	"""Check that manga is already exist in tag manga or not.

	# 	Args:
	# 		manga_id: new manga
	# 	Returns:
	# 		bool: True, manga does not exist, False otherwise.
	# 	"""
	# 	manga = Tag.objects.filter(id=tag_id).get(manga)
	# 	if manga_id in manga:
	# 		return False
	# 	else:
	# 		return True
