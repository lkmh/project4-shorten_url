import hashlib
import re

def hash_func_shorten_url(original_url):
    """ hash the original url to 7 """
    hash_url = hashlib.sha1(original_url.encode('utf-8')).hexdigest()[:7]
    return hash_url

### stuff to bring to a separate utils ####
def formaturl(url):
  if not re.match('(?:http|ftp|https)://', url):
    return 'http://{}'.format(url)
  return url