from bot_replies import *
from Dealer_Interaction.src.utils import Utils
from Dealer_Interaction.src.dealer_persistence import Dealer_Persistence

class Shop_Window_Handler(object):
	def __init__(self):
		self.Utils_Obj = Utils()
		self.Dealer_Persistence_Obj = Dealer_Persistence()

	
	
	def new_entry_point_main_handler(self, update, context):
		try:
			print("new_entry_point_main_handler:",update.message.text)
			

			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)

			user_categories = Utility_Obj.get_user_categories(chat_id, context)
		
			group_token = self.Utils_Obj.make_token(chat_id)

			message_to_send = ""
			if len(user_categories) == 0 and Dealer_Persistence_Obj.is_token_in_persistence(group_token):		
				user_categories = self.Dealer_Persistence_Obj.get_categories_list_by_token(group_token)
				shopping_window_in_file = self.Dealer_Persistence_Obj.get_shopping_window_by_token(group_token)

				Utility_Obj.set_shopping_window_list_by_chat_id(chat_id, context, shopping_window_in_file)
				message_to_send = bot_replies['choice_your_category_edit']

			keyboard_to_show = make_keyboard(user_categories, 1)

			Utility_Obj.set_categories_keyboard_by_chat_id(chat_id, context, keyboard_to_show)
			
			if message_to_send == "": 	message_to_send = bot_replies['choice_your_category']
			reply_message = update.message.reply_text(message_to_send, parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			
			Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
			
			return 4
		except Exception as e: 	print("Eccezione in new_entry_point_main_handler :",str(e))
	
	def choice_your_subcategory_handler(self, update, context):
		try:
			print("4: " + update.message.text)
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)

			chat_message = this_category = update.message.text 		# Category name (eg. alimentari)
			if self.Utils_Obj.is_category_in_file(this_category):
				subcategories_list = self.Utils_Obj.get_subcategories_name_by_category(this_category)
				
				keyboard_to_show = make_upper_end_back_keyboard(subcategories_list, 3)
				
				Utility_Obj.set_tmp_category(chat_id, chat_message, context)
				Utility_Obj.set_subcategories_keyboard_by_chat_id(chat_id, context, keyboard_to_show)
				
				reply_message = update.message.reply_text(bot_replies['choice_your_subcategory'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
				return 5
			else:
				print("indietro in choice_your_subcategory_handler")
				keyboard_to_show = Utility_Obj.get_categories_keyboard_by_chat_id(chat_id, context)
				
				reply_message = update.message.reply_text(bot_replies['choice_your_category'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
				return 4
		except Exception as e: 	print("Eccezione in choice_your_subcategory_handler:",str(e))


	def choice_your_product_handler(self, update, context):
		try:
			print("\n5: " + update.message.text)
			chat_id = update.message.chat.id
			chat_message = this_subcategory = update.message.text 		# SubCategory name (eg. Cereali)
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)

			subcategories_keyboard = Utility_Obj.get_subcategories_keyboard_by_chat_id(chat_id, context)
			if chat_message in [j for i in subcategories_keyboard.keyboard for j in i] and chat_message != bot_buttons['back_button']:
				Utility_Obj.set_tmp_subcategory(chat_id, context, this_subcategory)

				category_name = Utility_Obj.get_tmp_category(chat_id, context)
				products_by_subcategory = self.Utils_Obj.get_subcategory_products(category_name, this_subcategory)

				(product_names, product_units) = self.Utils_Obj.from_subcat_prod_dict_to_list(products_by_subcategory)
				keyboard_to_show = make_upper_back_keyboard(product_names, 3)
				Utility_Obj.set_products_keyboard_by_chat_id(chat_id, context, keyboard_to_show)
				
				reply_message = update.message.reply_text(bot_replies['insert_product'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
				return 6
			else:
				print("indietro in choice_your_product_handler")
				keyboard_to_show = subcategories_keyboard
				
				reply_message = update.message.reply_text(bot_replies['choice_your_subcategory'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
				return 5
		except Exception as e: 	print("Eccezione in choice_your_product_handler:", str(e))


	def pre_insert_product_price_handler(self, update, context):
		try:
			print("\n6: " + update.message.text)
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)

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
				
				reply_message = update.message.reply_text(bot_replies['insert_price'] %(this_product_units, this_product), parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
				return 7
			else:
				print("indietro in pre_insert_product_handler")
				keyboard_to_show = products_keyboard
				
				reply_message = update.message.reply_text(bot_replies['insert_product'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
				return 6
		except Exception as e: 	print("Eccezione in pre_insert_product_price_handler:",str(e))


	def insert_product_price_handler(self, update, context):
		try:
			print("\n7: " + update.message.text)
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)

			chat_message = update.message.text 		# 1.3 (price)
			
			#verify if is really a formatted price
			if self.Utils_Obj.isDigit(chat_message):
				this_product_price = self.Utils_Obj.truncate_float(chat_message)	# from string to float
				Utility_Obj.set_tmp_product_price(chat_id, context, this_product_price)

				this_product = Utility_Obj.get_tmp_product(chat_id, context)
				this_product_name = list(this_product.keys())[0]	# eg. Kellogs

				keyboard_to_show = yes_no_sure_price
				
				reply_message = update.message.reply_text(bot_replies['are_you_sure_price'] %(this_product_name, str(this_product_price)), parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
				return 8
			else:	# if is not a price
				products_keyboard = Utility_Obj.get_products_keyboard_by_chat_id(chat_id, context)
				keyboard_to_show = products_keyboard
				
				reply_message = update.message.reply_text(bot_replies['insert_product'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
				return 6
		except Exception as e: 	print("Eccezione in insert_product_price_handler:",str(e))

#---------[_yes_no_sure_price_handler]---------
	def loop_in_yes_no_sure_price_handler(self, update, context):
		try:
			print("\n8.1: " + update.message.text)
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)

			chat_message = update.message.text 		# you have insert something different from yes or no sure price

			this_product_price = Utility_Obj.get_tmp_product_price(chat_id, context)
			this_product = Utility_Obj.get_tmp_product(chat_id, context)
			this_product_name = list(this_product.keys())[0]	# eg. Kellogs


			keyboard_to_show = yes_no_sure_price
			reply_message = update.message.reply_text(bot_replies['are_you_sure_price'] %(this_product_name, str(this_product_price)), parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
			return 8
		except Exception as e: 	print("Eccezione in loop_in_yes_no_sure_price_handler:",str(e))

	def yes_insert_other_products_handler(self, update, context):
		try:
			print("\n8.2: " + update.message.text)
			chat_id = update.message.chat.id
			chat_message = update.message.text 		# you have pressed yes
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)


			# if you have pressed yes, store tmp product in shopping window list
			(product_name_and_unit, product_price) = (Utility_Obj.get_tmp_product(chat_id, context),Utility_Obj.get_tmp_product_price(chat_id, context))
			product_name = list(product_name_and_unit.keys())[0]
			product_unit = list(product_name_and_unit.values())[0]
			product_and_price = {"name": product_name, "price": product_price, "unit": product_unit}
			Utility_Obj.append_to_shopping_window_list(chat_id, context, product_and_price)

			keyboard_to_show = other_product_main_keyboard
			reply_message = update.message.reply_text(bot_replies['shop_window'] %(product_name), parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
			print("\tLista: ",  Utility_Obj.get_shopping_window_list_by_chat_id(chat_id, context))
			return 5 + 4
		except Exception as e: 	print("Eccezione in yes_insert_other_products_handler:",str(e))

	def no_back_to_shopping_window_handler(self, update, context):
		try:
			print("\n8.3: " + update.message.text)
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)

			chat_message = update.message.text 		# you have pressed no

			# Utility_Obj.reset_shopping_window(chat_id, context)	# reset all temp products and keyboard
			# user_categories = Utility_Obj.get_user_categories(chat_id, context)
			# keyboard_to_show = self.Utils_Obj.make_keyboard(user_categories, 1)

			# Utility_Obj.set_categories_keyboard_by_chat_id(chat_id, context, keyboard_to_show)
			keyboard_to_show = Utility_Obj.get_products_keyboard_by_chat_id(chat_id, context)
			
			reply_message = update.message.reply_text(bot_replies['choice_your_category'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
			return 6
		except Exception as e: 	print("Eccezione in no_back_to_shopping_window_handler:",str(e))


#---------[insert_new_product or end]---------
	def loop_in_shopping_window_go_end_handler(self, update, context):
		try:
			print("\n9.1: " + update.message.text)
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)

			chat_message = update.message.text 		# some text different from (Inserisci nuovo prodotto, Fine - vedi vetrina)
			
			product_name_and_unit = Utility_Obj.get_tmp_product(chat_id, context)
			product_name = list(product_name_and_unit.keys())[0]
			
			keyboard_to_show = other_product_main_keyboard
			reply_message = update.message.reply_text(bot_replies['shop_window'] %(product_name), parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
			return 9
		except Exception as e: 	print("Eccezione in loop_in_shopping_window_go_end_handler:",str(e))

	def show_shopping_window_handler(self, update, context):
		try:
			print("\n9.2: " + update.message.text)
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)

			chat_message = update.message.text 		# Fine - vedi vetrina
			
			shopping_window = Utility_Obj.get_shopping_window_list_by_chat_id(chat_id, context)
			if len(shopping_window) == 0:
				return self.new_entry_point_main_handler(update, context)

			group_token = self.Utils_Obj.make_token(chat_id)
			
			
			formatted_shopping_window = Utility_Obj.format_shopping_window(shopping_window)	# this is a string and not a list
			
			keyboard_to_show = send_shop_window_keyboard
			reply_message = update.message.reply_text(bot_replies['shop_window_done'] %(formatted_shopping_window), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
			#Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
			reply_message = update.message.reply_text(bot_replies['want_to_send'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
			return 10
		except Exception as e: 	print("Eccezione in show_shopping_window_handler:",str(e))

	def insert_new_products_handler(self, update, context):
		try:
			print("\n9.3: " + update.message.text)	# Inserisci nuovo prodotto
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)
			return self.no_back_to_shopping_window_handler(update, context)
		except Exception as e: 	print("Eccezione in insert_new_products_handler:",str(e))



#---------[Send Shopping window]---------
	def loop_in_end_shopping_window_handler(self, update, context):
		try:
			print("\n10.1: " + update.message.text)# some text different from ("SI - Invia ai clienti" or "NO - Modifica Prodotti")
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)
			return self.show_shopping_window_handler(update, context)
		except Exception as e: 	print("Eccezione in loop_in_end_shopping_window_handler:",str(e))

	def yes_send_shopping_window_handler(self, update, context):
		try:
			print("\n10.2: " + update.message.text)
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)


			chat_message = update.message.text 		# "SI - Invia ai clienti"
			keyboard_to_show = ReplyKeyboardRemove()

			user_token = self.Utils_Obj.make_token(chat_id)

			reply_message = update.message.reply_text(bot_replies['shop_window_send'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			#Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
			reply_message = update.message.reply_text(bot_replies['shop_window_send_token'] %(user_token), parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			#Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
			reply_message = update.message.reply_text(bot_replies['shop_window_send_done'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			#Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)



			keyboard_to_show = edit_shopping_window_keyboard
			Utility_Obj.set_main_keyboard_by_chat_id(chat_id, keyboard_to_show, context)
			Utility_Obj.set_shopping_window_date(chat_id, context, datetime.now())
			
			#user_categories = self.Dealer_Persistence_Obj.get_categories_list_by_token(user_token)
			
			dealer_infos = Utility_Obj.prepare_persistence(chat_id, context)


			self.Dealer_Persistence_Obj.append_dealer_persistence(user_token, dealer_infos)

			if len(dealer_infos['categories_list']) == 0:
				user_categories = self.Dealer_Persistence_Obj.get_categories_list_by_token(user_token)
				self.Dealer_Persistence_Obj.set_categories_list_by_token(user_token, user_categories)

			# Remove old messages
			job = context.job_queue.run_once(deleteMessages, 2, context=update.message)
			messages_to_delete = Utility_Obj.get_messages_to_delete(chat_id, context)
			job.context = (chat_id, messages_to_delete)
			Utility_Obj.reset_messages_to_delete(chat_id, context)

			return ConversationHandler.END
		except Exception as e: 	print("Eccezione in yes_send_shopping_window_handler:",str(e))

	def dont_send_shopping_window_handler(self, update, context):
		try:
			print("\n10.3: " + update.message.text)
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)

			chat_message = update.message.text 		# "NO - Modifica Prodotti"

			shopping_window = Utility_Obj.get_shopping_window_list_by_chat_id(chat_id, context)
			shopping_window_names_list = Utility_Obj.get_all_shopping_window_names(shopping_window)

			keyboard_to_show = make_upper_back_keyboard(shopping_window_names_list, 3)
			Utility_Obj.set_shopping_window_keyboard(chat_id, context, keyboard_to_show)	# store shopping_window keyboard products 
			
			reply_message = update.message.reply_text(bot_replies['edit_shopping_window'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
			return 11
		except Exception as e: 	print("Eccezione in dont_send_shopping_window_handler:",str(e))

#---------[Edit or delete product]---------
	def edit_your_products_main_handler(self, update, context):
		try:
			print("\n11: " + update.message.text)
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)

			chat_message = update.message.text 		# all type of text

			shopping_window_products_keyboard = Utility_Obj.get_shopping_window_keyboard(chat_id, context)
			if chat_message in [j for i in shopping_window_products_keyboard.keyboard for j in i]:
				keyboard_to_show = delete_edit_keyboard
				shopping_window = Utility_Obj.get_shopping_window_list_by_chat_id(chat_id, context)
				this_product = self.Utils_Obj.get_product_infos(shopping_window, chat_message)
				Utility_Obj.set_tmp_product(chat_id, context, this_product)
				
				reply_message = update.message.reply_text(bot_replies['edit_action'] % chat_message, parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
				return 12
			else:
				return self.dont_send_shopping_window_handler(update, context)	# go back
		except Exception as e: 	print("Eccezione in edit_your_products_main_handler:",str(e))

	def edit_this_product_handler(self, update, context):
		try:
			print("\n12.1: " + update.message.text)
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)


			chat_message = update.message.text 		#	"Modificare il Prezzo"

			shopping_window = Utility_Obj.get_shopping_window_list_by_chat_id(chat_id, context)
			tmp_product  = Utility_Obj.get_tmp_product(chat_id, context)	#	 {'name': 'Blanche de Namur', 'price': 1.0, 'unit': '0.33l'}
			
			keyboard_to_show = ReplyKeyboardRemove()
			
			reply_message = update.message.reply_text(bot_replies['edit_product_price'] % (tmp_product['unit'], tmp_product['name']), parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
			return 14
		except Exception as e: 	print("Eccezione in edit_this_product_handler:",str(e))


	def delete_product_handler(self, update, context):
		try:
			print("\n12.2: " + update.message.text)
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)

			chat_message = update.message.text 		#	"Eliminare il Prodotto",

			tmp_product  = Utility_Obj.get_tmp_product(chat_id, context)	#  {'name': 'Blanche de Namur', 'price': 1.0, 'unit': '0.33l'}
			tmp_product_name = tmp_product['name']
			keyboard_to_show = delete_product_sure_keyboard
			
			reply_message = update.message.reply_text(bot_replies['sure_delete_product'] % tmp_product_name, parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
			return 13
		except Exception as e: 	print("Eccezione in delete_product_handler:",str(e))



	def delete_product_done_handler(self, update, context):
		try:
			print("\n13.1: " + update.message.text)
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)

			chat_message = update.message.text

			tmp_product  = Utility_Obj.get_tmp_product(chat_id, context)
			shopping_window = Utility_Obj.get_shopping_window_list_by_chat_id(chat_id, context)
			shopping_window = self.Utils_Obj.tmp_remove_product_from_shopping_window(shopping_window, tmp_product['name'])
			Utility_Obj.manually_set_shopping_window(chat_id, context, shopping_window)
			
			reply_message = update.message.reply_text(bot_replies['deletion_done'] % tmp_product['name'], parse_mode=ParseMode.MARKDOWN, reply_markup = ReplyKeyboardRemove(), disable_web_page_preview=True)
			Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
			return self.show_shopping_window_handler(update, context)

		except Exception as e: 	print("Eccezione in delete_product_done_handler:",str(e))

	def dont_delete_product_handler(self, update, context):
		try:
			print("\n13.2: " + update.message.text)
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)

			chat_message = update.message.text

			shopping_window = Utility_Obj.get_shopping_window_list_by_chat_id(chat_id, context)
			shopping_window_names_list = Utility_Obj.get_all_shopping_window_names(shopping_window)

			keyboard_to_show = make_upper_back_keyboard(shopping_window_names_list, 3)
			Utility_Obj.set_shopping_window_keyboard(chat_id, context, keyboard_to_show)	# store shopping_window keyboard products 
			
			reply_message = update.message.reply_text(bot_replies['edit_shopping_window'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
			return 11
		except Exception as e: 	print("Eccezione in dont_delete_product_handler:",str(e))

	def back_to_are_you_sure_delete_product_handler(self, update, context):
		try:
			print("\n13.3: " + update.message.text)
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)
			return self.delete_product_handler(update, context)	# some text (different from "Si elimina proddotto" and ...)
		except Exception as e: 	print("Eccezione in back_to_are_you_sure_delete_product_handler:",str(e))




	def set_new_product_price_handler(self, update, context):
		try:
			print("\n14: " + update.message.text)	# some text, I hope it's a price
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)

			chat_message = update.message.text
			if self.Utils_Obj.isDigit(chat_message):
				new_price = chat_message
				tmp_product  = Utility_Obj.get_tmp_product(chat_id, context)
				shopping_window = Utility_Obj.get_shopping_window_list_by_chat_id(chat_id, context)
				Utility_Obj.set_tmp_product_price(chat_id, context, new_price)
				#shopping_window = self.Utils_Obj.edit_shopping_window_price(self, shopping_window, tmp_product['name'], new_price)
				keyboard_to_show = edit_product_price_keyboard
				reply_message = update.message.reply_text(bot_replies['sure_edit_price'] % (tmp_product['name'],new_price), parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
				return 15
			else:
				return self.edit_this_product_handler(update, context) 
		except Exception as e: 	print("Eccezione in set_new_product_price_handler:",str(e))



	def edit_product_price_done_handler(self, update, context):
		try:
			print("\n15.1: " + update.message.text)	# some text, I hope it's a price
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)

			chat_message = update.message.text

			tmp_product  = Utility_Obj.get_tmp_product(chat_id, context)
			tmp_product_price = Utility_Obj.get_tmp_product_price(chat_id, context)
			shopping_window = Utility_Obj.get_shopping_window_list_by_chat_id(chat_id, context)
			shopping_window = self.Utils_Obj.edit_shopping_window_price(shopping_window, tmp_product['name'], tmp_product_price)
			Utility_Obj.manually_set_shopping_window(chat_id, context, shopping_window)
			shopping_window = Utility_Obj.get_shopping_window_list_by_chat_id(chat_id, context)
			
			keyboard_to_show = ReplyKeyboardRemove()
			
			reply_message = update.message.reply_text(bot_replies['edit_product_price_done'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
			return self.show_shopping_window_handler(update, context)
		except Exception as e: 	print("Eccezione in edit_product_price_done_handler:",str(e))

	def dont_edit_price_handler(self, update, context):
		try:
			print("\n15.2: " + update.message.text)	# some text, I hope it's a price
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)
			return self.dont_send_shopping_window_handler(update, context)
		except Exception as e: 	print("Eccezione in dont_edit_price_handler:",str(e))

