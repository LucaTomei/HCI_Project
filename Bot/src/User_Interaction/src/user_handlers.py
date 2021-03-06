from bot_replies import *
from Dealer_Interaction.src import dealer_persistence
from . import user_utils

class User_Handlers(object):
	def __init__(self):
		self.Dealer_Persistence_Obj = dealer_persistence.Dealer_Persistence()
		self.User_Utils_obj = user_utils.User_Utils()

	def unknown_user_function(self, update, context):
		try:
			chat_id = update.message.chat_id
			first_name = update.message.chat.first_name
			first_name = first_name if first_name != None else update.message.from_user.first_name
			group_title = update.message.chat.title
			#registered_shop = self.Dealer_Persistence_Obj.get_formatted_token_merchant_list()
			registered_shop = self.Dealer_Persistence_Obj.get_formatted_shop_names()
			context.bot.send_message(chat_id=chat_id, text = bot_replies['insert_token'] % (first_name, registered_shop), reply_markup=ReplyKeyboardRemove(),  parse_mode = ParseMode.MARKDOWN)
			context.bot.send_message(chat_id=chat_id, text = bot_replies['want_to_buy'], reply_markup=want_to_buy_keyboard,  parse_mode = ParseMode.MARKDOWN)
		except Exception as e:	print("Eccezione in unknown_function:", str(e))

	def insert_token_main_handler(self, update, context):
		try:
			chat_message = update.message.text
			print("1:", chat_message)
			chat_id = update.message.chat.id
			self.User_Utils_obj.init_customer_data(chat_id, context)
			if self.Dealer_Persistence_Obj.is_token_in_persistence(chat_message):
				token = chat_message
				self.User_Utils_obj.set_used_token(chat_id, context, token)
				dealer_shopping_window = self.Dealer_Persistence_Obj.get_shopping_window_by_token(token)

				formatted_shopping_window = Utility_Obj.format_shopping_window(dealer_shopping_window)
				
				dealer_name = self.Dealer_Persistence_Obj.get_group_tytle_by_token(token)
				shop_location = self.Dealer_Persistence_Obj.get_shop_location(token)
				if all(isinstance(x, (int, float)) for x in shop_location):
					shop_location_list = city, address, cap = Utility_Obj.reverse_location(*shop_location)
					shop_location = shop_location_list[0] + " (" + shop_location_list[1] + " - " + shop_location_list[2] + ")"
				update.message.reply_text(bot_replies['shop_window_customer'] %(dealer_name, shop_location, formatted_shopping_window), parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
				
				keyboard_to_show = add_product_show_shopping_cart_keyboard
				update.message.reply_text(bot_replies['show_shopping_window_customer'], parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard_to_show)
			else:	# not valid token
				return self.unknown_user_function(update, context)
			return 1
		except Exception as e:	print("Eccezione in insert_token_main_handler: ",str(e)) 

	def add_product_main_handler(self, update, context):
		try:
			chat_message = update.message.text
			print("1.1:", chat_message)				#AGGIUNGI PRODOTTO
			chat_id = update.message.chat.id

			token = self.User_Utils_obj.get_used_token(chat_id, context)
			dealer_shopping_window = self.Dealer_Persistence_Obj.get_shopping_window_by_token(token)
			dealer_shopping_window_names = self.Dealer_Persistence_Obj.extract_names_from_shopping_window(dealer_shopping_window)
			
			keyboard_to_show = makeAKeyboard(dealer_shopping_window_names, 2)	# keyboard with only product names

			dealer_name = self.Dealer_Persistence_Obj.get_group_tytle_by_token(token)
			update.message.reply_text(bot_replies['show_shopping_window_buttons'] %(dealer_name), parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard_to_show)
			return 2
		except Exception as e:	print("add_product_main_handler",str(e)) 

	def show_shopping_cart_main_handler(self, update, context):
		try:
			chat_message = update.message.text
			print("1.2:", chat_message)				#VISUALIZZA CARRELLO
			chat_id = update.message.chat.id
			shopping_cart = self.User_Utils_obj.get_shopping_cart(chat_id, context)
			print(shopping_cart)
			if len(shopping_cart) == 0:
				update.message.reply_text(bot_replies['empty_shopping_cart'], parse_mode=ParseMode.MARKDOWN)
				return self.add_product_main_handler(update, context)
			else:
				self.User_Utils_obj = user_utils.User_Utils()

				token = self.User_Utils_obj.get_used_token(chat_id, context)
				products_sum = self.Dealer_Persistence_Obj.sum_up_all_shopping_window_prices(shopping_cart, token)
				self.User_Utils_obj.set_shopping_cart(chat_id, context, products_sum)
				total = str(self.User_Utils_obj.make_total(products_sum))
				formatted_cart = self.User_Utils_obj.better_print_shopping_cart(products_sum)

				update.message.reply_text(bot_replies['cart_content'] %(formatted_cart, total), parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
				keyboard_to_show = checkout_or_add_adain_keyboard
				update.message.reply_text(bot_replies['process_checkout'], parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard_to_show)
			return 3
		except Exception as e:	print("Eccezione in show_shopping_cart_main_handler :",str(e)) 

	def back_to_main_handler(self, update, context):
		try:
			chat_message = update.message.text
			print("1.3:", chat_message)
			chat_id = update.message.chat.id
			
			token = self.User_Utils_obj.get_used_token(chat_id, context)
			dealer_shopping_window = self.Dealer_Persistence_Obj.get_shopping_window_by_token(token)
			formatted_shopping_window = Utility_Obj.format_shopping_window(dealer_shopping_window)
			
			dealer_name = self.Dealer_Persistence_Obj.get_group_tytle_by_token(token)
			shop_location = self.Dealer_Persistence_Obj.get_shop_location(token)
			if all(isinstance(x, (int, float)) for x in shop_location) and len(shop_location) == 2:
				shop_location_list = city, address, cap = Utility_Obj.reverse_location(*shop_location)
				shop_location = shop_location_list[0] + " (" + shop_location_list[1] + " - " + shop_location_list[2] + ")"
			update.message.reply_text(bot_replies['shop_window_customer'] %(dealer_name, shop_location, formatted_shopping_window), parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
			
			keyboard_to_show = add_product_show_shopping_cart_keyboard
			update.message.reply_text(bot_replies['show_shopping_window_customer'], parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard_to_show)
			return 1
		except Exception as e:	print("Eccezione in back_to_main_handler: ", str(e)) 


	def pre_add_product_handler(self, update, context):
		try:
			chat_message = update.message.text
			print("2.1:", chat_message)			# any type of text, I hope is a product name
			chat_id = update.message.chat.id

			token = self.User_Utils_obj.get_used_token(chat_id, context)
			dealer_shopping_window = self.Dealer_Persistence_Obj.get_shopping_window_by_token(token)
			if self.Dealer_Persistence_Obj.is_product_in_shopping_window(dealer_shopping_window, chat_message):
				product_name = chat_message
				
				product_details = self.Dealer_Persistence_Obj.get_product_details_by_product_name(dealer_shopping_window, product_name)
				product_price, product_unit = (product_details['price'], product_details['unit'])

				update.message.reply_text(bot_replies['add_product_shopping_cart'] % (product_unit, product_name, str(product_price)), parse_mode=ParseMode.MARKDOWN)
				keyboard_to_show = add_or_select_other_product_keyboard
				update.message.reply_text(bot_replies['sure_add_product_cart'], parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard_to_show)
				
				self.User_Utils_obj.set_tmp_product(chat_id, context, product_details)
			else:
				return self.add_product_main_handler(update, context)
			return 4
		except Exception as e:	print("pre_add_product_handler",str(e)) 

	def end_add_product_handler(self, update, context):
		try:
			chat_message = update.message.text
			print("2.2:", chat_message)			# Fine
			chat_id = update.message.chat.id
			return self.show_shopping_cart_main_handler(update, context)
		except Exception as e:	print("end_add_product_handler",str(e)) 


	def add_product_in_context_handler(self, update, context):
		try:
			chat_message = update.message.text
			print("4.1:", chat_message)			# AGGIUNGI
			chat_id = update.message.chat.id
			tmp_product = self.User_Utils_obj.get_tmp_product(chat_id, context)

			# add in shopping cart
			self.User_Utils_obj.append_to_shopping_cart(chat_id, context, tmp_product)

			print(self.User_Utils_obj.get_shopping_cart(chat_id, context))
			keyboard_to_show = add_or_show_shopping_cart
			update.message.reply_text(bot_replies['add_to_cart_done'], parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard_to_show)
			return 5
		except Exception as e:	print("add_product_in_context_handler",str(e)) 

	def select_other_product_handler(self, update, context):
		try:
			chat_message = update.message.text
			print("4.2:", chat_message)			# SELEZIONA UN ALTRO PRODOTTO
			chat_id = update.message.chat.id
			return self.add_product_main_handler(update, context)
		except Exception as e:	print("select_other_product_handler",str(e)) 
	
	def loop_in_add_or_select_other_handler(self, update, context):
		try:
			chat_message = update.message.text
			print("4.3:", chat_message)			# Other text
			chat_id = update.message.chat.id
			product_details = self.User_Utils_obj.get_tmp_product(chat_id, context)
			product_name, product_price, product_unit = (product_details['name'], product_details['price'], product_details['unit'])

			update.message.reply_text(bot_replies['add_product_shopping_cart'] % (product_unit, product_name, str(product_price)), parse_mode=ParseMode.MARKDOWN)
			keyboard_to_show = add_or_select_other_product_keyboard
			update.message.reply_text(bot_replies['sure_add_product_cart'], parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard_to_show)
			
			self.User_Utils_obj.set_tmp_product(chat_id, context, product_details)
		except Exception as e:	print("loop_in_add_or_select_other_handler",str(e)) 

	def add_other_products_handler(self, update, context):
		try:
			chat_message = update.message.text
			print("5.1:", chat_message)			# bot_buttons['add_other_products']
			chat_id = update.message.chat.id
			return self.add_product_main_handler(update, context)
		except Exception as e:	print("add_other_products_handler",str(e)) 

	def loop_in_add_or_show_handler(self, update, context):
		try:
			chat_message = update.message.text
			print("5.3:", chat_message)			# Other Text
			chat_id = update.message.chat.id
			keyboard_to_show = add_or_show_shopping_cart
			update.message.reply_text(bot_replies['add_to_cart_done'], parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard_to_show)
			return 5
		except Exception as e:	print("loop_in_add_or_show_handler",str(e)) 


	def checkout_main_handler(self, update, context):
		try:
			chat_message = update.message.text
			print("3:", chat_message)			# CHECKOUT
			chat_id = update.message.chat.id

			keyboard_to_show = delete_or_send_keyboard

			token = self.User_Utils_obj.get_used_token(chat_id, context)
			dealer_name = self.Dealer_Persistence_Obj.get_group_tytle_by_token(token)
			update.message.reply_text(bot_replies['checkout_main'] % (dealer_name), parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard_to_show)
			return 6
		except Exception as e:	print("checkout_main_handler",str(e)) 



	def send_shopping_cart_handler(self, update, context):
		try:
			chat_message = update.message.text
			print("6.2:", chat_message)			# INVIA LISTA DELLA SPESA
			chat_id = update.message.chat.id
			token = self.User_Utils_obj.get_used_token(chat_id, context)
			dealer_chat_id = self.User_Utils_obj.decrypt_token(token)
			
			update.message.reply_text(bot_replies['send_shopping_cart_done'],parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())


			shopping_cart = self.User_Utils_obj.get_shopping_cart(chat_id, context)
			products_sum = self.Dealer_Persistence_Obj.sum_up_all_shopping_window_prices(shopping_cart, token)
			total = str(self.User_Utils_obj.make_total(products_sum))
			formatted_cart = self.User_Utils_obj.better_print_shopping_cart(products_sum)

			message = bot_replies['arrived_new_shopping_cart'] % (update.message.chat.first_name, formatted_cart, str(total))
			context.bot.send_message(chat_id=dealer_chat_id, text = message, reply_markup=ReplyKeyboardRemove(),  parse_mode = ParseMode.MARKDOWN)
			

			########
			# AUTOMATIZZAZIONE INVIO MESSAGGIO
			########
			job = context.job_queue.run_once(automatize_message, 10, context=update.message)	# after 10 secs
			
			my_name = update.message.chat.first_name
			merchant_name = self.Dealer_Persistence_Obj.get_group_tytle_by_token(token)
			job.context = chat_id, my_name, merchant_name, formatted_cart, total


			return ConversationHandler.END
		except Exception as e:	print("send_shopping_cart_handler: " + str(e)) 

	def delete_product_main_handler(self, update, context):
		try:
			chat_message = update.message.text
			print("6.1:", chat_message)			# ELIMINA PRODOTTO
			chat_id = update.message.chat.id

			shopping_cart = self.User_Utils_obj.get_shopping_cart(chat_id, context)
			product_names = [item['name'] for item in shopping_cart]

			keyboard_to_show = make_upper_back_keyboard(product_names, len(product_names))
			self.User_Utils_obj.set_products_keyboard(chat_id, context,keyboard_to_show)
			update.message.reply_text(bot_replies['delete_product'], parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard_to_show)
			return 7
		except Exception as e:	print(str(e)) 

	def delete_product_execute_handler(self, update, context):
		try:
			chat_message = update.message.text
			print("7:", chat_message)			# Any type of text
			chat_id = update.message.chat.id

			products_keyboard = self.User_Utils_obj.get_products_keyboard(chat_id, context)
			if chat_message in [j for i in products_keyboard.keyboard for j in i]:
				product_name = chat_message
				self.User_Utils_obj.set_tmp_product(chat_id, context, product_name)
				keyboard_to_show = delete_product_or_back_keyboard


				token = self.User_Utils_obj.get_used_token(chat_id, context)

				product_details = self.Dealer_Persistence_Obj.get_original_product_details(product_name, token)
				unit, name = product_details['unit'], product_details['name']
				update.message.reply_text(bot_replies['sure_delete_product_in_cart'] %(unit, name), parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard_to_show)
				return 8
			else:	# loop
				return self.delete_product_main_handler(update, context)
		except Exception as e:	print(str(e)) 

	def really_delete_product_handler(self, update, context):
		try:

			chat_message = update.message.text
			print("8:", chat_message)			# ELIMINA PRODOTTO
			chat_id = update.message.chat.id
			product_name = self.User_Utils_obj.get_tmp_product(chat_id, context)
			shopping_cart = self.User_Utils_obj.get_shopping_cart(chat_id, context)


			token = self.User_Utils_obj.get_used_token(chat_id, context)
			shopping_cart = self.Dealer_Persistence_Obj.decrement_quantity(shopping_cart, product_name, token)
			# # side effect in context
			self.User_Utils_obj.set_shopping_cart(chat_id, context, shopping_cart)

			
			update.message.reply_text(bot_replies['delete_product_success'], parse_mode=ParseMode.MARKDOWN)
			return self.show_shopping_cart_main_handler(update, context)
		except Exception as e:	print(str(e)) 


########	NEW ENTRY POINT
	

########
	
	def want_to_buy_yes_main_handler(self, update, context):
		try:
			chat_message = update.message.text
			print("-1.1:", chat_message)
			chat_id = update.message.chat.id

			all_shop_names = self.Dealer_Persistence_Obj.get_all_merchant_names()

			keyboard_to_show = makeAKeyboard(all_shop_names, 1)
			
			update.message.reply_text(bot_replies['show_shops'], parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard_to_show)
			return 0
		except Exception as e:	print("want_to_buy_yes_main_handler: ", str(e))
	
	def refresh_shopping_window_main_handler(self, update, context):
		try:
			chat_message = update.message.text
			print("1.1:", chat_message)			# Fine
			chat_id = update.message.chat.id
			

		except Exception as e:	print("refresh_shopping_window_main_handler: ", str(e))

	def choice_shop_name_main_handler(self, update, context):
		try:
			chat_message = update.message.text
			print("1.2:", chat_message)			# Any Text. I hope shop name
			chat_id = update.message.chat.id
			
			all_shop_names = self.Dealer_Persistence_Obj.get_all_merchant_names()
			if chat_message in all_shop_names:
				# Side effect in update.message.text
				update.message.text = self.Dealer_Persistence_Obj.from_merchant_name_to_token(chat_message)
				return self.insert_token_main_handler(update, context)
			else:
				return self.want_to_buy_yes_main_handler(update, context)
		except Exception as e:	print("choice_shop_name_main_handler: ", str(e))


	def want_to_buy_no_main_handler(self, update, context):
		try:
			chat_message = update.message.text
			print("-1.2:", chat_message)		#	NO - Aggiorna lista Negozi
			chat_id = update.message.chat.id

			keyboard_to_show = update_shop_list_keyboard
			update.message.reply_text(bot_replies['no_dont_buy'], parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard_to_show)
			return ConversationHandler.END

		except Exception as e:	print("want_to_buy_no_main_handler: ", str(e))


	def register_user_handlers(self):
		register_user_handlers  = ConversationHandler(
			[
        		MessageHandler(Filters.regex('^' + bot_buttons['want_to_buy_yes'] +'$'),self.want_to_buy_yes_main_handler),
        		MessageHandler(Filters.regex('^' + bot_buttons['want_to_buy_no'] +'$'),self.want_to_buy_no_main_handler),
			],
			{
				0:[
					MessageHandler(Filters.regex('^' + bot_buttons['stop_button'] +'$'),self.want_to_buy_no_main_handler),
					MessageHandler(Filters.text, self.choice_shop_name_main_handler),
				],
				1:[
					MessageHandler(Filters.regex('^' + bot_buttons['add_product'] +'$'),self.add_product_main_handler),
					MessageHandler(Filters.regex('^' + bot_buttons['show_shopping_cart'] +'$'),self.show_shopping_cart_main_handler),
					MessageHandler(Filters.text, self.back_to_main_handler),
				],
				2:[
					MessageHandler(Filters.regex('^' + bot_buttons['stop_button'] +'$'),self.end_add_product_handler),
					MessageHandler(Filters.text, self.pre_add_product_handler),
				],
				3:[	# show shopping cart - Checkout or add
					MessageHandler(Filters.regex('^' + bot_buttons['checkout'] +'$'),self.checkout_main_handler),
					MessageHandler(Filters.regex('^' + bot_buttons['add_again'] +'$'),self.add_other_products_handler),
					MessageHandler(Filters.text, self.show_shopping_cart_main_handler),
				],
				4:[	# really add product in shopping cart
					MessageHandler(Filters.regex('^' + bot_buttons['add_product_done'] +'$'),self.add_product_in_context_handler),
					MessageHandler(Filters.regex('^' + bot_buttons['select_other_product'] +'$'),self.select_other_product_handler),
					MessageHandler(Filters.text, self.loop_in_add_or_select_other_handler),

				],
				5:[ # Add other products or show shopping cart
					MessageHandler(Filters.regex('^' + bot_buttons['add_other_products'] +'$'),self.add_other_products_handler),
					MessageHandler(Filters.regex('^' + bot_buttons['show_shopping_cart'] +'$'),self.show_shopping_cart_main_handler),
					MessageHandler(Filters.text, self.loop_in_add_or_show_handler),
				],
				6:[	# delete or send shopping cart
					MessageHandler(Filters.regex('^' + bot_buttons['delete_product'] +'$'),self.delete_product_main_handler),
					MessageHandler(Filters.regex('^' + bot_buttons['send_shopping_cart'] +'$'),self.send_shopping_cart_handler),
					MessageHandler(Filters.text, self.checkout_main_handler),
				],
				7:[
					MessageHandler(Filters.regex('^' + bot_buttons['back_button'] +'$'),self.checkout_main_handler),
					MessageHandler(Filters.text, self.delete_product_execute_handler),
				],
				8:[
					MessageHandler(Filters.regex('^' + bot_buttons['back_button'] +'$'),self.delete_product_main_handler),
					MessageHandler(Filters.regex('^' + bot_buttons['delete_product'] +'$'),self.really_delete_product_handler),

				],
			},[], persistent=True, name='register_user_handlers')
		return register_user_handlers





