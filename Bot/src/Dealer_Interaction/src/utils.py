from telegram import ReplyKeyboardMarkup
import json, re 

class Utils(object):
	def __init__(self):
		#self.categories_file = "Dealer_Interaction/src/files/_categories.json"
		self.categories_file = "files/_categories.json"	#<--- only for test and __main__

	def isDigit(self, string):
		p = re.compile(r'\d+(\.\d+)?$')
		if ',' in string:	string = string.replace(',', '.')
		if p.match(string):	return True
		return False

	def truncate_float(self, string):
		if ',' in string:	string = string.replace(',', '.')
		float_string = float(string)
		return round(float_string, 2)

	def get_content_of_file(self):
		file = open(self.categories_file, 'r')
		file_content = json.load(file)
		file.close()
		return file_content


	def all_natural_keys_in_file(self):
		content = self.get_content_of_file()
		return [item['natural_key'].lower() for item in content]

	def is_category_in_file(self, category_name):
		if category_name.lower() in self.all_natural_keys_in_file():	return True
		return False

	
	"""
		Ritorna una lista contenente tutti i nomi delle sottocategorie
	"""
	def get_subcategories_name_by_category(self, category_name):
		to_ret = []
		if self.is_category_in_file(category_name):
			content = self.get_content_of_file()
			for item in content:
				if item['natural_key'].lower() == category_name.lower():
					for sub_cat in item['sub_categories']:	to_ret.append(list(sub_cat.keys())[0])
			return to_ret
		else:	return	to_ret


	""" 
	Ritorna una lista di dizionari!
	Utils.get_subcategory_products("alimentari", "Acqua") = [{'Nepi': '1.5L'}, {'Panna': '1.5L'}, {'Ferrarelle': '1.5L'},...]
	"""
	def get_subcategory_products(self, category_name, subcategory_name):
		if self.is_category_in_file(category_name):
			content = self.get_content_of_file()
			for item in content:
				if item['natural_key'].lower() == category_name.lower():
					for sub_cat in item['sub_categories']:
						if list(sub_cat.keys())[0].lower() == subcategory_name.lower():	return list(sub_cat.values())[0]
		return []


	def make_keyboard(self, alist, parti): 
	    length = len(alist)
	    keyboard =  [alist[i*length // parti: (i+1)*length // parti] for i in range(parti)]
	    return ReplyKeyboardMarkup(keyboard)


if __name__ == '__main__':
	Utils = Utils()
	import random
	content = Utils.get_subcategories_name_by_category("alimentari")
	subcategory = random.choice(content)
	print(subcategory)
	content = Utils.get_subcategory_products("alimentari", subcategory)
	print(content)
	


