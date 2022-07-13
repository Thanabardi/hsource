import cv2
# import numpy as np
import os
import time

N_FEATURES = 5000
MATCH_DIST_DIVISOR = 0.7

"""
Find best match from an image list
"""

orb = cv2.ORB_create(nfeatures=N_FEATURES)

original_image_path = 'backend/api/Original_Image'
img_list = []
original_img_name = []

images_list = os.listdir(original_image_path)

for image_name in images_list:
  image = cv2.imread(f"{original_image_path}/{image_name}", 0)
  img_list.append(image)
  original_img_name.append(os.path.splitext(image_name)[0])

def findDescriptor(images):
  desList = []
  start_time = time.time()
  for image in images:
    kb, des = orb.detectAndCompute(image, None)
    desList.append(des)
  print(f'findDescriptor time: {(time.time() - start_time):.4f} sec')
  return desList

def find_match(img, desList):
  kp2, des2 = orb.detectAndCompute(img, None)
  bf = cv2.BFMatcher()
  matches_list = []
  start_time = time.time()
  for des in desList:
    good_matches = 0
    matches = bf.knnMatch(des, des2, k=2)
    for m, n in matches:
      if m.distance < MATCH_DIST_DIVISOR * n.distance:
        good_matches += 1
    reverse_insort(matches_list, good_matches)
  print(f'findMatch time: {(time.time() - start_time):.4f} sec')
  print(f'match result: {matches_list}')
  return matches_list.index(max(matches_list))

desList = findDescriptor(img_list)

def reverse_insort(list, value):
  lo, hi = 0, len(list)
  while lo < hi:
    mid = (lo+hi)//2
    if value > list[mid]: hi = mid
    else: lo = mid+1
  list.insert(lo, value)

image_crop = cv2.imread("backend/api/Crop_Image/crop_yofukashi_no_uta.jpg")
print(f"your original image is: {original_img_name[find_match(image_crop, desList)]}")


"""
Show and compare 2 different image
"""
# image1 = cv2.imread("backend/api/Crop_Image/crop_jujutsu_kaisen.jpg")
# image2 = cv2.imread("backend/api/Original_Image/original_jujutsu_kaisen.jpg")

# orb = cv2.ORB_create(nfeatures=N_FEATURES)

# kp1, descriptor1 = orb.detectAndCompute(image1, None)
# kp2, descriptor2 = orb.detectAndCompute(image2, None)

# bf = cv2.BFMatcher()
# matches = bf.knnMatch(descriptor1, descriptor2, k=2)

# good_matches = []

# for m, n in matches:
#   if m.distance < MATCH_DIST_DIVISOR * n.distance:
#     good_matches.append([m])

# print(len(good_matches))
# image3 = cv2.drawMatchesKnn(image1, kp1, image2, kp2, good_matches, None, flags=2)

# imagekp1 = cv2.drawKeypoints(image1, kp1, None)
# imagekp2 = cv2.drawKeypoints(image2, kp2, None)

# cv2.imshow('image3', image3)
# cv2.waitKey(0)