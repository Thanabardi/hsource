from django.contrib import admin

from .models.manga import Manga
from .models.manga_pages import Page
from .models.manga_tag import Tag


admin.site.register(Manga)
admin.site.register(Page)
admin.site.register(Tag)
