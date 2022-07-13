from django.db import models
from django.core.exceptions import ValidationError
from .manga import Manga
import numpy


class Page(models.Model):

	def descriptor_default():
		return {"descriptor": numpy.ndarray, "nfeatures": int}

	def validate_descriptor(value):
		try:
			if type(value["descriptor"]) != numpy.ndarray:
				raise ValidationError("descriptor must be an array")
			elif type(value["nfeatures"]) != int:
				raise ValidationError("nfeatures must be an integer")
		except KeyError:
			raise ValidationError("input error")

	manga_id = models.ForeignKey(Manga, blank=True, on_delete=models.CASCADE, related_name='page')
	page = models.PositiveSmallIntegerField(null=False, blank=True)
	descriptor = models.JSONField(null=False, blank=True, default=descriptor_default, validators=[validate_descriptor])
	computed = models.DateField(null=False, blank=True, auto_now=True)

	class Meta:
		ordering = ['manga_id','page']
		get_latest_by = 'computed'

	def __str__(self):
		return self.computed

	@classmethod
	def can_add(self, manga_id: int, page_no: int) -> bool:
		"""Check that new manga is already exist in manga data or not.
		
		Args:
			manga_id: manga id of page
			page_no: new manga page
		Returns:
			bool: True, page of manga does not exist, False otherwise.
		"""
		try:
			manga = Manga.objects.get(id=manga_id)
			page = Page.objects.filter(manga_id=manga).get(page=page_no)
		except:
			return True
		return False