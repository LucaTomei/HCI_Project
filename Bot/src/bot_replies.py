from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, ChatAction, MessageEntity, Bot
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, PicklePersistence, PrefixHandler, CallbackQueryHandler

import re, os, requests, sys, time, json

from datetime import datetime

from utilities import Utility
from Dealer_Interaction.src import utils
from Dealer_Interaction.src import dealer_persistence

Utility_Obj = Utility()
Utils_Obj = utils.Utils()
Dealer_Persistence_Obj = dealer_persistence.Dealer_Persistence()

BOT_TOKEN = ""		# t.me/ColligoBot
BOT_DEV_TOKEN = "1140474924:AAEEt2LD6Hg0TRXZDZU7HoHullUtEqNQAPc"	# t.me/Colligo_Development_Bot


BOT_TOKEN = BOT_DEV_TOKEN	# Development mode

Bot_Obj = Bot(BOT_TOKEN)

#---------[Some Strings]---------
bot_replies = {
	"main_message": "*Utilizza la tastiera sottostante*",
	"category_message" : "Seleziona a quale categoria appartiene il tuo negozio.(Max 3)\n*[Premere il pulsante Fine per terminare la selezione]*",
	"position_message": "Inviami la posizione(clicca sulla spilla e seleziona *Posizione*, quindi seleziona *Invia posizione corrente*)",

	"category_error_message": "*Inserire almeno una tra le categorie elencate*",
	"registration_error_message": "*Qualcosa è andato storto con la registrazione del tuo negozio\nRicominciamo la registrazione dall'inizio.*",
	"location_error_message" : "Non è stato possibile salvare la posizione del tuo negozio.\nInseriscila manualmente attenendoti al seguente formato: *via*, *CAP*, *città*.\nEsempio: *Via corcolle 30, 00131, Roma*",
	
	"description_message": "*Attraverso i pannelli sottostanti potrai selezionare le categorie che descrivono il tuo negozio e condividere la tua posizione con i clienti.*",
	"dealer_welcome_message": "Benvenuto *%s*  del negozio *%s* sono ColliGo, il bot che ti accompagnerà nella vendita online della tua attività.\nHai un sito web del negozio?",

	"catagories_done": "Ecco le categorie che hai impostato\n*%s*",
	"catagory_added": "Categoria *%s* aggiunta con successo.\n*[Premere il pulsante Fine per terminare la selezione]*",
	"category_yes_no": "Sei sicuro di voler aggiungere la categoria *%s*?",

	"location_done": "Posizione Registrata: *[%s, %s]*",
	"website_added": "*Sito Web %s impostato con successo*",
	"insert_website": "*Inserisci il link al tuo sito web*",
	"website_error": "*Il sito %s non rispecchia lo schema di un sito web: Sei sicuro che il messaggio contenga 'http://'?\nInserisci di nuovo il link al tuo sito web [q per uscire].*",
	"website_not_insert": "*Sito web non inserito.*",

	"all_done": "Tutto impostato con successo:\nCategorie del negozio: *%s*\nPosizione del negozio: *%s*.",

	"no_access_here": "*Mi dispiace ma il bot può essere utilizzato solamente all'interno di gruppi o supergruppi*",



	#---------[After Registration Show Categories]---------
	"choice_your_category": "*Attraverso i pannelli sottostanti potrai selezionare la categoria di prodotti da inserire in vetrina per i tuoi clienti*",
	"choice_your_subcategory": "*Inserisci ora la sotto-categoria di prodotti*",
	"insert_product": "*Inserisci ora il prodotto che desideri far visionare ai tuoi clienti*",
	"insert_price": "*Inserisci ora il prezzo a cui desideri vendere %s di %s*",
	"are_you_sure_price":"*Sei sicuro di voler vendere %s a %s€?*",
	"shop_window": "*%s* inserito correttamente nella tua vetrina. Desideri inserire altro o visionare la tua vetrina?",
	"shop_window_done": "Questa è la vetrina della tua bottega con il riepilogo dei prodotti:\n\n%s",
	"want_to_send": "*Vuoi che la invio ai tuoi clienti o desideri apportare ulteriori modifiche?*",

	"shop_window_send": "*La vetrina del tuo negozio è stata inoltrata correttamente a tutti i tuoi clienti.\nDi seguito ti invio il token di accesso che i tuoi clienti dovranno inserire nella chat privata con ColliGo al fine di poter visualizzare la tua vetrina e cominciare così a creare la propria lista della spesa.*",
	"shop_window_send_token": "*Il token di accesso è il seguente:*\n```%s```",
	"shop_window_send_done": "*Il mio compito per oggi è terminato.\nDomani potrai effettuare nuove modifiche oppure allestire una nuova vetrina per la tua bottega!*",
	"all_done_shopping_window": "*Tutto impostato con successo*",

	"edit_shopping_window": "*Seleziona il prodotto che desideri modificare/eliminare.*",
	"edit_action":"*Hai selezionato %s. Che azione desideri effettuare?*",

	"sure_delete_product": "*Sei sicuro di voler eleminare %s dalla tua vetrina?*",
	"deletion_done": "*Prodotto %s eliminato correttamente*",

	"edit_product_price": "*Modifica ora il prezzo a cui desideri vendere %s di %s*", # %(size, product_name)
	"sure_edit_price": "*Sei sicuro di voler inserire %s al prezzo di %s€?*",
	"edit_product_price_done": "*Prodotto modificato correttamente.*",



	#---------[Customer Replies]---------
	#"pre_insert_token": "*Ciao %s, per visualizzare la vetrina del tuo negoziante di fiducia, utilizza la tastiera sottostante per inserire il token fornito dal gruppo del negoziante*",
	"insert_token": "*Ciao %s, per visualizzare la vetrina del tuo negoziante di fiducia, per favore inserisci il Token di accesso fornito nel gruppo del negozio.*",
	"shop_window_customer":"*Questa è la vetrina della bottega %s con il riepilogo dei prodotti:\n%s*",
	"show_shopping_window_customer":"*Vuoi aggiungere prodotti al tuo carrello oppure visualizzare il suo contenuto?*",
	"empty_shopping_cart":"*Il tuo carrello è attualmente vuoto.\n\nÈ il momento di fare la spesa*",
	"show_shopping_window_buttons": "*La vetrina del negozio %s è riportata di seguito. Scegli i prodotti che desideri acquistare e conferma di volerli inserire nel carrello.*",
	"add_product_shopping_cart":"*Il costo di %s di %s è pari a %s€*",
	"sure_add_product_cart": "*Sei sicuro di voler aggiungere questo prodotto al tuo carrello o desideri selezionare un altro prodotto?*",
	"add_to_cart_done": "*Prodotto inserito correttamente nel tuo carrello.\nVuoi continuare ad inserire prodotti o visionare cosa contiene il tuo carrello?*",


	"cart_content":"*Questo è il contenuto del tuo carrello:\n\n%s\n\nIl costo complessivo è pari a: %s€*",
	"process_checkout":"*Vuoi procedere al checkout o aggiungere altri prodotti?*",

	"checkout_main":"*Prima di inviare la tua lista della spesa al negozio %s, controlla che ci sia tutto.\n\nVuoi eliminare alcuni prodotti dal tuo carrello della spesa o desideri procedere all'invio della lista della spesa?*",

	"delete_product":"*Seleziona il prodotto che desideri eliminare dal tuo carrello*",
	"sure_delete_product_in_cart": "*Sei sicuro di voler eliminare %s di %s?*",
	"delete_product_success": "*Prodotto correttamente eliminato dal tuo carrello*",

	"arrived_new_shopping_cart":"*È arrivata una nuova lista della spesa dal cliente %s.*",
	"show_shopping_cart": "*%s\n\nIl costo complessivo è pari a: %s€*",
}

