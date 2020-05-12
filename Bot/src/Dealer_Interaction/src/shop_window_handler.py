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
				keyboard_to_show = self.Utils_Obj.make_upper_back_keyboard(product_names, 3)
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

			# Utility_Obj.reset_shopping_window(chat_id, context)	# reset all temp products and keyboard
			# user_categories = Utility_Obj.get_user_categories(chat_id, context)
			# keyboard_to_show = self.Utils_Obj.make_keyboard(user_categories, 1)

			# Utility_Obj.set_categories_keyboard_by_chat_id(chat_id, context, keyboard_to_show)
			keyboard_to_show = Utility_Obj.get_products_keyboard_by_chat_id(chat_id, context)
			
			update.message.reply_text(bot_replies['choice_your_category'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			return 2
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

	def show_shopping_window_handler(self, update, context):
		try:
			print("\n5.2: " + update.message.text)
			chat_id = update.message.chat.id
			chat_message = update.message.text 		# Fine - vedi vetrina
			
			shopping_window = Utility_Obj.get_shopping_window_list_by_chat_id(chat_id, context)
			formatted_shopping_window = Utility_Obj.format_shopping_window(shopping_window)	# this is a string and not a list
			
			keyboard_to_show = send_shop_window_keyboard
			update.message.reply_text(bot_replies['shop_window_done'] %(formatted_shopping_window), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
			update.message.reply_text(bot_replies['want_to_send'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			return 6
		except Exception as e: 	print(str(e))

	def insert_new_products_handler(self, update, context):
		try:
			print("\n5.3: " + update.message.text)	# Inserisci nuovo prodotto
			return self.no_back_to_shopping_window_handler(update, context)
		except Exception as e: 	print(str(e))



#---------[Send Shopping window]---------
	def loop_in_end_shopping_window_handler(self, update, context):
		try:
			print("\n6.1: " + update.message.text)# some text different from ("SI - Invia ai clienti" or "NO - Modifica Prodotti")
			return self.show_shopping_window_handler(update, context)
		except Exception as e: 	print(str(e))

	def yes_send_shopping_window_handler(self, update, context):
		try:
			print("\n6.2: " + update.message.text)
			chat_id = update.message.chat.id
			chat_message = update.message.text 		# "SI - Invia ai clienti"
			
			keyboard_to_show = ReplyKeyboardRemove()

			user_token = self.Utils_Obj.make_token(chat_id)

			update.message.reply_text(bot_replies['shop_window_send'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			update.message.reply_text(bot_replies['shop_window_send_token'] %(user_token), parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			update.message.reply_text(bot_replies['shop_window_send_done'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)

			Utility_Obj.set_main_keyboard_by_chat_id(chat_id, keyboard_to_show, context)
			Utility_Obj.set_shopping_window_date(chat_id, context, datetime.now())
			return ConversationHandler.END
		except Exception as e: 	print(str(e))

	def dont_send_shopping_window_handler(self, update, context):
		try:
			print("\n6.3: " + update.message.text)
			chat_id = update.message.chat.id
			chat_message = update.message.text 		# "NO - Modifica Prodotti"

			shopping_window = Utility_Obj.get_shopping_window_list_by_chat_id(chat_id, context)
			shopping_window_names_list = Utility_Obj.get_all_shopping_window_names(shopping_window)

			keyboard_to_show = self.Utils_Obj.make_upper_back_keyboard(shopping_window_names_list, 3)
			Utility_Obj.set_shopping_window_keyboard(chat_id, context, keyboard_to_show)	# store shopping_window keyboard products 
			
			update.message.reply_text(bot_replies['edit_shopping_window'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)

			return 7
		except Exception as e: 	print(str(e))

#---------[Edit or delete product]---------
	def edit_your_products_main_handler(self, update, context):
		try:
			print("\n7: " + update.message.text)
			chat_id = update.message.chat.id
			chat_message = update.message.text 		# all type of text

			shopping_window_products_keyboard = Utility_Obj.get_shopping_window_keyboard(chat_id, context)
			if chat_message in [j for i in shopping_window_products_keyboard.keyboard for j in i]:
				keyboard_to_show = delete_edit_keyboard
				shopping_window = Utility_Obj.get_shopping_window_list_by_chat_id(chat_id, context)
				this_product = self.Utils_Obj.get_product_infos(shopping_window, chat_message)
				Utility_Obj.set_tmp_product(chat_id, context, this_product)
				update.message.reply_text(bot_replies['edit_action'] % chat_message, parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				return 8
			else:
				return self.dont_send_shopping_window_handler(update, context)	# go back
		except Exception as e: 	print(str(e))

	def edit_this_product_handler(self, update, context):
		try:
			print("\n8.1: " + update.message.text)
			chat_id = update.message.chat.id
			chat_message = update.message.text 		#	"Modificare il Prezzo"

			shopping_window = Utility_Obj.get_shopping_window_list_by_chat_id(chat_id, context)
			tmp_product  = Utility_Obj.get_tmp_product(chat_id, context)	#	 {'name': 'Blanche de Namur', 'price': 1.0, 'unit': '0.33l'}
			
			keyboard_to_show = ReplyKeyboardRemove()
			update.message.reply_text(bot_replies['edit_product_price'] % (tmp_product['unit'], tmp_product['name']), parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			return 10
		except Exception as e: 	print(str(e))


	def delete_product_handler(self, update, context):
		try:
			print("\n8.2: " + update.message.text)
			chat_id = update.message.chat.id
			chat_message = update.message.text 		#	"Eliminare il Prodotto",

			tmp_product  = Utility_Obj.get_tmp_product(chat_id, context)	#  {'name': 'Blanche de Namur', 'price': 1.0, 'unit': '0.33l'}
			tmp_product_name = tmp_product['name']
			keyboard_to_show = delete_product_sure_keyboard
			update.message.reply_text(bot_replies['sure_delete_product'] % tmp_product_name, parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			return 9
		except Exception as e: 	print(str(e))



	def delete_product_done_handler(self, update, context):
		try:
			print("\n9.1: " + update.message.text)
			chat_id = update.message.chat.id
			chat_message = update.message.text

			tmp_product  = Utility_Obj.get_tmp_product(chat_id, context)
			shopping_window = Utility_Obj.get_shopping_window_list_by_chat_id(chat_id, context)
			shopping_window = self.Utils_Obj.tmp_remove_product_from_shopping_window(shopping_window, tmp_product['name'])
			Utility_Obj.manually_set_shopping_window(chat_id, context, shopping_window)
			
			update.message.reply_text(bot_replies['deletion_done'] % tmp_product['name'], parse_mode=ParseMode.MARKDOWN, reply_markup = ReplyKeyboardRemove(), disable_web_page_preview=True)
			
			return self.show_shopping_window_handler(update, context)

		except Exception as e: 	print(str(e))

	def dont_delete_product_handler(self, update, context):
		try:
			print("\n9.2: " + update.message.text)
			chat_id = update.message.chat.id
			chat_message = update.message.text

			shopping_window = Utility_Obj.get_shopping_window_list_by_chat_id(chat_id, context)
			shopping_window_names_list = Utility_Obj.get_all_shopping_window_names(shopping_window)

			keyboard_to_show = self.Utils_Obj.make_upper_back_keyboard(shopping_window_names_list, 3)
			Utility_Obj.set_shopping_window_keyboard(chat_id, context, keyboard_to_show)	# store shopping_window keyboard products 
			
			update.message.reply_text(bot_replies['edit_shopping_window'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)

			return 7
		except Exception as e: 	print(str(e))

	def back_to_are_you_sure_delete_product_handler(self, update, context):
		try:
			print("\n9.3: " + update.message.text)
			return self.delete_product_handler(update, context)	# some text (different from "Si elimina proddotto" and ...)
		except Exception as e: 	print(str(e))




	def set_new_product_price_handler(self, update, context):
		try:
			print("\n10: " + update.message.text)	# some text, I hope it's a price
			chat_id = update.message.chat.id
			chat_message = update.message.text
			if self.Utils_Obj.isDigit(chat_message):
				new_price = chat_message
				tmp_product  = Utility_Obj.get_tmp_product(chat_id, context)
				shopping_window = Utility_Obj.get_shopping_window_list_by_chat_id(chat_id, context)
				Utility_Obj.set_tmp_product_price(chat_id, context, new_price)
				#shopping_window = self.Utils_Obj.edit_shopping_window_price(self, shopping_window, tmp_product['name'], new_price)
				keyboard_to_show = edit_product_price_keyboard
				update.message.reply_text(bot_replies['sure_edit_price'] % (tmp_product['name'],new_price), parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				return 11
			else:
				return self.edit_this_product_handler(update, context) 
		except Exception as e: 	print(str(e))



	def edit_product_price_done_handler(self, update, context):
		try:
			print("\n11.1: " + update.message.text)	# some text, I hope it's a price
			chat_id = update.message.chat.id
			chat_message = update.message.text

			tmp_product  = Utility_Obj.get_tmp_product(chat_id, context)
			tmp_product_price = Utility_Obj.get_tmp_product_price(chat_id, context)
			shopping_window = Utility_Obj.get_shopping_window_list_by_chat_id(chat_id, context)
			shopping_window = self.Utils_Obj.edit_shopping_window_price(shopping_window, tmp_product['name'], tmp_product_price)
			Utility_Obj.manually_set_shopping_window(chat_id, context, shopping_window)
			shopping_window = Utility_Obj.get_shopping_window_list_by_chat_id(chat_id, context)
			
			keyboard_to_show = ReplyKeyboardRemove()
			update.message.reply_text(bot_replies['edit_product_price_done'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)

			return self.show_shopping_window_handler(update, context)
		except Exception as e: 	print(str(e))

	def dont_edit_price_handler(self, update, context):
		try:
			print("\n11.2: " + update.message.text)	# some text, I hope it's a price
			return self.dont_send_shopping_window_handler(update, context)
		except Exception as e: 	print(str(e))

