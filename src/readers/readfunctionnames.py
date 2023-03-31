import json
import os

def read_function_names(path):
  '''
  Reads the JSON file specified by the path and outputs a list of function
  names and arguments corresponding to each function name.

  Example:
  {
    "module": "module",
    "functions": [
      {
        "func1": [
          "arg1", ...
        ]
      },
      "func2" 
    ]
  }

  yields

  func_names = {
    'module.func1': ['arg1'],
    'module.func2': []
  }
  '''
  try:
    f = open(path, 'r')
    json_data = json.load(f)
    f.close()
  except Exception as e:
    print('Error occurred while reading function names file:', path)
    print('Error:', e)
    return {}

  func_names = {}
  try:
    for module in json_data['functions']:
      module_name = None
      if 'module' in module.keys():
        module_name = module['module']
      functions = module['functions']

      for func in functions:
        function_name = func
        arg_names = []
        if isinstance(func, dict):
          function_name = func['function_name']
          arg_names = func['arg_names']

        function_name = module_name + '.' + function_name if module_name != None else function_name
        func_names[function_name] = arg_names
    
    module_keys = list(func_names.keys())
    module_keys.sort()
    sorted_dict = {i: func_names[i] for i in module_keys}
    func_names = sorted_dict
  except Exception as e:
    print('Note: function names JSON file has incorrect format:', os.path.abspath(path))
    print('Ensure file follows the format:', """
      {
        "functions": [
          {
            "module": "[module name]",
            "functions": [
              "func1": {
                "arg_names": [
                  "arg1", ...
                ]
              },
              "func2", ... 
            ]
          }
        ]
      }
    """)
    print('Error:', e)
  return func_names