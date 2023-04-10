

class ASTReformatter():
  def __init__(self, args):
    self.function_names = args.keys()
    self.output_structure = []
    
  def run(self, filtered_ast):
    self.search_ast(filtered_ast)
    return self.output_structure

  def search_ast(self, filtered_ast):
    calls = filtered_ast['calls']
    for call in calls:
      self.search_call(call)

    function_defs = filtered_ast['function_defs']
    for function_def in function_defs:
      self.search_function_def(function_def)
  
  def search_value(self, value):
    if isinstance(value, dict) and 'type' in value.keys():
      if value['type'] == 'call':
        self.search_call(value)
      elif value['type'] == 'list' or value['type'] == 'set' or value['type'] == 'tuple':
        self.search_iterable(value)
      elif value['type'] == 'dict':
        self.search_dict(value)

  def search_iterable(self, iterable):
    for element in iterable['elements']:
      self.search_value(element)

  def search_dict(self, dict):
    for key, value in dict['key_values']:
      self.search_value(key)
      self.search_value(value)

  def search_call(self, call):
    if call['function'] in self.function_names:
      self.output_structure.append(call)
    for arg in call['args']:
      self.search_value(arg)
    for keyword in call['keywords']:
      self.search_value(keyword['value'])

  def search_function_def(self, func_def):
    for call in func_def['calls']:
      self.search_call(call)

