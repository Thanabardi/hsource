def descending_bisect(list, value, key):
  """
  insert value in list of dict by desending order
    Ex. descending_bisect(matches_list, data, "match")
  """
  lo, hi = 0, len(list)
  while lo < hi:
    mid = (lo+hi)//2
    if value > list[mid][key]: hi = mid
    else: lo = mid+1
  list.insert(lo, value)