#---------[Keyboard Buttons]---------
bot_buttons = {
	"category": "🥐 Categoria 🍷",
	"location": "📍 Posizione 📍",

	"yes": "👍 SI 👍",
	"no": "👎 NO 👎",

	"yes_category": "SI 👍",
	"no_category": "NO 👎",

	"stop_button": "Fine",

	#---------[Message: insert_price]---------
	"yes_sure_price": "SI👍",
	"no_sure_price": "NO👎",

	#---------[Message: shop_window]---------
	"yes_insert_new_product": "Inserisci nuovo prodotto",
	"no_show_shop_window": "Fine - vedi vetrina",

	#---------[Message: shop_window_done]---------
	"yes_send_shop_window": "SI - Invia ai clienti",
	"no_send_shop_window": "NO - Modifica Prodotti",

	#---------[Message: edit_action]---------
	"delete_product":"Eliminare il Prodotto",
	"edit_product_price": "Modificare il Prezzo",

	"sure_delete_product": "Si - Elimina Prodotto",
	"not_sure_delete_product": "No - Torna a Vetrina",

	"yes_edit_price": "Si - Modifica Prezzo",

	"back_button":"🔙Indietro🔙",


	#---------[Customer Buttons]---------
	"insert_token": "Inserisci il Token",

	"add_product": "AGGIUNGI PRODOTTO",
	"show_shopping_cart": "VISUALIZZA CARRELLO",

	"add_product_done": "AGGIUNGI",
	"select_other_product": "SELEZIONA UN ALTRO PRODOTTO",

	"add_other_products": "AGGIUNGI ALTRI PRODOTTI",

	"checkout": "CHECKOUT",
	"add_again":"AGGIUNGI ANCORA",

	"delete_product":"ELIMINA PRODOTTO",
	"send_shopping_cart": "INVIA LISTA DELLA SPESA",
}

