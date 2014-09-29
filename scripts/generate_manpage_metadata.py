import os
import os.path
import urllib
from bs4 import BeautifulSoup
import json
import re

if __name__ != '__main__':
    print 'This script is not meant to be imported!'
    exit()

c_function_signature_re = re.compile(ur'(.*)[(](.*)[)];')
include_re = re.compile(ur'#include\s+[<](.+)[>]\s*(.*)\s*')
define_re = re.compile(ur'#define\s+(.+)\s*')


def get_param_type_and_name(param_str):
    param = param_str.strip().split()
    param_type = ' '.join(param[:-1])
    param_var_name = param[-1]
    if param_var_name[0] == '*':
        param_type += ' *'
        param_var_name = param_var_name[1:]
    return param_type, param_var_name


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
    function_signatures = []
    hash_includes = []
    hash_defines = []
    # TODO: This script needs to be changed
    # I realized it is better to separate man page index and autocomplete metadata into separate json files
    if text:
        for line in text.split('\n\n'):
            line = line.strip()
            c_function_signature_match = re.match(c_function_signature_re, ' '.join(line.split()))
            if c_function_signature_match:
                # Function signature
                parameters = []
                for param in c_function_signature_match.group(2).split(','):
                    param = get_param_type_and_name(param)
                    parameters.append({
                        'type': param[0],
                        'var': param[1]
                    })
                function_type_and_name = get_param_type_and_name(c_function_signature_match.group(1))
                function_signatures.append({
                    'return_type': function_type_and_name[0],
                    'name': function_type_and_name[1],
                    'parameters': parameters
                })
            else:
                for l in line.split('\n'):
                    l = l.strip()
                    include_match = re.match(include_re, l)
                    define_match = re.match(define_re, l)
                    if include_match:
                        # include
                        hash_includes.append({
                            'file_path': include_match.group(1),
                            'comments': include_match.group(2)
                        })
                    elif define_match:
                        # define
                        hash_defines.append({
                            'text': define_match.group(1)
                        })
                    else:
                        # TODO: some function signatures do not get parsed
                        # TODO: some functions need special linker flags, parse them too
                        pass
                        #print l
    return function_signatures, hash_includes, hash_defines

# sysassets man pages directory
if os.path.basename(os.getcwd()) == 'scripts':
    sysassets_dir = '../'
else:
    sysassets_dir = './'
sysassets_dir = os.path.abspath(sysassets_dir)
man_pages_path = os.path.join(sysassets_dir, 'man_pages/')

# Man pages metadata output json file
man_page_index_json_out_filename = os.path.join(man_pages_path, 'sys_man_page_index.json')
syscall_metadata_json_out_filename = os.path.join(man_pages_path, 'syscall_metadata.json')

# Directory to man pages in HTML form, which contains index.html
man_pages_html_path = os.path.join(man_pages_path, 'html')

# List of man page section directories (man1, man2, ...)
man_pages_section_dirs = next(os.walk(man_pages_html_path))[1]

# The list containing the man pages index, to be converted to json later
man_page_index = []

# The list of system calls and their metadata for autocomplete support in sysbuild
syscalls = []

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

                # Do not include URL to keep JSON size small, as it can be constructed on the client
                man_page_index.append({
                    'name': man_page_name,
                    'section': section,
                    'summary': summary,
                    #'url': html_url
                })

                # Syscall metadata
                synopsis = soup.h2.find_next_sibling('pre')
                synopsis_text = ''
                if synopsis:
                    synopsis_text = synopsis.get_text()
                function_metadata = parse_synopsis_text(synopsis_text)
                if function_metadata[0] or function_metadata[1] or function_metadata[2]:
                    # TODO: this format needs to be changed to have functions at the top level of the list
                    syscalls.append({
                        'man_page': man_page_name,
                        'functions': function_metadata[0],
                        'includes': function_metadata[1],
                        'defines': function_metadata[2]
                    })

with open(man_page_index_json_out_filename, 'w') as json_out_file:
    json.dump(man_page_index, json_out_file, indent=4, sort_keys=True)

with open(syscall_metadata_json_out_filename, 'w') as json_out_file:
    json.dump(syscalls, json_out_file, indent=4, sort_keys=True)
