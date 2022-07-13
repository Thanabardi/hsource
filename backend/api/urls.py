from django.urls import path
from . import views

urlpatterns = [
  path('', views.getRoutes, name='routes'),
  path('manga/', views.manga_list, name='manga_list'),
  path('manga/<str:manga_slug>', views.manga, name='manga'),
  path('manga/<str:manga_slug>/', views.manga_pages, name='manga_pages'),
  path('manga/<str:manga_slug>/<str:page_no>', views.manga_page, name='manga_page'),

  path('tag/', views.tag_list, name='tag_list'),
  path('tag/<str:tag_slug>', views.tag, name='tag'),
  path('tag/<str:tag_slug>/', views.tag_manga, name='tag_manga'),
]