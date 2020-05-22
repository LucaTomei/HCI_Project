from bot_replies import *
from . import shop_window_handler

class Edit_Shop_Window_Handler(object):
	def __init__(self):
		self.Shop_Window_Handler_Obj = shop_window_handler.Shop_Window_Handler()
		self.Dealer_Persistence_Obj = self.Shop_Window_Handler_Obj.Dealer_Persistence_Obj

	def dont_edit_shopping_window(self, update, context):
		print("-1 (dont_edit_shopping_window) : ", update.message.text)
		chat_id = update.message.chat.id
		Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)

		chat_message = update.message.text

		message = bot_replies['all_done_shopping_window']
		keyboard = ReplyKeyboardRemove()
		Utility_Obj.set_main_keyboard_by_chat_id(chat_id, keyboard, context)

		# Edit date in file
		group_token = Utils_Obj.make_token(chat_id)
		self.Dealer_Persistence_Obj.set_now_date_by_token(group_token)

		reply_message = update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard)
		Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
		return ConversationHandler.END

	

	def edit_shopping_window_main_handler(self, update, context):
		print("-1 (category_main_handler) : ", update.message.text)
		try:
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)

			chat_message = update.message.text

			keyboard_to_show = edit_shopping_window_execute_keyboard
			Utility_Obj.set_main_keyboard_by_chat_id(chat_id, keyboard_to_show, context)

			
			group_token = Utils_Obj.make_token(chat_id)
			shopping_window = self.Dealer_Persistence_Obj.get_shopping_window_by_token(group_token)
			formatted_shopping_window = Utility_Obj.format_shopping_window(shopping_window)

			message = bot_replies["shop_window_done"] % formatted_shopping_window
			reply_message = update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
			Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
			
			message = bot_replies["what_do_you_want"]
			reply_message = update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard_to_show)
			Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
			return 0
		except Exception as e: print("edit_shopping_window_main_handler: ",str(e))


################### 	ADD NEW PRODUCTS
	
	def add_some_products_main_handler(self, update, context):
		print("0.1 (add_some_products_main_handler) : ", update.message.text)
		try:
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)

			chat_message = update.message.text
		except Exception as e: print(str(e))




################### 	DELETE SOME PRODUCTS
	def delete_some_products_main_handler(self, update, context):
		print("0.2 (delete_some_products_main_handler) : ", update.message.text)
		try:
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)

			chat_message = update.message.text
		except Exception as e: print(str(e))




################### 	EDIT PRICES

	def edit_shopping_window_prices_main_handler(self, update, context):
		print("0.3 (edit_shopping_window_prices_main_handler) : ", update.message.text)
		try:
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)

			chat_message = update.message.text
		except Exception as e: print(str(e))



	def edit_shop_handler(self):
		edit_shop_handler = ConversationHandler(
            [	# Entry Points
            	MessageHandler(Filters.regex('^' + bot_buttons['edit_shopping_window'] +'$') & (Filters.group),self.edit_shopping_window_main_handler),
            	MessageHandler(Filters.regex('^' + bot_buttons['stop_button'] +'$') & (Filters.group),self.dont_edit_shopping_window),
            ], 
            {
            	0:[
            		MessageHandler(Filters.regex('^' + bot_buttons['back_button'] +'$') & (Filters.group),unknown_function_for_groups),
            		MessageHandler(Filters.regex('^' + bot_buttons['add_some_products'] +'$') & (Filters.group),self.add_some_products_main_handler),
            		MessageHandler(Filters.regex('^' + bot_buttons['delete_some_products'] +'$') & (Filters.group),self.delete_some_products_main_handler),
            		MessageHandler(Filters.regex('^' + bot_buttons['edit_shopping_window_prices'] +'$') & (Filters.group),self.edit_shopping_window_prices_main_handler),
            	],
            },[])
		return edit_shop_handler

