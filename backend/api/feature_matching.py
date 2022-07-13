import cv2
import urllib.request
import numpy as np
from config import *
from utils import descending_bisect


def load_image(url):
  """Load image by the URL"""
  req = urllib.request.urlopen(url)
  arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
  img = cv2.imdecode(arr, -1)
  return img


def findDescriptor(image):
  """Find descriptor of an image"""
  orb = cv2.ORB_create(nfeatures=N_FEATURES)
  kb, des = orb.detectAndCompute(image, None)
  return des


def find_best_match(img, desList):
  """Find best match of img descriptor and image in desList"""
  orb = cv2.ORB_create(nfeatures=N_FEATURES)
  img_kp, img_des = orb.detectAndCompute(img, None)
  bf = cv2.BFMatcher()
  best_matches, index_count = 0, 0
  for des in desList:
    good_matches = 0
    matches = bf.knnMatch(des, img_des, k=2)
    for m, n in matches:
      if m.distance < MATCH_DIST_DIVISOR * n.distance:
        good_matches += 1
    if (good_matches >= MATCH_THRESHOLD and good_matches > best_matches):
      best_matches = {"page": index_count+1, "match":  good_matches}
    index_count += 1
  return best_matches
