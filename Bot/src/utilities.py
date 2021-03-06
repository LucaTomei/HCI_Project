import requests, json, geopy, googlemaps, re, pickle, os
from geopy.geocoders import Nominatim


class Utility(object):
	def __init__(self):
		#self.base_request_url = "https://api.colligo.shop/"
		self.base_request_url = "https://boiling-beyond-07880.herokuapp.com/"
		self.colligo_categories_fileName = "files/original_categories.json"
		self.persistence_filename = "bot_persistence"

	def is_really_a_website(self, url):
	    regex = re.compile(
	        r'^https?://'  # http:// or https://
	        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
	        r'localhost|'  # localhost...
	        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
	        r'(?::\d+)?'  # optional port
	        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	    return url is not None and regex.search(url)
	
	#---------[CATEGORIES FUNCTIONS]---------
	def retrieve_merchant_categories_online(self):
		url = self.base_request_url + '/categories'
		response = requests.get(url = url)
		return response.json()

	""" Without connection"""
	def retrieve_merchant_categories(self):
		file = open(self.colligo_categories_fileName)
		content = json.load(file)
		file.close()
		return content
	
	def get_all_merchant_categories(self):
		json_content = self.retrieve_merchant_categories()
		return [item['name'] for item in json_content]

	def from_category_name_to_ids(self, categoriesNamesList):
		toRet = []
		for item in self.retrieve_merchant_categories():
			if item['name'] in categoriesNamesList:	toRet.append(item['id'])
		return list(set(toRet))

	def get_all_categories_ids(self, categoy_list):
		toRet = []
		for item in self.retrieve_merchant_categories():
			if item['name'] in categoy_list:	toRet.append(item['id'])
		return list(set(toRet))
	#---------[END CATEGORIES FUNCTIONS]---------
	

	#---------[CONTEXT_USER_DATA_HANDLERS]---------
	def set_user_data(self, chat_id, context, main_keyboard, group_title):
		if not chat_id in context.user_data:
			context.user_data[chat_id] = {
				"group_title": group_title,
				"telegram_link":'',
				"main_keyboard":main_keyboard, 
				"is_set_location":False, 
				"is_set_categories":False, 
				"categories_list":[],
				"tmp_category":None,
				"user_location":(None, None), 
				"user_website":"",
				"all_done":False,

				#---------[SHOPPING WINDOW]---------
				"categries_keyboard":None,
				"subcategries_keyboard":None,
				"products_keyboard":None,
				"shopping_window_keyboard":None,	# contains all names in shopping window
				"tmp_subcategory":"",
				"tmp_product": {}, 	# to add temp product {"name":"kg"}
				"tmp_price": 0, 	# to add temp product price
				"shopping_window_list": [], 	# shopping_window_list structure: [{'name': 'Nepi', 'price': 10.0, 'units':'1.5L'}, {...}]
				"shopping_window_date": None,	# this will contains the in which that we have stored the shopping window
				"messages_to_delete":[],
			}

	#---------[SHOPPING WINDOW PERSISTENCE]---------
	def get_messages_to_delete(self, chat_id, context):	# list of messages to delete
		return context.user_data[chat_id]['messages_to_delete']
	def append_messages_to_delete(self, chat_id, context, message_id):
		context.user_data[chat_id]['messages_to_delete'].append(message_id)
	def reset_messages_to_delete(self, chat_id, context):
		context.user_data[chat_id]['messages_to_delete'] = []


	def format_datetime(self, datetime_obj):
		return datetime_obj.strftime("%d/%m/%YCOLLIGO%H:%M")
	
	def get_group_title(self, chat_id, context):
		return context.user_data[chat_id]['group_title']
	
	def prepare_persistence(self, chat_id, context):
		dealer_infos = {
			"group_title": self.get_group_title(chat_id, context),
			"shop_location": self.get_user_location(chat_id, context),
			"categories_list": self.get_user_categories(chat_id, context),
			"shopping_window_list": self.get_shopping_window_list_by_chat_id(chat_id, context),
			"shopping_window_date": self.format_datetime(self.get_shopping_window_date(chat_id, context))
		}
		return dealer_infos


	#---------[SHOPPING WINDOW]---------
	def reset_shopping_window(self, chat_id, context):
		context.user_data[chat_id]['categries_keyboard'] = None
		context.user_data[chat_id]['subcategries_keyboard'] = None
		context.user_data[chat_id]['products_keyboard'] = None
		context.user_data[chat_id]['tmp_subcategory'] = ""
		context.user_data[chat_id]['tmp_product'] = {}
		context.user_data[chat_id]['tmp_price'] = 0

	def get_shopping_window_keyboard(self, chat_id, context):
		return context.user_data[chat_id]['shopping_window_keyboard']
	def set_shopping_window_keyboard(self, chat_id, context, shopping_window_keyboard): 
		context.user_data[chat_id]['shopping_window_keyboard'] = shopping_window_keyboard

	def get_shopping_window_date(self, chat_id, context):
		return context.user_data[chat_id]['shopping_window_date']
	def set_shopping_window_date(self, chat_id, context, shopping_window_date): #shopping_window_date is a datetime object
		context.user_data[chat_id]['shopping_window_date'] = shopping_window_date



	def get_categories_keyboard_by_chat_id(self, chat_id, context):
		return context.user_data[chat_id]['categries_keyboard']
	def set_categories_keyboard_by_chat_id(self, chat_id, context, categries_keyboard):
		context.user_data[chat_id]['categries_keyboard'] = categries_keyboard

	def get_subcategories_keyboard_by_chat_id(self, chat_id, context):
		return context.user_data[chat_id]['subcategries_keyboard']
	def set_subcategories_keyboard_by_chat_id(self, chat_id, context, subcategries_keyboard):
		context.user_data[chat_id]['subcategries_keyboard'] = subcategries_keyboard

	def get_products_keyboard_by_chat_id(self, chat_id, context):
		return context.user_data[chat_id]['products_keyboard']
	def set_products_keyboard_by_chat_id(self, chat_id, context, products_keyboard):
		context.user_data[chat_id]['products_keyboard'] = products_keyboard

	

	def get_tmp_subcategory(self, chat_id, context):
		return context.user_data[chat_id]['tmp_subcategory']
	
	def set_tmp_subcategory(self, chat_id, context, subcategory):
		context.user_data[chat_id]['tmp_subcategory'] = subcategory 


	def get_tmp_product(self, chat_id, context):
		return context.user_data[chat_id]['tmp_product']
	
	def set_tmp_product(self, chat_id, context, product):
		context.user_data[chat_id]['tmp_product'] = product

	def get_tmp_product_price(self, chat_id, context):
		return context.user_data[chat_id]['tmp_price']
	
	def set_tmp_product_price(self, chat_id, context, price):
		context.user_data[chat_id]['tmp_price'] = price


	def get_shopping_window_list_by_chat_id(self, chat_id, context):
		return context.user_data[chat_id]['shopping_window_list']
	def set_shopping_window_list_by_chat_id(self, chat_id, context, shopping_window_list):
		context.user_data[chat_id]['shopping_window_list'] = shopping_window_list


	def format_shopping_window(self, a_list):	#a_list = [{'name': 'Amstel', 'price': 12.0, 'unit': '0.33l'}, ...]
		to_ret = ''
		for dictionary in a_list:
			(name, price, unit) = (dictionary['name'], dictionary['price'], dictionary['unit'])
			to_ret += '• %s %s: %s€\n' %(unit, name.capitalize(), str(price))
		return to_ret
	def get_all_shopping_window_names(self, a_list):
		to_ret = []
		for dictionary in a_list:	to_ret.append(dictionary['name'])
		return to_ret
	
	def append_to_shopping_window_list(self, chat_id, context, product_and_price):	# product_price =  [{'name': 'Nepi', 'price': 10.0, 'units':'1.5L'}, {...}]
		if product_and_price not in context.user_data[chat_id]['shopping_window_list']: context.user_data[chat_id]['shopping_window_list'].append(product_and_price)
	
	def manually_set_shopping_window(self, chat_id, context, shopping_window_list):
		context.user_data[chat_id]['shopping_window_list'] = shopping_window_list

	#---------[END SHOPPING WINDOW]---------
	


	def get_user_data(self, chat_id, context):
		return context.user_data[chat_id]

	def get_main_keyboard_by_chat_id(self, chat_id, context):
		return context.user_data[chat_id]['main_keyboard']
	def set_main_keyboard_by_chat_id(self, chat_id, main_keyboard, context):
		context.user_data[chat_id]['main_keyboard'] = main_keyboard

	def get_user_categories(self, chat_id, context):
		return list(set(context.user_data[chat_id]['categories_list']))
	
	def set_user_category(self, chat_id, category, context):
		context.user_data[chat_id]['categories_list'].append(category)

	def get_tmp_category(self, chat_id, context):
		return context.user_data[chat_id]['tmp_category']
	
	def set_tmp_category(self, chat_id, category, context):
		context.user_data[chat_id]['tmp_category'] = category

	def get_telegram_link(self, context, chat_id):
		try:
			return context.user_data[chat_id]['telegram_link']
		except:	return ''

	def set_telegram_link(self, update, context):
		chat_id = update.message.chat.id
		telegram_link = ''
		if self.get_telegram_link(context, chat_id) == '':
			try:	telegram_link = context.user_data[chat_id]['telegram_link'] = context.bot.exportChatInviteLink(chat_id)
			except Exception as e:	pass
		return telegram_link



	def set_user_website(self, chat_id, website, context):
		context.user_data[chat_id]['user_website'] = website
	def get_user_website(self, chat_id, context):
		return context.user_data[chat_id]['user_website']


	def get_user_location(self, chat_id, context):	return context.user_data[chat_id]['user_location']
	def set_user_location(self, chat_id, tupla_location, context):
		context.user_data[chat_id]['user_location'] = tupla_location

	def set_location_done(self, chat_id, context):
		context.user_data[chat_id]['is_set_location'] = True
	def has_done_location(self, chat_id, context):	return context.user_data[chat_id]['is_set_location']


	def set_categories_done(self, chat_id, context):
		context.user_data[chat_id]['is_set_categories'] = True
	def has_done_categories(self, chat_id, context):	return context.user_data[chat_id]['is_set_categories']

	def remove_user_in_context(self, chat_id, context):
		del context.user_data[chat_id]


	def check_if_user_has_done(self, chat_id, context):
		try:
			return context.user_data[chat_id]['all_done']
		except:return False

	def set_all_done(self, chat_id, context):
		context.user_data[chat_id]['all_done'] = True
	#---------[END CONTEXT_USER_DATA_HANDLERS]---------
	

	#---------[SAVING DATA TO BACKAND]---------
	
	def reverse_location(self, latitude, longitude):
		try:
			api_key = 'AIzaSyANBKTnUtFUgYga3F-gzM6qwdNFaUul8Gg'
			geolocator = Nominatim(user_agent='ColliGoBot')
			gmaps = googlemaps.Client(key=api_key)
			reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude)) #("22.5757344, 88.4048656")
			location = geolocator.reverse(str(latitude) + ',' + str(longitude))
			raw_location = location.raw['address']


			formatted_address = reverse_geocode_result[0]['formatted_address']
			tupla_location = (address, num_address, cap_and_city, country)  = formatted_address.split(',')
			address = address + " " + str(num_address)
			#print(tupla_location)
			cap = raw_location['postcode']
			#print(cap)
			
			try:	city = raw_location['town'].capitalize() if 'town' in raw_location else raw_location['village'].capitalize()
			except:	cyty = cap_and_city.split(' ')[1]

			return city, address, cap
		except:	return None, None, None

	# def post_shop_details(self, chat_id, context):
	# 	context_to_set = context
	# 	context = context.user_data[chat_id]
	# 	try:
	# 		latitude, longitude = context['user_location']
	# 		#print(latitude, longitude)
	# 		(city, address, cap) = self.reverse_location(latitude, longitude)
	# 	except:
	# 		address, cap, city = context['user_location']

	# 	to_post = {
	# 			'name':context['group_title'],
	# 			"city":city ,
	# 			"address": address, 
	# 			"cap":cap,
	# 			"description":context['group_title'], 
	# 			"telegram":context['telegram_link'] if context['telegram_link'] != '' else 'https://'+context['group_title'],
	# 			'categories_ids': self.from_category_name_to_ids(context['categories_list']), 
	# 			"accepts_terms_and_conditions":True
	# 		}
		
	# 	website = context['user_website']	# if you have a website
	# 	if website != '':	to_post.update({'website':website})
		
	# 	#print("to_post", to_post)
	# 	post_url = self.base_request_url + '/shops' #"http://localhost:5000/shops" for test
	# 	response = requests.post(url = post_url, json = to_post)
	# 	#print(response.status_code, response.text)
	# 	self.set_all_done(chat_id, context_to_set)
	# 	return response.status_code

	def post_shop_details(self, chat_id, context):
		pass

	#---------[END SAVING DATA TO BACKAND]---------
	
	def reset_user_in_pickle(self, chat_id, context):	# not used
		if os.path.exists(self.persistence_filename):
			file = open(self.persistence_filename, 'rb')
			content = pickle.load(file)
			file.close()
			for keys in content:
				if keys == 'conversations':
					for item in content[keys]:
						tmp = content[keys][item]
						new_dict = {}
						for i in tmp:
							value = tmp[i]
							i = list(i)
							if int(chat_id) in i:
								i.remove(int(chat_id))
							i = tuple(i)
							new_dict.update({i:value})
						content[keys][item] = new_dict
			
			if chat_id in content['user_data'] and chat_id in content['user_data'][chat_id]:
				content['user_data'][chat_id][chat_id]['used_token'] = ""
			
			content['user_data'][chat_id] = {}
			file.close()
			
			file = open(self.persistence_filename, 'wb')
			pickle.dump(content, file)
			file.close()
			


if __name__ == '__main__':
	Utility_Obj = Utility()
	# x = Utility_Obj.retrieve_merchant_categories()	
	# print(x)
	chat_id = 303679205
	context = {}
	x = Utility_Obj.reset_user_in_pickle(chat_id, context)



