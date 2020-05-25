import json
from datetime import datetime
from datetime import timedelta
from collections import defaultdict
class Dealer_Persistence(object):
	def __init__(self):
		try:
			self.persistence_filename = "Dealer_Interaction/src/files/dealer_persistence.json"
			self.read_persistence()
		except:	self.persistence_filename = "files/dealer_persistence.json"	#<--- only for test and __main__

	
	def write_persistence(self, content):
		file = open(self.persistence_filename, 'w')
		json.dump(content, file,indent=4)
		file.close()
	
	def read_persistence(self):
		file = open(self.persistence_filename)
		content = json.load(file)
		file.close()
		return content

	def append_dealer_persistence(self, dealer_token, dealer_infos):
		content = self.read_persistence()
		content[dealer_token] = dealer_infos
		self.write_persistence(content)


	def set_now_date_by_token(self, token):
		content = self.read_persistence()
		content[token]['shopping_window_date'] = self.format_datetime(datetime.now())
		self.write_persistence(content)

	def format_datetime(self, datetime_obj):
		return datetime_obj.strftime("%d/%m/%YCOLLIGO%H:%M")	#"12/05/2020COLLIGO18:53"

	def is_token_in_persistence(self, token):
		content = self.read_persistence()
		return token in content

	def get_shopping_window_date_day_by_token(self, token):
		content = self.read_persistence()
		return int(content[token]['shopping_window_date'].split('/')[0])

	def get_shopping_window_by_token(self, token):
		content = self.read_persistence()
		return content[token]['shopping_window_list']
	def extract_names_from_shopping_window(self, shopping_window_list):
		to_ret = []
		for item in shopping_window_list:	to_ret.append(item['name'])
		return to_ret

	def is_product_in_shopping_window(self, shopping_window_list, product_name):
		for item in shopping_window_list:
			if item['name'] == product_name:	return True
		return False
	
	def get_product_details_by_product_name(self, shopping_window_list, product_name):
		for item in shopping_window_list:
			if item['name'] == product_name: return item
		return {}





	# [{'name': "La Trappe Isid'or", 'price': 15.0, 'unit': '0.33l', 'quantity': 3}, ...]	<--- added quantity
	def sum_up_all_shopping_window_prices(self, shopping_window_list, token):
		c = defaultdict(int)
		c.clear()
		

		for d in shopping_window_list:	c[d['name']] += d['price']
		
		new_shopping_window_list = [{'name': name, 'price': price} for name, price in c.items()]
		c.clear()

		to_ret = self.how_many_units(new_shopping_window_list, token)
		return to_ret
	
	def get_original_product_details(self, product_name, token):	# pass its token
		content = self.read_persistence()
		if token in content:
			for item in content[token]['shopping_window_list']:
				if item['name'] == product_name:	return item
		return {}

	def decrement_quantity(self, shopping_cart, product_name, token):
		for item in shopping_cart:
			if item['name'] == product_name:
				item['quantity'] -= 1
				original_product_details = self.get_original_product_details(product_name, token)
				original_price = original_product_details['price']
				item['price'] -= original_price
			if item['quantity'] == 0:	shopping_cart.remove(item)
		return shopping_cart # remember to do side effect

	def how_many_units(self, shopping_window_list, token):
		for item in shopping_window_list:
			product_name, product_price = item['name'], item['price']
			original_product_details = self.get_original_product_details(product_name, token)
			original_price, original_unit = original_product_details['price'], original_product_details['unit']
			if original_price == product_price:
				item.update({"unit":original_product_details['unit'], "quantity":1})
			else:
				how_many_units = int(product_price / original_price)
				item.update({"unit":original_product_details['unit'], "quantity":how_many_units})
		return shopping_window_list


	def get_categories_list_by_token(self, token):
		content = self.read_persistence()
		return content[token]['categories_list']
	def set_categories_list_by_token(self, token, categories_list):
		content = self.read_persistence()
		content[token]['categories_list'] = categories_list
		self.write_persistence(content)


	def get_group_tytle_by_token(self, token):
		content = self.read_persistence()
		return content[token]['group_title']

	def reset_date_by_token(self, token):
		content = self.read_persistence()
		old_date = content[token]['shopping_window_date']
		old_date_datetime = datetime.strptime(old_date, "%d/%m/%YCOLLIGO%H:%M")

		new_datetime = old_date_datetime - timedelta(days=1)
		new_date_datetime = self.format_datetime(new_datetime)
		content[token]['shopping_window_date'] = new_date_datetime
		self.write_persistence(content)

	def remove_user_by_token(self, token):
		content = self.read_persistence()
		del content[token]
		self.write_persistence(content)
		

if __name__ == '__main__':
	Dealer_Persistence_Obj = Dealer_Persistence()
	# token = "eJzTNTG0MDA3MDM0AwAK3QH/"
	# Dealer_Persistence_Obj.remove_user_by_token(token)

	Dealer_Persistence_Obj.get_original_product_details("Ferrarelle", "eJzTNTG0MDA3MDM0AwAK3QH/")
