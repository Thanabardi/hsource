from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models.manga import Manga
from .models.manga_pages import Page
from .models.manga_tag import Tag
from .serializers import MangaSerializer, PageSerializer, TagSerializer
from django.http.response import Http404

@api_view(['GET'])
def getRoutes(request):

  routes = [
    {
      'Endpoint': '/manga/',
      'method': 'GET, POST',
      'body': {
        "id": "int",
        "media_id": "str",
        "title": 
        {
          "english": "str",
          "japanese": "str",
          "pretty": "str"
        },
        "upload_date": "2022-1-1",
        "num_favorites": "int",
        "tag": [{
          "tag_id": "int",
          "type": "str",
          "name": "str"
        }]
      },
      'description': 'GET all manga and POST new manga'
    },
    {
      'Endpoint': 'manga/<manga_slug>',
      'method': 'GET, PUT',
      'body': '{updated_data}',
      'description': 'GET manga by id and PUT to update manga'
    },
    {
      'Endpoint': '/manga/<manga_slug>/',
      'method': 'GET, POST',
      'body': {
        "page": "int",
        "descriptor": 
        {
          "descriptor": "[]",
          "nfeatures": "int"
        }
      },
      'description': 'GET all manga page and POST new page'
    },
    {
      'Endpoint': '/manga/<manga_id>/<page_no>',
      'method': 'GET, PUT',
      'body': '{updated_data}',
      'description': 'GET page by page_no and PUT to update page'
    },
    {
      'Endpoint': '/tag/',
      'method': 'GET, POST',
      'body': {
        "tag_id": "int",
        "type": "str",
        "name": "str"
      },
      'description': 'GET all tag and POST new tag'
    },
        {
      'Endpoint': 'tag/<tag_slug>',
      'method': 'GET, PUT',
      'body': '{updated_data}',
      'description': 'GET tag by id and PUT to update tag'
    },
    {
      'Endpoint': '/tag/<tag_slug>/',
      'method': 'GET',
      'body': None,
      'description': 'GET all manga by tag id'
    }
  ]

  return Response(routes)


@api_view(['GET', 'POST'])
def manga_list(request):
  """GET all manga and POST new manga"""

  if request.method == 'GET':
    manga = Manga.objects.all()
    serializer = MangaSerializer(manga, many=True)
    return Response(serializer.data)

  if request.method == 'POST':
    data = request.data
    manga = Manga.objects.create(
      id = data["id"],
      media_id = data["media_id"],
      title = data["title"],
      upload_date = data["upload_date"],
      num_favorites = data["num_favorites"]
    )
    for data_tag in data["tag"]:
      try:
        tag = Tag.objects.get(tag_id=data_tag["tag_id"])
        manga.tag.add(tag)
      except:
        tag = Tag.objects.create(
          tag_id = data_tag["tag_id"],
          type = data_tag["type"],
          name = data_tag["name"]
        )
        manga.tag.add(tag)
    serializer = MangaSerializer(manga, many=False)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
def manga(request, manga_slug):
  """GET manga by id and PUT to update manga"""

  manga = Manga.objects.get(id=manga_slug)

  if request.method == 'GET':
    serializer = MangaSerializer(manga, many=False)
    return Response(serializer.data)

  if request.method == 'PUT':
    data = request.data
    tag_list = []
    for data_tag in data["tag"]:
      tag_list.append(data_tag["tag_id"])
      try:
        tag = Tag.objects.get(tag_id=data_tag["tag_id"])
      except:
        tag = Tag.objects.create(
          tag_id = data_tag["tag_id"],
          type = data_tag["type"],
          name = data_tag["name"]
        )
    data["tag"] = tag_list
    serializer = MangaSerializer(instance=manga, data=data)

    if serializer.is_valid():
      serializer.save()
    else:
      return Response(serializer.errors)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def manga_pages(request, manga_slug):
  """GET all manga page and POST new page"""

  if request.method == 'GET':
    manga = Manga.objects.get(id=manga_slug)
    page = Page.objects.filter(manga_id=manga)
    serializer = PageSerializer(page, many=True)
    return Response(serializer.data)

  if request.method == 'POST':
    data = request.data
    if Page.can_add(manga_slug, data["page"]):
      manga = Manga.objects.get(id=manga_slug)
      page = Page.objects.create(
        manga_id = manga,
        page = data["page"],
        descriptor = data["descriptor"]
      )
      serializer = PageSerializer(page, many=False)
      return Response(serializer.data)
    else:
      return Response(f'manga id {manga_slug} page {data["page"]} already exists')

@api_view(['GET', 'PUT'])
def manga_page(request, manga_slug, page_no):
  """GET page by page_no and PUT to update page"""

  manga = Manga.objects.get(id=manga_slug)
  page = Page.objects.filter(manga_id=manga).get(page=page_no)

  if request.method == 'GET':
    serializer = PageSerializer(page, many=False)
    return Response(serializer.data)

  if request.method == 'PUT':
    data = request.data
    serializer = PageSerializer(instance=page, data=data)
    if serializer.is_valid():
      serializer.save()
    else:
      return Response(serializer.errors)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def tag_list(request):
  """GET all tag and POST new tag"""

  if request.method == 'GET':
    tag = Tag.objects.all()
    serializer = TagSerializer(tag, many=True)
    return Response(serializer.data)

  if request.method == 'POST':
    data = request.data
    tag = Tag.objects.create(
      tag_id = data["tag_id"],
      type = data["type"],
      name = data["name"]
    )
    serializer = TagSerializer(tag, many=False)
    return Response(serializer.data)

@api_view(['GET', 'PUT'])
def tag(request, tag_slug):
  """GET tag by id and PUT to update tag"""

  tag = Tag.objects.get(tag_id=tag_slug)

  if request.method == 'GET':
    serializer = TagSerializer(tag, many=False)
    return Response(serializer.data)

  if request.method == 'PUT':
    data = request.data
    serializer = TagSerializer(instance=tag, data=data)

    if serializer.is_valid():
      serializer.save()
    else:
      return Response(serializer.errors)
    return Response(serializer.data)

@api_view(['GET'])
def tag_manga(request, tag_slug):
  """GET all manga by tag id"""

  if request.method == 'GET':
    tag = Tag.objects.get(tag_id=tag_slug)
    manga = Manga.objects.filter(tag=tag)
    serializer_manga = MangaSerializer(manga, many=True)
    return Response(serializer_manga.data)
  
  # if request.method == 'PUT':
  #   data = request.data
  #   if Tag.can_add_manga(tag_id, data["id"]):
  #     serializer = PageSerializer(data, many=True)
  #     serializer.save()
  #     return Response(serializer.data)
  #   else:
  #     return Response(f'tag id {tag_id} manga {data["manga"]} already exists')