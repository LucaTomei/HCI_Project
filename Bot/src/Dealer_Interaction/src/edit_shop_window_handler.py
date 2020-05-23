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


################### 	ADD NEW PRODUCTS
	
	def add_some_products_main_handler(self, update, context):
		print("16.1 (add_some_products_main_handler) : ", update.message.text)
		try:
			chat_id = update.message.chat.id
			Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)

			chat_message = update.message.text
			
			return self.Shop_Window_Handler_Obj.new_entry_point_main_handler(update, context)
		except Exception as e: print(str(e))

