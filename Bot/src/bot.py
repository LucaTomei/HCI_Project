from bot_replies import *

from Dealer_Interaction.src import dealer_handlers


class Bot(object):
	def __init__(self):
		self.Dealer_Handlers_Obj = dealer_handlers.Dealer_Handlers()


	def start(self, update, context):
		chat_id = update.message.chat_id
		group_title = update.message.chat.title
		Utility_Obj.set_user_data(chat_id, context, main_keyboard, group_title)
		Utility_Obj.set_telegram_link(update, context)
		first_name = update.message.chat.first_name
		first_name = first_name if first_name != None else update.message.from_user.first_name
		if 'group' in update.message.chat.type:
			context.bot.send_message(chat_id=update.effective_chat.id, text = bot_replies['dealer_welcome_message'] % (first_name, group_title), reply_markup=yes_no_keyboard,  parse_mode = ParseMode.MARKDOWN)
		else:
			context.bot.send_message(chat_id=update.effective_chat.id, text = bot_replies['no_access_here'], reply_markup=ReplyKeyboardRemove(),  parse_mode = ParseMode.MARKDOWN)
		

	
	def register_all_handlers(self, dp):
		dp.add_handler(CommandHandler('start', self.start))
		dp.add_handler(MessageHandler(Filters.status_update, self.start))
		#dp.add_handler(self.Dealer_Handlers_Obj.preamble_register_shop_handler())
		#dp.add_handler(self.Dealer_Handlers_Obj.register_shop_handler())
		dp.add_handler(self.Dealer_Handlers_Obj.register_shop_handler_test())
		#dp.add_handler(self.Dealer_Handlers_Obj.register_shop_window_handler())
		dp.add_handler(MessageHandler(Filters.text, unknown_function))

	def main(self):
		updater = Updater(BOT_TOKEN,  use_context=True)
		dp = updater.dispatcher

		self.register_all_handlers(dp)
		
		print("In Loop")
		updater.start_polling()
		updater.idle()

if __name__ == '__main__':
	Bot().main()

#except Exception as e:print(str(e))