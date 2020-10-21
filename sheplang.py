import shlex

# Parser
# 	- Tokenizer (Lexer): Split input into discrete tokens
#	- Syntactic Analysis: construct AST (Abstract Syntax Tree) from tokens

def smart_split(string, delimeters=' '):
	# split, ignoring delimiteres which are in quotes
	splitter = shlex.shlex(string, posix=True)
	splitter.whitespace += delimeters
	splitter.whitespace_split = True
	return list(splitter)

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
		'Number': ShepType('Float', float)
	}

	def __init__(self, outline, func=None):
		self.name, self.params, self.optional_params = ShepCMD.parse(outline)
		self.func = func

	def execute(input):
		args = smart_split(input)

	def parse(outline):
		tokens = ShepCMD.tokenize(outline)
		return ShepCMD.AST(tokens)

	def tokenize(outline):
		# TODO: make lexer more sophisticated, handling errors and allowing spaces within quotations
		return smart_split(outline)

	def AST(tokens):
		# TODO: make more sophisticated, handling errors and allowing all characters within quotations,
		# disallowing optional params before non_optional params, and checking for name collisions
		cmd_name = []
		params = []
		optional_params = []
		for token in tokens:
			if ':' in token:
				type_name_val = smart_split(token, ':=')
				if len(type_name_val) == 3:
					shep_type, var_name, default_val = type_name_val
					shep_type = ShepCMD.types[shep_type]
					param = ShepParam(shep_type, var_name, default_val)
					optional_params.append(param)
				else:
					shep_type, var_name = type_name_val
					shep_type = ShepCMD.types[shep_type]
					default_val = None
					param = ShepParam(shep_type, var_name, default_val)
					params.append(param)
			else:
				# token is a keyword
				cmd_name.append(token)

		
		cmd_name = ' '.join(cmd_name)
		return cmd_name, params, optional_params
		

	def __repr__(self):
		return "{0}\n{1}\n{2}".format(self.name, self.params, self.optional_params)

write = ShepCMD('watchlist write String:str Integer:value=3')