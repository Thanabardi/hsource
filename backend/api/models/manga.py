from django.db import models
from django.core.exceptions import ValidationError
from .manga_tag import Tag

class Manga(models.Model):

	def title_default():
		return {"english": str, "japanese": str, "pretty": str}
	
	def validate_title(value):
		try:
			if type(value["englist"]) != str:
				raise ValidationError("englist title must be a string")
			elif type(value["japanese"]) != str:
				raise ValidationError("japanese title must be a string")
			elif type(value["pretty"]) != str:
				raise ValidationError("pretty title must be a string")
		except KeyError:
			raise ValidationError("input error")

	id = models.PositiveIntegerField(primary_key=True, blank=True)
	media_id = models.CharField(null=False, blank=True, unique=True, max_length=255)
	title = models.JSONField(null=False, blank=True, default=title_default, validators=[validate_title])
	upload_date = models.DateField(null=False, blank=True)
	num_favorites = models.PositiveIntegerField(null=False, blank=True, default=0)
	tag = models.ManyToManyField(Tag, blank=True, related_name='manga')

	class Meta:
		ordering = ['id']
		get_latest_by = 'upload_date'

	def __str__(self):
		return self.id

	# @classmethod
	# def can_add(self, manga_id: int) -> bool:
	# 	"""Check that new manga is already exist in manga data or not.
		
	# 	Args:
	# 		manga_id: new manga id
	# 	Returns:
	# 		bool: True, manga does not exist, False otherwise.
	# 	"""
	# 	try:
	# 		manga = Manga.objects.get(id=manga_id)
	# 	except:
	# 		return True
	# 	return False
