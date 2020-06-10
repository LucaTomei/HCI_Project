from bot_replies import *

from Dealer_Interaction.src import dealer_handlers
from User_Interaction.src import user_handlers


class Bot(object):
	def __init__(self):
		self.Dealer_Handlers_Obj = dealer_handlers.Dealer_Handlers()
		self.User_Handlers_Obj = user_handlers.User_Handlers()

		self.bot_persistence = PicklePersistence(filename = persistence_filename)

	def start(self, update, context):
		chat_id = update.message.chat_id
		group_title = update.message.chat.title
		first_name = update.message.chat.first_name
		first_name = first_name if first_name != None else update.message.from_user.first_name
		if 'group' in update.message.chat.type:
			Utility_Obj.set_user_data(chat_id, context, main_keyboard, group_title)
			Utility_Obj.set_telegram_link(update, context)
			context.bot.send_message(chat_id=update.effective_chat.id, text = bot_replies['dealer_welcome_message'] % (first_name, group_title), reply_markup=yes_no_keyboard,  parse_mode = ParseMode.MARKDOWN)
		else:
			context.bot.send_message(chat_id=chat_id, text = bot_replies['insert_token'] % first_name, reply_markup=ReplyKeyboardRemove(),  parse_mode = ParseMode.MARKDOWN)
		
	def allow_mod(self, update, context):
		try:
			Dealer_Persistence_Obj = self.Dealer_Handlers_Obj.Shop_Window_Handler_Obj.Dealer_Persistence_Obj
			token = context.args[0]
			Dealer_Persistence_Obj.reset_date_by_token(token)
			update.message.reply_text("Ora puoi effettuare modifiche della vetrina")
		except Exception as e:
			update.message.reply_text("Errore. Token ricevuto: " + token)
			print(e)

	def unregister(self, update, context):
		try:
			Dealer_Persistence_Obj = self.Dealer_Handlers_Obj.Shop_Window_Handler_Obj.Dealer_Persistence_Obj
			token = context.args[0]
			Dealer_Persistence_Obj.remove_user_by_token(token)
			update.message.reply_text("I dati relativi a quel token sono stati completamente cancellati")
		except Exception as e:
			update.message.reply_text("Errore. Token ricevuto: " + token)
			print(e)
	
	def pressed(self, update, context):
		query = update.callback_query
		query.answer()
		query.edit_message_text(text="Selected option: {}".format(query.data))
		return int(query.data)

	def register_all_handlers(self, dp):
		dp.add_handler(CommandHandler('start', self.start))

		#####	HANDLERS ONLY FOR TEST
		dp.add_handler(CommandHandler('mod_date', self.allow_mod))
		dp.add_handler(CommandHandler('unregister', self.unregister))
		####

		dp.add_handler(MessageHandler(Filters.status_update, self.start))
		dp.add_handler(self.Dealer_Handlers_Obj.preamble_register_shop_handler())
		
		dp.add_handler(self.Dealer_Handlers_Obj.register_shop_handler())
		dp.add_handler(self.User_Handlers_Obj.register_user_handlers())
		
#		dp.add_handler(self.Dealer_Handlers_Obj.Edit_Shop_Window_Handler_Obj.edit_shop_handler())


		#dp.add_handler(self.Dealer_Handlers_Obj.register_shop_handler_test())	# to merge with the upper line
		

		dp.add_handler(MessageHandler(Filters.text & Filters.group, unknown_function_for_groups))
		dp.add_handler(MessageHandler(Filters.text & (~Filters.group), unknown_function))
		

	def main(self):
		updater = Updater(BOT_TOKEN,  use_context=True, persistence = self.bot_persistence)
		dp = updater.dispatcher

		self.register_all_handlers(dp)
		
		print("In Loop")

		updater.start_polling()
		updater.idle()

if __name__ == '__main__':
	Bot().main()

#except Exception as e:print(str(e))