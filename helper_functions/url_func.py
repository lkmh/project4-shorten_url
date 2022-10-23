import hashlib
import re
import requests

def hash_func_shorten_url(original_url):
    """ hash the original url to 7 """
    hash_url = hashlib.sha1(original_url.encode('utf-8')).hexdigest()[:7]
    return hash_url

### stuff to bring to a separate utils ####
def format_url(url):
  if not re.match('(?:http|ftp|https)://', url):
    return 'http://{}'.format(url)
  return url

def is_url_valid(input_url):
    try: 
        response = requests.get(format_url(input_url))
        if response.status_code == 200:
            return True 
        else:
            return False 
    except:
        return False 