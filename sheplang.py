import re

# Parser
# 	- Tokenizer (Lexer): Split input into discrete tokens
#	- Syntactic Analysis: construct AST (Abstract Syntax Tree)

# Parse a command outline and construct a ShepCMD object.
# "/watchlist add Player:player String:reason='Toxicity' Duration:time=1d" 
# => Tokenizer =>
# ['watchlist', 'add', 'Player', ':', 'player', 'String', ':', 'reason', '=', ,"\'", 'Toxicity', "\'", 'Duration', ':', 'time', '=', '1d']
# => Syntactic analyzer =>
# AST = {
# 	'Command Outline'
# 	'outline': [
# 		'watchlist',
# 		'add',
# 		{
# 			'ShepParam'
# 			'type': 'Player'
# 			'name': 'player'
# 			'default_val': None
# 		},
# 		{
# 			'ShepParam'
# 			'type': 'String'
# 			'name': 'reason'
# 			'default_val': 'Toxicity'
# 		},
# 		{
# 			'ShepParam'
# 			'type': 'Duration'
# 			'name': 'player'
# 			'default_val': Duration('1d')
# 		}
# 	]
# }

class ShepType():
	def __init__(self, class_name, constructor):
		self.class_name = class_name
		self.constructor = constructor
	def create(self, value):
		try:
			return self.constructor(value)
		except:
			self.error(value)
	def error(self, value):
		raise "{0} is not a valid {1}".format(value, self.class_name)
	def __repr__(self):
		return self.class_name

class ShepParam:
	def __init__(self, shep_type, var_name, default_val):
		self.type = shep_type
		self.var_name = var_name
		self.default_val = self.type.create(default_val)
	def __repr__(self):
		return '{0}:{1}={2}'.format(self.type, self.var_name, self.default_val)

class ShepCMD:

	types = {
		'String': ShepType('String', str),
		'Integer': ShepType('Integer', int),
	}
	
	def __init__(self, outline):
		self.name, self.params = ShepCMD.parse(outline)

	def parse(outline):
		tokens = ShepCMD.tokenize(outline)
		return ShepCMD.AST(tokens)

	def tokenize(outline):
		# TODO: make lexer more sophisticated, handling errors and allowing spaces within quotations
		return outline.split()

	def AST(tokens):
		# TODO: make more sophisticated, handling errors and allowing all characters within quotations,
		# disallowing optional params before non_optional params, and checking for name collisions
		cmd_name = []
		outline = []
		for token in tokens:
			if ':' in token:
				type_name_val = re.split(':|=', token)
				if len(type_name_val) == 3:
					shep_type, var_name, default_val = type_name_val
					shep_type = ShepCMD.types[shep_type]
				else:
					shep_type, var_name = type_name_val
					shep_type = ShepCMD.types[shep_type]
					default_val = None
				param = ShepParam(shep_type, var_name, default_val)
				outline.append(param)
			else:
				# token is a keyword
				cmd_name.append(token)

		
		cmd_name = ' '.join(cmd_name)
		params = outline
		return cmd_name, outline
		

	def __repr__(self):
		return "{0} \n {1}".format(self.name, self.params)

# write = ShepCMD('watchlist write String:str=bob Integer:value=3')