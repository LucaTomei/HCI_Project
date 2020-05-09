from bot_replies import *
from Dealer_Interaction.src.utils import Utils

class Shop_Window_Handler(object):
	def __init__(self):
		self.Utils_Obj = Utils()

	def test_entry_point_main_handler(self, update, context):
		try:
			## TEST - TO REMOVE
			chat_id = update.message.chat.id
			print("-1: " + update.message.text)
			tmp_category = "alimentari"		# TAKE THEM FROM get_user_categories IN UTILS
			Utility_Obj.set_user_category(chat_id, tmp_category, context)
			tmp_category = "birroteca" 	# TAKE THEM FROM get_user_categories IN UTILS
			Utility_Obj.set_user_category(chat_id, tmp_category, context)
			# END TEST - TO REMOVE
			

			user_categories = Utility_Obj.get_user_categories(chat_id, context)
			keyboard_to_show = self.Utils_Obj.make_keyboard(user_categories, 1)

			Utility_Obj.set_categories_keyboard_by_chat_id(chat_id, context, keyboard_to_show)
			
			update.message.reply_text(bot_replies['choice_your_category'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			
			# Test cancellazione messaggio
			# import time
			# time.sleep(2)
			# Bot_Obj.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
			return 0
		except Exception as e: 	print(str(e))
	
	def choice_your_subcategory_handler(self, update, context):
		try:
			print("0: " + update.message.text)
			chat_id = update.message.chat.id
			chat_message = this_category = update.message.text 		# Category name (eg. alimentari)
			if self.Utils_Obj.is_category_in_file(this_category):
				subcategories_list = self.Utils_Obj.get_subcategories_name_by_category(this_category)
				keyboard_to_show = self.Utils_Obj.make_back_keyboard(subcategories_list, 3)
				Utility_Obj.set_tmp_category(chat_id, chat_message, context)
				Utility_Obj.set_subcategories_keyboard_by_chat_id(chat_id, context, keyboard_to_show)
				update.message.reply_text(bot_replies['choice_your_subcategory'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				return 1
			else:
				print("indietro in choice_your_subcategory_handler")
				keyboard_to_show = Utility_Obj.get_categories_keyboard_by_chat_id(chat_id, context)
				update.message.reply_text(bot_replies['choice_your_category'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				return 0
		except Exception as e: 	print(str(e))


	def choice_your_product_handler(self, update, context):
		try:
			print("\n1: " + update.message.text)
			chat_id = update.message.chat.id
			chat_message = this_subcategory = update.message.text 		# SubCategory name (eg. Cereali)
			
			subcategories_keyboard = Utility_Obj.get_subcategories_keyboard_by_chat_id(chat_id, context)
			if chat_message in [j for i in subcategories_keyboard.keyboard for j in i] and chat_message != bot_buttons['back_button']:
				Utility_Obj.set_tmp_subcategory(chat_id, context, this_subcategory)

				category_name = Utility_Obj.get_tmp_category(chat_id, context)
				products_by_subcategory = self.Utils_Obj.get_subcategory_products(category_name, this_subcategory)

				(product_names, product_units) = self.Utils_Obj.from_subcat_prod_dict_to_list(products_by_subcategory)
				keyboard_to_show = self.Utils_Obj.make_back_keyboard(product_names, 3)
				Utility_Obj.set_products_keyboard_by_chat_id(chat_id, context, keyboard_to_show)
				update.message.reply_text(bot_replies['insert_product'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				return 2
			else:
				print("indietro in choice_your_product_handler")
				keyboard_to_show = subcategories_keyboard
				update.message.reply_text(bot_replies['choice_your_subcategory'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				return 1
		except Exception as e: 	print(str(e))


	def pre_insert_product_price_handler(self, update, context):
		try:
			print("\n2: " + update.message.text)
			chat_id = update.message.chat.id
			chat_message = this_product = update.message.text 		# product name name (eg. Kellogs ...)
			
			products_keyboard = Utility_Obj.get_products_keyboard_by_chat_id(chat_id, context)

			if chat_message in [j for i in products_keyboard.keyboard for j in i]:
				chosen_category = Utility_Obj.get_tmp_category(chat_id, context)
				chosen_subcategory = Utility_Obj.get_tmp_subcategory(chat_id, context)
				products_by_subcategory = self.Utils_Obj.get_subcategory_products(chosen_category, chosen_subcategory)
				tupla = (product_names, product_units) = self.Utils_Obj.from_subcat_prod_dict_to_list(products_by_subcategory)

				this_product_units = self.Utils_Obj.from_product_name_to_units(this_product, tupla)	# eg. 950g if product_name == Nesquik
				
				Utility_Obj.set_tmp_product(chat_id, context, {this_product:this_product_units})	# store this product and its unit

				keyboard_to_show = ReplyKeyboardRemove()
				update.message.reply_text(bot_replies['insert_price'] %(this_product_units, this_product), parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				return 3
			else:
				print("indietro in pre_insert_product_handler")
				keyboard_to_show = products_keyboard
				update.message.reply_text(bot_replies['insert_product'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				return 2
		except Exception as e: 	print(str(e))


	def insert_product_price_handler(self, update, context):
		try:
			print("\n3: " + update.message.text)
			chat_id = update.message.chat.id
			chat_message = update.message.text 		# 1.3 (price)
			
			#verify if is really a formatted price
			if self.Utils_Obj.isDigit(chat_message):
				this_product_price = self.Utils_Obj.truncate_float(chat_message)	# from string to float
				Utility_Obj.set_tmp_product_price(chat_id, context, this_product_price)

				this_product = Utility_Obj.get_tmp_product(chat_id, context)
				this_product_name = list(this_product.keys())[0]	# eg. Kellogs

				keyboard_to_show = yes_no_sure_price
				
				update.message.reply_text(bot_replies['are_you_sure_price'] %(this_product_name, str(this_product_price)), parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				return 4 
			else:	# if is not a price
				products_keyboard = Utility_Obj.get_products_keyboard_by_chat_id(chat_id, context)
				keyboard_to_show = products_keyboard
				update.message.reply_text(bot_replies['insert_product'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				return 2
		except Exception as e: 	print(str(e))

#---------[_yes_no_sure_price_handler]---------
	def loop_in_yes_no_sure_price_handler(self, update, context):
		try:
			print("\n4.1: " + update.message.text)
			chat_id = update.message.chat.id
			chat_message = update.message.text 		# you have insert something different from yes or no sure price

			this_product_price = Utility_Obj.get_tmp_product_price(chat_id, context)
			this_product = Utility_Obj.get_tmp_product(chat_id, context)
			this_product_name = list(this_product.keys())[0]	# eg. Kellogs


			keyboard_to_show = yes_no_sure_price
			update.message.reply_text(bot_replies['are_you_sure_price'] %(this_product_name, str(this_product_price)), parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			return 4 
		except Exception as e: 	print(str(e))

	def yes_insert_other_products_handler(self, update, context):
		try:
			print("\n4.2: " + update.message.text)
			chat_id = update.message.chat.id
			chat_message = update.message.text 		# you have pressed yes

			# if you have pressed yes, store tmp product in shopping window list
			(product_name_and_unit, product_price) = (Utility_Obj.get_tmp_product(chat_id, context),Utility_Obj.get_tmp_product_price(chat_id, context))
			product_name = list(product_name_and_unit.keys())[0]
			product_unit = list(product_name_and_unit.values())[0]
			product_and_price = {"name": product_name, "price": product_price, "unit": product_unit}
			Utility_Obj.append_to_shopping_window_list(chat_id, context, product_and_price)

			keyboard_to_show = other_product_main_keyboard
			update.message.reply_text(bot_replies['shop_window'] %(product_name), parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			print("\tAppena salvato, lista: ",  Utility_Obj.get_shopping_window_list_by_chat_id(chat_id, context))
			return 5
		except Exception as e: 	print(str(e))

	def no_back_to_shopping_window_handler(self, update, context):
		try:
			print("\n4.3: " + update.message.text)
			chat_id = update.message.chat.id
			chat_message = update.message.text 		# you have pressed no

			Utility_Obj.reset_shopping_window(chat_id, context)	# reset all temp products and keyboard
			user_categories = Utility_Obj.get_user_categories(chat_id, context)
			keyboard_to_show = self.Utils_Obj.make_keyboard(user_categories, 1)

			Utility_Obj.set_categories_keyboard_by_chat_id(chat_id, context, keyboard_to_show)
			
			update.message.reply_text(bot_replies['choice_your_category'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			return 0
		except Exception as e: 	print(str(e))


#---------[insert_new_product or end]---------
	def loop_in_shopping_window_go_end_handler(self, update, context):
		try:
			print("\n5.1: " + update.message.text)
			chat_id = update.message.chat.id
			chat_message = update.message.text 		# some text different from (Inserisci nuovo prodotto, Fine - vedi vetrina)
			
			product_name_and_unit = Utility_Obj.get_tmp_product(chat_id, context)
			product_name = list(product_name_and_unit.keys())[0]
			
			keyboard_to_show = other_product_main_keyboard
			update.message.reply_text(bot_replies['shop_window'] %(product_name), parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			return 5
		except Exception as e: 	print(str(e))

	def dont_go_show_shop_window_handler(self, update, context):
		try:
			print("\n5.2: " + update.message.text)
			chat_id = update.message.chat.id
			chat_message = update.message.text 		# Fine - vedi vetrina
		except Exception as e: 	print(str(e))

	def insert_new_products_handler(self, update, context):
		try:
			print("\n5.3: " + update.message.text)
			chat_id = update.message.chat.id
			chat_message = update.message.text 		# Inserisci nuovo prodotto
		except Exception as e: 	print(str(e))




