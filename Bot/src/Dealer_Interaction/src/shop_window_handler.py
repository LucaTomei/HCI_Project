from bot_replies import *
from Dealer_Interaction.src.utils import Utils

class Shop_Window_Handler(object):
	def __init__(self):
		self.Utils_Obj = Utils()

	def test_entry_point_main_handler(self, update, context):
		try:
			print(update)
			## TEST - TO REMOVE
			chat_id = update.message.chat.id
			tmp_category = "panificio"		# TAKE THEM FROM get_user_categories IN UTILS
			Utility_Obj.set_user_category(chat_id, tmp_category, context)
			tmp_category = "gastronomia" 	# TAKE THEM FROM get_user_categories IN UTILS
			Utility_Obj.set_user_category(chat_id, tmp_category, context)
			# END TEST - TO REMOVE
			

			user_categories = Utility_Obj.get_user_categories(chat_id, context)
			keyboard_to_show = self.Utils_Obj.make_keyboard(user_categories, len(user_categories))

			Utility_Obj.set_main_keyboard_by_chat_id(chat_id, keyboard_to_show, context)
			
			update.message.reply_text(bot_replies['choice_your_category'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			
			# Test cancellazione messaggio
			# import time
			# time.sleep(2)
			# Bot_Obj.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
			return 0
		except Exception as e: 	print(str(e))
		

	def choice_your_product_handler(self, update, context):
		chat_id = update.message.chat.id
		chat_message = update.message.text
		if self.Utils_Obj.is_category_in_file(chat_message):	# if is really a category
			products_by_category = self.Utils_Obj.get_product_list_by_category_name(chat_message)
			keyboard_to_show = self.Utils_Obj.make_keyboard(products_by_category, len(products_by_category))
			Utility_Obj.set_main_keyboard_by_chat_id(chat_id, keyboard_to_show, context)
			update.message.reply_text(bot_replies['insert_product'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			return 1
		else:	# Blocking loop if not valid category
			keyboard_to_show = Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context)
			context.bot.send_message(chat_id=chat_id, text = bot_replies['choice_your_category'], reply_markup=keyboard_to_show,  parse_mode = ParseMode.MARKDOWN)
			return 0

	def insert_price_handler(self, update, context):
		chat_id = update.message.chat.id
		chat_message = update.message.text

		if self.Utils_Obj.is_product_in_categories(chat_message):
			Utility_Obj.set_tmp_product(chat_id, context, chat_message)	# store in tmp_product
			keyboard_to_show = ReplyKeyboardRemove()
			Utility_Obj.set_main_keyboard_by_chat_id(chat_id, keyboard_to_show, context)
			update.message.reply_text(bot_replies['insert_price'] % chat_message, parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			return 2
		else:
			keyboard_to_show = Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context)
			context.bot.send_message(chat_id=chat_id, text = bot_replies['insert_product'], reply_markup=keyboard_to_show,  parse_mode = ParseMode.MARKDOWN)
			return 1

	def set_product_in_shopping_window_handler(self, update, context):
		chat_id = update.message.chat.id
		chat_message = update.message.text	# now we have the price as chat message

		if self.Utils_Obj.isDigit(chat_message):	# you have insert an integer or float
			this_price = self.Utils_Obj.truncate_float(chat_message)
			this_product = Utility_Obj.get_tmp_product(chat_id, context)
			
			Utility_Obj.set_tmp_product_price(chat_id, context, this_price)

			keyboard_to_show = yes_no_sure_price
			Utility_Obj.set_main_keyboard_by_chat_id(chat_id, keyboard_to_show, context)
			update.message.reply_text(bot_replies['are_you_sure_price'] % (this_product, str(this_price)), parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			return 3

		else:	# loop until is digit
			product = Utility_Obj.get_tmp_product(chat_id, context)
			keyboard_to_show = Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context)
			context.bot.send_message(chat_id=chat_id, text = bot_replies['insert_price'] % product, reply_markup=keyboard_to_show,  parse_mode = ParseMode.MARKDOWN)
			return 2
	
	def yes_no_sure_price_handler(self, update, context):
		chat_id = update.message.chat.id
		chat_message = update.message.text

		if chat_message in [j for i in yes_no_sure_price.keyboard for j in i]:
			if chat_message == bot_buttons['yes_sure_price']:
				pass
			else:
				user_categories = Utility_Obj.get_user_categories(chat_id, context)
				keyboard_to_show = self.Utils_Obj.make_keyboard(user_categories, len(user_categories))

				Utility_Obj.set_main_keyboard_by_chat_id(chat_id, keyboard_to_show, context)
				update.message.reply_text(bot_replies['choice_your_category'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				return 0

		else:	# loop until tou press yes or not
			keyboard_to_show = yes_no_sure_price
			Utility_Obj.set_main_keyboard_by_chat_id(chat_id, keyboard_to_show, context)
			update.message.reply_text(bot_replies['are_you_sure_price'] % (this_product, str(this_price)), parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			return 3

		