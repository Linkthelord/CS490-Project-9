import os
import re

def is_pattern_match(path, patterns):
  for pattern in patterns:
    if re.search(pattern, path) != None:
      return True
  return False

def crawl_directory(path, ignore_list):
  '''Crawls the directory starting at the path to find file paths that are valid.

  crawl_directory traverses the 'path' in BFS fashion and identifies all the
  files that are not specified by ignore_list either via pattern or specific
  path. If files are excluded using '!', then they are considered 'excluded'
  from the ignore patterns and are represented in 'include_patterns' or
  'include_directories' depending on how they are specified in .ignore
  (i.e. they have a backslash at the end - e.g. test/).

  Example:
  └── my_project
      ├── Test/
      │   └── test.py
      ├── Help/
      │   └── helpers.py
      └── configs.py

  ignore_list = {}
  ignore_list['directories'] = ['Help/']
  ignore_list['name_patterns'] = ['configs.py']
  ignore_list['include_patterns'] = ['test.py']
  ignore_list['include_directories'] = ['Test/']

  crawl_directory(my_project, ignore_list) -> ['my_project/Test/test.py']
  '''
  
  path = os.path.abspath(path)
  paths = []

  for root, dirs, files in os.walk(path, topdown = True):
    new_dirs = []
    for dir_path in dirs:
    
      in_include_list = (len(ignore_list['include_patterns']) > 0 or len(ignore_list['include_directories']) > 0) and (is_pattern_match(dir_path, ignore_list['include_patterns']) or is_pattern_match(dir_path + '/', ignore_list['include_directories']))
      in_ignore_list = (len(ignore_list['name_patterns']) > 0 or len(ignore_list['directories']) > 0) and (is_pattern_match(dir_path, ignore_list['name_patterns']) or is_pattern_match(dir_path + '/', ignore_list['paths']))

      dir = os.path.join(root, dir_path)
      if not in_include_list and not in_ignore_list:
        new_dirs.append(dir)
      elif in_include_list and not in_ignore_list:
        new_dirs.append(dir)
      elif in_include_list and in_ignore_list:
        new_dirs.append(dir)

    dirs[:] = new_dirs
    for file_name in files:
      in_include_list = len(ignore_list['include_patterns']) > 0 and is_pattern_match(file_name, ignore_list['include_patterns'])
      in_ignore_list = len(ignore_list['name_patterns']) > 0 and is_pattern_match(file_name, ignore_list['name_patterns'])

      file_path = os.path.join(root, file_name)
      if not in_include_list and not in_ignore_list:
        paths.append(file_path)
      elif in_include_list and not in_ignore_list:
        paths.append(file_path)
      elif in_include_list and in_ignore_list:
        paths.append(file_path)

  return paths
