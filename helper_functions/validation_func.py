import validators 
import re

def is_URL_valid(input_url):
    result = validators.url(input_url)
    if result != True:
        return False
    return result


def is_Email_valid(input_email):
    result = validators.email(input_email)
    if result != True:
        return False
    return result


def is_Password_length_valid(input_password):
    result = validators.length(input_password, min=6, max=10)
    if result != True:
        return False
    return result

def is_Password_valid(input_password):
    """ Should have at least one number.
        Should have at least one uppercase and one lowercase character.
        Should have at least one special symbol.
        Should be between 6 to 10 characters long. """
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,10}$"
    # compiling regex
    pat = re.compile(reg)
      
    # searching regex                 
    valid = re.search(pat, input_password)
      
    # validating conditions
    if valid:
        return True
    else:
        return False 
