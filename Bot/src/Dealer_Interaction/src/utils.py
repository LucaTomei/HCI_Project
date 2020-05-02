from telegram import ReplyKeyboardMarkup
import json, re 

class Utils(object):
	def __init__(self):
		self.categories_file = "Dealer_Interaction/src/files/categories.json"
		#self.categories_file = "files/categories.json"	#<--- only for test and __main__

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

	def get_product_list_by_category_name(self, category_name):
		content = self.get_content_of_file()
		return [item['products'] for item in content if item['natural_key'] == category_name][0]

	def all_natural_keys_in_file(self):
		content = self.get_content_of_file()
		return [item['natural_key'] for item in content]

	def is_category_in_file(self, category_name):
		if category_name in self.all_natural_keys_in_file():	return True
		return False

	def is_product_in_categories(self, product_name):
		for item in self.get_content_of_file():
			for product in item['products']:
				if product == product_name:	return True

	def make_keyboard(self, alist, parti): 
	    length = len(alist)
	    keyboard =  [alist[i*length // parti: (i+1)*length // parti] for i in range(parti)]
	    return ReplyKeyboardMarkup(keyboard)


if __name__ == '__main__':
	Utils = Utils()
	# content = Utils.is_category_in_file("panificio")
	# print(content)
	stringa = "0.1022222"
	isDigit = Utils.isDigit(stringa)
	print(isDigit)


