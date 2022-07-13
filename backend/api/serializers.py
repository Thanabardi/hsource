from rest_framework.serializers import ModelSerializer
from .models.manga import Manga
from .models.manga_pages import Page
from .models.manga_tag import Tag


class MangaSerializer(ModelSerializer):
  class Meta:
    model = Manga
    fields = '__all__'

class PageSerializer(ModelSerializer):
  class Meta:
    model = Page
    fields = '__all__'

class TagSerializer(ModelSerializer):
  class Meta:
    model = Tag
    fields = '__all__'