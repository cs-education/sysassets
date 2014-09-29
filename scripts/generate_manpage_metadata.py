import os
import os.path
import urllib
from bs4 import BeautifulSoup
import json


def parse_synopsis_text(text):
    """
    Parse a Linux Man Page's Synopsis section for C function signatures, #includes and #defines
    Can be used to extract information about a system call, etc.
    :param text: Text (without extra formatting, like HTML tags)
        from the synopsis section of the man page
    :return: A 3-tuple of function signatures, includes and defines. Each 'function signature' is an
        object with function metadata (return type, name, parameters). Each 'include' is a string of the
        #include file path, and each 'define' is the text after #define.
    """
    if text:
        for line in text.split('\n\n'):
            line = line.strip()
            #print repr(' '.join(line.split()))

# sysassets man pages directory
man_pages_path = os.path.abspath('man_pages/')

# Man pages metadata output json file
json_out_filename = os.path.join(man_pages_path, 'sys_man_pages.json')

# Directory to man pages in HTML form, which contains index.html
man_pages_html_path = os.path.join(man_pages_path, 'html')

# List of man page section directories (man1, man2, ...)
man_pages_section_dirs = next(os.walk(man_pages_html_path))[1]

# The list containing the metadata, to be converted to json later
man_pages = []

for section_dir in man_pages_section_dirs:
    print section_dir
    section = int(section_dir[-1])
    section_dir_path = os.path.join(man_pages_html_path, section_dir)

    # Get list of man page html files in the section directory
    file_names = next(os.walk(section_dir_path))[2]

    for man_page_file_name in file_names:
        # Get man page name from filename, e.g., 'accept' from accept.2.html
        man_page_name = man_page_file_name.split('.')[0]
        # Get a relative link to the man page's HTML file
        html_url = urllib.pathname2url(os.path.join('html', section_dir, man_page_file_name))
        with open(os.path.join(section_dir_path, man_page_file_name), 'r') as f:
            soup = BeautifulSoup(f)
            if soup.title.string != 'Invalid Man Page':
                summary = soup.h2.next_sibling.strip()
                synopsis = soup.h2.find_next_sibling('pre')
                synopsis_text = ''
                if synopsis:
                    synopsis_text = synopsis.get_text()
                parse_synopsis_text(synopsis_text)
                # Do not include URL to keep JSON size small, as it can be constructed on the client
                man_pages.append({
                    'name': man_page_name,
                    'section': section,
                    'summary': summary
                    #'url': html_url
                })

with open(json_out_filename, 'w') as json_out_file:
    json.dump(man_pages, json_out_file, indent=4, sort_keys=True)
