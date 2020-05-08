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

			Utility_Obj.set_main_keyboard_by_chat_id(chat_id, keyboard_to_show, context)
			
			update.message.reply_text(bot_replies['choice_your_category'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
			
			# Test cancellazione messaggio
			# import time
			# time.sleep(2)
			# Bot_Obj.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
			return 0
		except Exception as e: 	print(str(e))
	
	def choice_your_subcategory_handler(self, update, context):
		try:
			chat_id = update.message.chat.id
			print("0: " + update.message.text, Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context).keyboard)
			chat_message = update.message.text
			if self.Utils_Obj.is_category_in_file(chat_message):	# if is really a category
				Utility_Obj.set_tmp_category(chat_id, chat_message, context)	# set category in context
				subcategories = self.Utils_Obj.get_subcategories_name_by_category(chat_message)
				
				keyboard_to_show = self.Utils_Obj.make_back_keyboard(subcategories, 3)

				Utility_Obj.set_main_keyboard_by_chat_id(chat_id, keyboard_to_show, context)
				update.message.reply_text(bot_replies['choice_your_subcategory'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				return 1
			else:	# Blocking loop if not valid category
				print("sono qui")
				keyboard_to_show = Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context)
				update.message.reply_text(bot_replies['choice_your_category'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				return 0
		except Exception as e: 	print(str(e))


	def choice_product_handler(self, update, context):
		try:
			chat_id = update.message.chat.id
			print("1: " + update.message.text, Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context).keyboard)
			chat_message = update.message.text
			
			if chat_message in [j for i in Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context).keyboard for j in i]:
				category_name = Utility_Obj.get_tmp_category(chat_id, context)
				Utility_Obj.set_tmp_subcategory(chat_id, context, chat_message)
				subcategory_products = self.Utils_Obj.get_subcategory_products(category_name, chat_message)
				
				(name, units) = self.Utils_Obj.from_subcat_prod_dict_to_list(subcategory_products)

				keyboard_to_show = self.Utils_Obj.make_back_keyboard(name, 3)
				print("sono qui ioooo", Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context).keyboard)
				Utility_Obj.set_main_keyboard_by_chat_id(chat_id, keyboard_to_show, context)
				print("\nsono qui ioooo", Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context).keyboard)

				update.message.reply_text(bot_replies['insert_product'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				return 2
			else:
				keyboard_to_show = Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context)
				update.message.reply_text(bot_replies['choice_your_subcategory'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				return 1
		except Exception as e: 	print(str(e))


	def back_to_choice_product_handler(self, update, context):
		chat_id = update.message.chat.id
		chat_message = update.message.text
		print("\nqui con: ")
		print(Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context))
	
	
	def insert_price_handler(self, update, context):
		chat_id = update.message.chat.id
		chat_message = update.message.text
		print("2: " + update.message.text)
		print("\n\n", Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context).keyboard)
		try:
			pass
		except Exception as e: 	print(str(e))
	