""" 
Include functions:
	Indicate if a str can be converted to int

"""

def int_in_disguise(s):
	try: 
		int(s)
		return True
	except ValueError:
		return False
