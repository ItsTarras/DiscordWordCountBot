import re

def remove_special_characters(input_string):
    # Define a regular expression pattern to match non-alphanumeric characters
    pattern = re.compile(r'[^a-zA-Z0-9\s]')
    
    # Use the sub() function to replace matched characters with an empty string
    result = re.sub(pattern, '', input_string)
    
    return result
