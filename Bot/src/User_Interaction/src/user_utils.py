from telegram import ReplyKeyboardMarkup
import base64, zlib

class User_Utils(object):
	def __init__(self):
		self.stop_button = "Fine"

	def init_customer_data(self, chat_id, context):
		if not chat_id in context.user_data:
			context.user_data[chat_id] = {
				"used_token": None,
				"shopping_cart":[],		# [..., {'name': 'Ferrarelle', 'price': 3.0, 'unit': '1.5L'}, ...]
				"tmp_product":None,		# {'name': 'Ferrarelle', 'price': 3.0, 'unit': '1.5L'}
				"products_keyboard":None,
			}

	def get_shopping_cart(self, chat_id, context):
		return context.user_data[chat_id]["shopping_cart"]
	def append_to_shopping_cart(self, chat_id, context, product):
		context.user_data[chat_id]["shopping_cart"].append(product)
	def set_shopping_cart(self, chat_id, context, shopping_cart):	# to set new sum up shopping cart
		context.user_data[chat_id]["shopping_cart"] = shopping_cart


	def get_used_token(self, chat_id, context):
		return context.user_data[chat_id]["used_token"]
	def set_used_token(self, chat_id, context, used_token):
		context.user_data[chat_id]["used_token"] = used_token
	

	def set_tmp_product(self, chat_id, context, product):
		context.user_data[chat_id]["tmp_product"] = product
	def get_tmp_product(self, chat_id, context):
		return context.user_data[chat_id]["tmp_product"]

	def set_products_keyboard(self, chat_id, context, products_keyboard):
		context.user_data[chat_id]["products_keyboard"] = products_keyboard
	def get_products_keyboard(self, chat_id, context):
		return context.user_data[chat_id]["products_keyboard"]

	


	def better_print_shopping_cart(self,shopping_cart):	# for printing shopping cart
		to_ret = ''
		for item in shopping_cart:
			name, price, unit, quantity = (item['name'], item['price'], item['unit'],item['quantity'])
			to_ret += '• %d × %s (%s): %s€\n' % (quantity, name, unit, price)
		return to_ret

	def make_total(self, shopping_cart):	# total in shopping cart
		to_ret = 0
		for item in shopping_cart:	to_ret += item['price']
		return to_ret



	def make_upper_stop_keyboard(self, alist, parti): 
	   	length = len(alist)
	   	keyboard = []
	   	keyboard.append([self.stop_button])
	   	keyboard =  keyboard + [alist[i*length // parti: (i+1)*length // parti] for i in range(parti)]
	   	return ReplyKeyboardMarkup(keyboard)

	def decrypt_token(self, token):
		token = str(token).encode("utf-8")
		return zlib.decompress(base64.decodebytes(token)).decode("utf-8").replace('\n', '')

if __name__ == '__main__':
	shopping_cart = [{'name': "La Trappe Isid'or", 'price': 15.0, 'unit': '0.33l', 'quantity': 3}, {'name': 'Panna', 'price': 2.0, 'unit': '1.5L', 'quantity': 1}, {'name': 'Krab', 'price': 10.0, 'unit': '0.33l', 'quantity': 1}]

	User_Utils_Obj = User_Utils()
	product_name = "Panna"
	User_Utils_Obj.decrement_quantity(shopping_cart, product_name)



