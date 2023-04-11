import os
import re

def handle_pattern(path):
  if '**' in path:
    index = path.index('**')
    left = path[0: index]
    right = path[index + 2: len(path)]
    return handle_pattern(left) + handle_pattern(right)

  pattern = path.replace('.', r'\.')
  pattern = pattern.replace('*', '.*')
  pattern = pattern.replace('?', '.')
  pattern = pattern.replace('!', '^')
  return ['^' + pattern + '$']

def create_ignore_dict():
  '''Returns a dictionary containing regex patterns that should be
  ignored/included by the file crawler. The ignore dictionary is created using
  the .ignore file. Files can be excluded using the '!' prefix. '#' comments
  are supported.
  '''

  output_dict = {'paths': [], 'ignore': [], 'include': [], 'include_paths': []}
  try:
    with open('.ignore') as f:
      directory_patterns = []
      name_patterns = []
      include_patterns = []
      include_path_patterns = []

      for line in f:
        line = line.strip()
        if line.startswith('#') or line == '':
          # Do nothing
          continue
        elif line.startswith('!'):
          pattern = handle_pattern(line[1:])
          if line.endswith('/'):
            include_path_patterns = include_path_patterns + pattern
          else:
            include_patterns = include_patterns + pattern
        elif line.endswith('/'):
          directory_patterns = directory_patterns + handle_pattern(line)
        else:
          name_patterns = name_patterns + handle_pattern(line)

      output_dict['paths'] = directory_patterns
      output_dict['ignore'] = name_patterns
      output_dict['include'] = include_patterns
      output_dict['include_paths'] = include_path_patterns
  except Exception as e:
    # Do nothing if the file does not exist
    print(e)
    return output_dict

  return output_dict