def makeAKeyboard(alist, parti):
    length = len(alist)
    keyboard =  [alist[i*length // parti: (i+1)*length // parti] for i in range(parti)]
    keyboard.append([bot_buttons['stop_button']])
    return ReplyKeyboardMarkup(keyboard)


def make_back_keyboard(alist, parti):
	length = len(alist)
	keyboard =  [alist[i*length // parti: (i+1)*length // parti] for i in range(parti)]
	keyboard.append([bot_buttons['back_button']])
	return ReplyKeyboardMarkup(keyboard)

def make_upper_back_keyboard(alist, parti): 
   	length = len(alist)
   	keyboard = []
   	keyboard.append([bot_buttons['back_button']])
   	keyboard =  keyboard + [alist[i*length // parti: (i+1)*length // parti] for i in range(parti)]
   	return ReplyKeyboardMarkup(keyboard)


#---------[Customer Keyboard]---------

delete_product_or_back_keyboard = make_back_keyboard([bot_buttons['delete_product']],2)

delete_or_send_keyboard = ReplyKeyboardMarkup([
	[bot_buttons['delete_product']],
	[bot_buttons['send_shopping_cart']]
])

checkout_or_add_adain_keyboard = ReplyKeyboardMarkup([
	[bot_buttons['checkout']],
	[bot_buttons['add_again']]
])

add_or_show_shopping_cart = ReplyKeyboardMarkup([
	[bot_buttons['add_other_products']],
	[bot_buttons['show_shopping_cart']]
])

add_or_select_other_product_keyboard = ReplyKeyboardMarkup([
	[bot_buttons['add_product_done']],
	[bot_buttons['select_other_product']]
])

insert_token_keyboard = ReplyKeyboardMarkup([
	[bot_buttons['insert_token']],
	[bot_buttons['stop_button']]
])

add_product_show_shopping_cart_keyboard = ReplyKeyboardMarkup([
	[bot_buttons['add_product']],
	[bot_buttons['show_shopping_cart']]
])



#---------[Dealer Keyboard]---------
edit_product_price_keyboard = ReplyKeyboardMarkup([
	[bot_buttons['yes_edit_price']],
	[bot_buttons['not_sure_delete_product']]
])

delete_product_sure_keyboard = ReplyKeyboardMarkup([
	[bot_buttons['sure_delete_product']],
	[bot_buttons['not_sure_delete_product']]
])

delete_edit_keyboard = ReplyKeyboardMarkup([
	[bot_buttons['edit_product_price']],
	[bot_buttons['delete_product']]
])

send_shop_window_keyboard = ReplyKeyboardMarkup([
	[bot_buttons['yes_send_shop_window']],
	[bot_buttons['no_send_shop_window']]
])

other_product_main_keyboard = ReplyKeyboardMarkup([
	[bot_buttons['yes_insert_new_product']],
	[bot_buttons['no_show_shop_window']]
])

yes_no_sure_price = ReplyKeyboardMarkup([
	[bot_buttons['yes_sure_price']],
	[bot_buttons['no_sure_price']]
])

main_keyboard = ReplyKeyboardMarkup([
	[bot_buttons['category']],
	[bot_buttons['location']]
])

main_keyboard_only_location = ReplyKeyboardMarkup([
	[bot_buttons['location']]
])

main_keyboard_only_categories = ReplyKeyboardMarkup([
	[bot_buttons['category']]
])

main_keyboard_empty = ReplyKeyboardRemove()

yes_no_keyboard = ReplyKeyboardMarkup([
	[bot_buttons['yes']],
	[bot_buttons['no']]
])

yes_no_categories_keyboard = ReplyKeyboardMarkup([
	[bot_buttons['yes_category']],
	[bot_buttons['no_category']]
])

categories_names_list = Utility_Obj.get_all_merchant_categories()	# Contains all categories names


categories_keyboard = makeAKeyboard(categories_names_list, 5)

#---------[Useful Functions]---------
def unknown_function(update, context):
	try:
		chat_id = update.message.chat_id
		first_name = update.message.chat.first_name
		first_name = first_name if first_name != None else update.message.from_user.first_name
		group_title = update.message.chat.title
		Utility_Obj.set_user_data(chat_id, context, main_keyboard, group_title)
		#print("has_done", Utility_Obj.check_if_user_has_done(chat_id, context))
		if not Utility_Obj.check_if_user_has_done(chat_id, context):
			if 'group' in update.message.chat.type:
				telegram_link = Utility_Obj.set_telegram_link(update, context)
				# Verify if is passed a day
				group_token = Utils_Obj.make_token(chat_id)
				#group_token = group_token.replace('=', "god")	# @ForTest
				#print(Dealer_Persistence_Obj.is_token_in_persistence(group_token))
				if Dealer_Persistence_Obj.is_token_in_persistence(group_token):
					if Dealer_Persistence_Obj.get_shopping_window_date_day_by_token(group_token) == datetime.now().day:
						message = bot_replies['all_done_shopping_window']
						keyboard = ReplyKeyboardRemove()
					else:
						message = bot_replies['main_message']
						keyboard = Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context)
					context.bot.send_message(chat_id=chat_id, text = message, reply_markup=keyboard,  parse_mode = ParseMode.MARKDOWN)
				else:	#if dealer is not in persistence file
					keyboard = Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context)
					message = bot_replies['main_message']
					context.bot.send_message(chat_id=chat_id, text = message, reply_markup=keyboard,  parse_mode = ParseMode.MARKDOWN)
					
			else:	# if i'm an User and not a customer
				
				context.bot.send_message(chat_id=chat_id, text = bot_replies['insert_token'] % first_name, reply_markup=ReplyKeyboardRemove(),  parse_mode = ParseMode.MARKDOWN)
			
			return ConversationHandler.END
		else:
			return ConversationHandler.END
	except Exception as e:	print(str(e))
