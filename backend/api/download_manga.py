import os
import json
from config import *
from feature_matching import *

manga_path = 'backend/api/manga'
images_list = []
original_img_name = []

manga_list = os.listdir(manga_path)

for data in manga_list:
  with open(f'backend/api/manga/{data}', 'r') as manga:
    m = json.load(manga)
    media_id = m['media_id']
    manga = {
      "id": m['id'],
      "media_id": m['media_id'],
      "title": m['title'],
      "upload_date": "2022-1-1",
      "num_favorites": m['num_favorites'],
      "tag": m['tag']
    }

    page = 1
    page_list = []
    for image in m['images']['pages']:
      img = load_image(f'https://i.manga.net/galleries/{media_id}/{page}.jpg')
      # img = cv2.resize(img, (210, 297), interpolation = cv2.INTER_AREA)
      des = findDescriptor(img)
      print(type(des))
      data = {
        "page": page,
        "descriptor": 
        {
          "descriptor": des,
          "nfeatures": N_FEATURES
        }
      }
      page_list.append(data)
      page += 1
      break