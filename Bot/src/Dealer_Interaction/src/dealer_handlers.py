from bot_replies import *
from . import shop_window_handler

class Dealer_Handlers(object):
	def __init__(self):
		self.Shop_Window_Handler_Obj = shop_window_handler.Shop_Window_Handler()

	#---------[You have pressed YES WEBSITE BUTTON]---------
	def you_have_website(self, update, context):
		Utility_Obj.set_telegram_link(update, context)
		update.message.reply_text(bot_replies['insert_website'], parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove(), disable_web_page_preview=True)
		return 1
	
	#---------[You have pressed NO WEBSITE BUTTON]---------
	def yout_dont_have_website(self, update, context):	# if you don't have website return 2
		Utility_Obj.set_telegram_link(update, context)
		update.message.reply_text(bot_replies['description_message'], parse_mode=ParseMode.MARKDOWN, reply_markup=main_keyboard, disable_web_page_preview=True)
		return ConversationHandler.END

	def register_website_handler(self, update, context):
		Utility_Obj.set_telegram_link(update, context)
		chat_id = update.message.chat_id
		website = update.message.text
		if website.lower() != 'q': 
			if Utility_Obj.is_really_a_website(website):
				Utility_Obj.set_user_website(chat_id, website, context)	# Save user website in user_data
				update.message.reply_text(bot_replies['website_added'] % (website), parse_mode=ParseMode.MARKDOWN, reply_markup=main_keyboard, disable_web_page_preview=True)
				update.message.reply_text(bot_replies['description_message'], parse_mode=ParseMode.MARKDOWN, reply_markup=main_keyboard, disable_web_page_preview=True)
				return ConversationHandler.END
			else:
				update.message.reply_text(bot_replies['website_error'] % website, parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove(), disable_web_page_preview=True)
				return 1	# loop until you add a valid website
		else:
			update.message.reply_text(bot_replies['website_not_insert'], parse_mode=ParseMode.MARKDOWN, reply_markup=main_keyboard, disable_web_page_preview=True)
			return ConversationHandler.END



	def category_main_handler(self, update, context):
		Utility_Obj.set_telegram_link(update, context)
		user_categories = Utility_Obj.get_user_categories(update.message.chat.id, context)
		#print("[category_main_handler] categorie utente: ", user_categories)
		update.message.reply_text(bot_replies['category_message'], parse_mode=ParseMode.MARKDOWN, reply_markup=categories_keyboard, disable_web_page_preview=True)
		return 0

	def filter_categories_handler(self, update, context):
		Utility_Obj.set_telegram_link(update, context)
		chat_message = update.message.text
		chat_id = update.message.chat_id
		user_categories = Utility_Obj.get_user_categories(chat_id, context)
		if len(user_categories) != 3:
			if chat_message in [j for i in categories_keyboard.keyboard for j in i]:
				Utility_Obj.set_tmp_category(update.message.chat_id, update.message.text, context)
				update.message.reply_text(bot_replies['category_yes_no'] % update.message.text, parse_mode=ParseMode.MARKDOWN, reply_markup=yes_no_categories_keyboard, disable_web_page_preview=True)
				return 1
			else:
				update.message.reply_text(bot_replies['category_error_message'], parse_mode=ParseMode.MARKDOWN, reply_markup=categories_keyboard, disable_web_page_preview=True)
				return 0
		else:
			if Utility_Obj.has_done_location(chat_id, context):
				Utility_Obj.set_main_keyboard_by_chat_id(chat_id, main_keyboard_empty, context)
				tupla_location = Utility_Obj.get_user_location(chat_id, context)
				message_to_send = bot_replies['all_done'] % (str(user_categories), str(tupla_location))
				Utility_Obj.post_shop_details(chat_id, context)
			else:
				Utility_Obj.set_main_keyboard_by_chat_id(chat_id, main_keyboard_only_location, context)
				message_to_send = bot_replies['catagories_done'] % (str(user_categories))
			main_keyboard = Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context)
			update.message.reply_text(message_to_send, parse_mode=ParseMode.MARKDOWN, reply_markup=main_keyboard, disable_web_page_preview=True)
			return ConversationHandler.END


	def add_category_handler(self, update, context):
		Utility_Obj.set_telegram_link(update, context)
		chat_id = update.message.chat_id
		category = Utility_Obj.get_tmp_category(update.message.chat_id, context)
		Utility_Obj.set_user_category(chat_id, category, context)
		user_categories = Utility_Obj.get_user_categories(update.message.chat.id, context)
		if len(user_categories) != 3:
			update.message.reply_text(bot_replies['catagory_added'] % category, parse_mode=ParseMode.MARKDOWN, reply_markup=categories_keyboard, disable_web_page_preview=True)
			return 0
		else:
			Utility_Obj.set_categories_done(chat_id, context)
			if not Utility_Obj.has_done_location(chat_id, context):
				Utility_Obj.set_main_keyboard_by_chat_id(chat_id, main_keyboard_only_location, context)
				
				message_to_send = bot_replies['catagories_done'] % (str(user_categories))
			else:
				Utility_Obj.set_main_keyboard_by_chat_id(chat_id, main_keyboard_empty, context)
				tupla_location = Utility_Obj.get_user_location(chat_id, context)
				message_to_send = bot_replies['all_done'] % (str(user_categories), str(tupla_location))
				Utility_Obj.post_shop_details(chat_id, context)
			main_keyboard = Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context)
			update.message.reply_text(message_to_send, parse_mode=ParseMode.MARKDOWN, reply_markup=main_keyboard, disable_web_page_preview=True)
			return ConversationHandler.END


	def check_user_categories_handler(self, update, context):
		chat_id = update.message.chat_id
		user_categories = Utility_Obj.get_user_categories(chat_id, context)
		try:
			Utility_Obj.set_telegram_link(update, context)
			chat_id = update.message.chat_id
			user_categories = Utility_Obj.get_user_categories(chat_id, context)
			if len(user_categories) != 0:
				if Utility_Obj.has_done_location(chat_id, context):
					Utility_Obj.set_main_keyboard_by_chat_id(chat_id, main_keyboard_empty, context)
				else:
					Utility_Obj.set_main_keyboard_by_chat_id(chat_id, main_keyboard_only_location, context)
				main_keyboard = Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context)
				Utility_Obj.set_categories_done(chat_id, context)
				update.message.reply_text(bot_replies['catagories_done'] % str(user_categories), parse_mode=ParseMode.MARKDOWN, reply_markup=main_keyboard, disable_web_page_preview=True)
				if Utility_Obj.has_done_location(chat_id, context):
					user_location = Utility_Obj.get_user_location(chat_id, context)
					update.message.reply_text(bot_replies['all_done'] % (str(user_categories), str(user_location)), parse_mode=ParseMode.MARKDOWN, reply_markup=main_keyboard, disable_web_page_preview=True)
					Utility_Obj.post_shop_details(chat_id, context)
				return ConversationHandler.END
			else:
				update.message.reply_text(bot_replies['category_error_message'], parse_mode=ParseMode.MARKDOWN, reply_markup=categories_keyboard, disable_web_page_preview=True)
				return 0
		except Exception as e:	print(str(e))

	def location_main_handler(self, update, context):
		Utility_Obj.set_telegram_link(update, context)
		update.message.reply_text(bot_replies['position_message'], parse_mode=ParseMode.MARKDOWN, reply_markup = ReplyKeyboardRemove(), disable_web_page_preview=True)
		return 2


	def set_user_location_handler(self, update, context):
		try:
			Utility_Obj.set_telegram_link(update, context)
			chat_id = update.message.chat_id
			location = update.message.location
			tupla_location = (latitude, longitude) = (location.latitude, location.longitude)
			city, address, cap = Utility_Obj.reverse_location(*tupla_location)
			if city != None and address != None and cap != None:
				Utility_Obj.set_user_location(chat_id, tupla_location, context)
				Utility_Obj.set_location_done(chat_id, context)
				if Utility_Obj.has_done_categories(chat_id, context):
					Utility_Obj.set_main_keyboard_by_chat_id(chat_id, main_keyboard_empty, context)
					user_categories = Utility_Obj.get_user_categories(chat_id, context)

					message_to_send = bot_replies['all_done'] % (str(user_categories), str(tupla_location))
					Utility_Obj.post_shop_details(chat_id, context)
				else:
					Utility_Obj.set_main_keyboard_by_chat_id(chat_id, main_keyboard_only_categories, context)
					message_to_send = bot_replies['location_done'] % (address + " ("+ cap +")", city)
				main_keyboard = Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context)
				update.message.reply_text(message_to_send, parse_mode=ParseMode.MARKDOWN, reply_markup = main_keyboard, disable_web_page_preview=True)
				return ConversationHandler.END
			else:
				update.message.reply_text(bot_replies['location_error_message'], parse_mode=ParseMode.MARKDOWN, reply_markup = ReplyKeyboardRemove(), disable_web_page_preview=True)
				return 3
		except Exception as e:	print(str(e))

	def manual_location_insertion_handler(self, update, context):
		Utility_Obj.set_telegram_link(update, context)
		chat_message = update.message.text
		chat_id = update.message.chat.id
		try:
			tupla_location = address, cap, city = chat_message.split(',')
			Utility_Obj.set_user_location(chat_id, tupla_location, context)
			Utility_Obj.set_location_done(chat_id, context)
			if Utility_Obj.has_done_categories(chat_id, context):
				Utility_Obj.set_main_keyboard_by_chat_id(chat_id, main_keyboard_empty, context)
				user_categories = Utility_Obj.get_user_categories(chat_id, context)

				message_to_send = bot_replies['all_done'] % (str(user_categories), str(tupla_location))
				Utility_Obj.post_shop_details(chat_id, context)
			else:
				Utility_Obj.set_main_keyboard_by_chat_id(chat_id, main_keyboard_only_categories, context)
				message_to_send = bot_replies['location_done'] % (address + " ("+ cap +")", city)
			main_keyboard = Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context)
			update.message.reply_text(message_to_send, parse_mode=ParseMode.MARKDOWN, reply_markup = main_keyboard, disable_web_page_preview=True)
			return ConversationHandler.END
		except:	# cannot retrieve tupla_location text
			update.message.reply_text(bot_replies['location_error_message'], parse_mode=ParseMode.MARKDOWN, reply_markup = ReplyKeyboardRemove(), disable_web_page_preview=True)
			return 3

	def register_shop_handler(self):
		register_shop_handler = ConversationHandler(
            [	# Entry Points
            	MessageHandler(Filters.regex('^' + bot_buttons['category'] +'$'),self.category_main_handler),
            	MessageHandler(Filters.regex('^' + bot_buttons['location'] +'$'),self.location_main_handler),
        		MessageHandler(Filters.text,unknown_function),
        		MessageHandler(Filters.location,self.set_user_location_handler),
            ], 
            {
            	0: [	# Starting main handler
            		MessageHandler(Filters.regex('^' + bot_buttons['stop_button'] +'$'), self.check_user_categories_handler),
            		MessageHandler(Filters.text, self.filter_categories_handler),
            	],
            	1: [	# category_yes_no
            		MessageHandler(Filters.regex('^' + bot_buttons['yes_category'] +'$'),self.add_category_handler),
            		MessageHandler(Filters.regex('^' + bot_buttons['no_category'] +'$'),self.category_main_handler),
            		MessageHandler(Filters.text, self.filter_categories_handler),
            	],
            	2:[		# Location
            		MessageHandler(Filters.text,unknown_function),
            		MessageHandler(Filters.location,self.set_user_location_handler),
            	],
            	3: [# error on location - manual insertion
            		MessageHandler(Filters.text,self.manual_location_insertion_handler),
            		MessageHandler(Filters.location,self.set_user_location_handler),
            	]  	
            },[])
		return register_shop_handler

	
	def register_shop_handler_test(self):
		register_shop_handler = ConversationHandler(
            [	# Entry Points
            	MessageHandler(Filters.regex('^' + bot_buttons['category'] +'$'),self.Shop_Window_Handler_Obj.test_entry_point_main_handler),
            	MessageHandler(Filters.regex('^' + bot_buttons['location'] +'$'),self.Shop_Window_Handler_Obj.test_entry_point_main_handler),
        		MessageHandler(Filters.text,unknown_function),
            ], 
            {
            	0: [ # Choice sub category
            		MessageHandler(Filters.text, self.Shop_Window_Handler_Obj.choice_your_subcategory_handler),
            	],
            	1: [ # Choice Product
            		MessageHandler(Filters.regex('^' + bot_buttons['back_button'] +'$'),self.Shop_Window_Handler_Obj.choice_your_subcategory_handler),
            		MessageHandler(Filters.text, self.Shop_Window_Handler_Obj.choice_your_product_handler),
            	],
            	2: [
            		MessageHandler(Filters.regex('^' + bot_buttons['back_button'] +'$'),self.Shop_Window_Handler_Obj.choice_your_product_handler),
            		MessageHandler(Filters.text, self.Shop_Window_Handler_Obj.pre_insert_product_price_handler),
            	],
            	3: [	# insert product price
            		MessageHandler(Filters.text, self.Shop_Window_Handler_Obj.insert_product_price_handler),
            	],
            	4: [	# yes no insert product price
            		MessageHandler(Filters.regex('^' + bot_buttons['no_sure_price'] +'$'),self.Shop_Window_Handler_Obj.no_back_to_shopping_window_handler),
            		MessageHandler(Filters.regex('^' + bot_buttons['yes_sure_price'] +'$'),self.Shop_Window_Handler_Obj.yes_insert_other_products_handler),
            		MessageHandler(Filters.text, self.Shop_Window_Handler_Obj.loop_in_yes_no_sure_price_handler),
            	],
            	5:[
            		MessageHandler(Filters.regex('^' + bot_buttons['no_show_shop_window'] +'$'),self.Shop_Window_Handler_Obj.show_shopping_window_handler),
            		MessageHandler(Filters.regex('^' + bot_buttons['yes_insert_new_product'] +'$'),self.Shop_Window_Handler_Obj.insert_new_products_handler),
            		MessageHandler(Filters.text, self.Shop_Window_Handler_Obj.loop_in_shopping_window_go_end_handler),
            	],
            	6:[
            		MessageHandler(Filters.regex('^' + bot_buttons['no_send_shop_window'] +'$'),self.Shop_Window_Handler_Obj.dont_send_shopping_window_handler),
            		MessageHandler(Filters.regex('^' + bot_buttons['yes_send_shop_window'] +'$'),self.Shop_Window_Handler_Obj.yes_send_shopping_window_handler),
            		MessageHandler(Filters.text, self.Shop_Window_Handler_Obj.loop_in_end_shopping_window_handler),
            	],
            	7:[
            		MessageHandler(Filters.regex('^' + bot_buttons['back_button'] +'$'),self.Shop_Window_Handler_Obj.loop_in_end_shopping_window_handler),
            		MessageHandler(Filters.text, self.Shop_Window_Handler_Obj.edit_your_products_main_handler),
            	],
            	8:[
            		MessageHandler(Filters.regex('^' + bot_buttons['edit_product_price'] +'$'),self.Shop_Window_Handler_Obj.edit_this_product_handler),
            		MessageHandler(Filters.regex('^' + bot_buttons['delete_product'] +'$'),self.Shop_Window_Handler_Obj.delete_product_handler),
            		MessageHandler(Filters.text, self.Shop_Window_Handler_Obj.edit_your_products_main_handler),
            	],
            	9:[	# delete product
            		MessageHandler(Filters.regex('^' + bot_buttons['sure_delete_product'] +'$'),self.Shop_Window_Handler_Obj.delete_product_done_handler),
            		MessageHandler(Filters.regex('^' + bot_buttons['not_sure_delete_product'] +'$'),self.Shop_Window_Handler_Obj.dont_delete_product_handler),
            		MessageHandler(Filters.text, self.Shop_Window_Handler_Obj.back_to_are_you_sure_delete_product_handler),
            	],
            	10:[	# edit product price
            		MessageHandler(Filters.text, self.Shop_Window_Handler_Obj.set_new_product_price_handler),
            	],
            	11: [	# Set editedp product price
            		MessageHandler(Filters.regex('^' + bot_buttons['yes_edit_price'] +'$'),self.Shop_Window_Handler_Obj.edit_product_price_done_handler),
            		MessageHandler(Filters.regex('^' + bot_buttons['not_sure_delete_product'] +'$'),self.Shop_Window_Handler_Obj.dont_edit_price_handler),
            	]
            },[])
		return register_shop_handler



	














	def preamble_register_shop_handler(self):
		preamble_register_shop_handler = ConversationHandler(
            [	# Entry Points
            	MessageHandler(Filters.regex('^' + bot_buttons['yes'] +'$'),self.you_have_website),
            	MessageHandler(Filters.regex('^' + bot_buttons['no'] +'$'),self.yout_dont_have_website),
            ], 
            {
            	0:[	
            		MessageHandler(Filters.text,unknown_function),
            	],
            	1:[	# state for register website
            		MessageHandler(Filters.text,self.register_website_handler)
            	]   	
            },[])
		return preamble_register_shop_handler

