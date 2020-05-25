from telegram import ReplyKeyboardMarkup
import json, re, base64, zlib

from Dealer_Interaction.src import dealer_persistence

class Utils(object):
	def __init__(self):
		self.back_button = "🔙Indietro🔙"
		try:	self.categories_file = "Dealer_Interaction/src/files/categories.json"
		except:	self.categories_file = "files/categories.json"	#<--- only for test and __main__


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


	"""
		Return two tuple lists
		(['Nesquik', 'Nesquik Duo', 'Lion', 'Kellogs Coco Pops', 'Kellogs Special Classic', ...] 
		['950g', '450g', '400g', '400g', '400g', ...])
	"""
	def from_subcat_prod_dict_to_list(self, sub_cat_prod_list):
		names = []
		units = []
		for item in sub_cat_prod_list:
			names.append(*item)
			units.append(list(item.values())[0])
		return (names, units)

	def from_product_name_to_units(self, product_name, tupla_from_subcat_prod_lists):
		(names, units) = tupla_from_subcat_prod_lists
		for i in range(len(names)):
			if names[i].lower() == product_name.lower():	return units[i]
		return ''




	def make_token(self, chat_id):	# make token by group chat_id
		chat_id = str(chat_id).encode("utf-8")
		return base64.encodebytes(zlib.compress(chat_id)).decode("utf-8").replace('\n', '')

	def decrypt_token(self, token):
		token = str(token).encode("utf-8")
		return zlib.decompress(base64.decodebytes(token)).decode("utf-8").replace('\n', '')

	def get_idx_in_shopping_window(self, shopping_window, product_name):
		for i in range(len(shopping_window)):
			if shopping_window[i]['name'].lower() == product_name.lower(): return i
		return -2

	def edit_shopping_window_price(self, shopping_window, product_name, new_price):	# return new shopping_window
		idx_in_shopping_window = self.get_idx_in_shopping_window(shopping_window, product_name)
		shopping_window[idx_in_shopping_window]['price'] = self.truncate_float(new_price)
		return shopping_window 	# now you have to save the new shopping window

	def get_product_infos(self, shopping_window, product_name):
		idx = self.get_idx_in_shopping_window(shopping_window, product_name)
		return shopping_window[idx]

	def tmp_remove_product_from_shopping_window(self,shopping_window, product_name):
		idx = self.get_idx_in_shopping_window(shopping_window, product_name)
		shopping_window.remove(self.get_product_infos(shopping_window, product_name))
		return shopping_window

if __name__ == '__main__':
	Utils = Utils()
	
	# shopping_window =  [{'name': 'Panna', 'price': 1.0, 'unit': '1.5L'}, {'name': 'Ferrarelle', 'price': 1.0, 'unit': '1.5L'}]
	# Utils.tmp_remove_product_from_shopping_window(shopping_window, 'Panna')
	#Utils.edit_shopping_window_price(shopping_window, 'Ferrarelle', "20.1")
	