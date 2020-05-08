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
				update.message.reply_text(bot_replies['insert_product'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				return 2
			else:
				print("indietro in choice_your_product_handler")
				keyboard_to_show = subcategories_keyboard
				update.message.reply_text(bot_replies['choice_your_subcategory'], parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show, disable_web_page_preview=True)
				return 1
		except Exception as e: 	print(str(e))


	def pre_insert_product_handler(self, update, context):
		try:
			print("\n2: " + update.message.text)
			chat_id = update.message.chat.id
			chat_message = this_product = update.message.text 		# product name name (eg. Kellogs ...)
			
			products_keyboard = Utility_Obj.get_products_keyboard_by_chat_id(chat_id, context)

			if chat_message in [j for i in products_keyboard.keyboard for j in i]:
				print("Ci sono")
			else:
				print("indietro in pre_insert_product_handler")


		except Exception as e: 	print(str(e))





