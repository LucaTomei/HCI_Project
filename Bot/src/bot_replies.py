from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, ChatAction, MessageEntity, Bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, PicklePersistence, PrefixHandler, CallbackQueryHandler

import re, os, requests, sys, time, json

from datetime import datetime

from utilities import Utility
from Dealer_Interaction.src import utils
from Dealer_Interaction.src import dealer_persistence


persistence_filename = "bot_persistence"

Utility_Obj = Utility()
Utils_Obj = utils.Utils()
Dealer_Persistence_Obj = dealer_persistence.Dealer_Persistence()

BOT_TOKEN = ""		# t.me/ColligoBot
BOT_DEV_TOKEN = "1140474924:AAEEt2LD6Hg0TRXZDZU7HoHullUtEqNQAPc"	# t.me/Colligo_Development_Bot
#BOT_DEV_TOKEN = "1224954876:AAFKhsKMrWM7qcLaIAWxPiCk4WF1FL_eXtA"

NO_PERSISTENCE_FLAG = False
if NO_PERSISTENCE_FLAG == True and os.path.exists(persistence_filename):	os.remove(persistence_filename)

BOT_TOKEN = BOT_DEV_TOKEN	# Development mode

Bot_Obj = Bot(BOT_TOKEN)

video_tutorials = {
	"first_tutorial":"../files/video/firts_tutorial.mp4",
}

#---------[Some Strings]---------
bot_replies = {
	"main_message": "*Utilizza la tastiera sottostante*",
	"category_message" : "Seleziona a quale categoria appartiene il tuo negozio.(Max 3)\n*[Premere il pulsante Fine per terminare la selezione]*",
	"position_message": "Inviami la posizione(clicca sulla spilla e seleziona *Posizione*, quindi seleziona *Invia posizione corrente*)",

	"category_error_message": "*Inserire almeno una tra le categorie elencate*",
	"registration_error_message": "*Qualcosa è andato storto con la registrazione del tuo negozio\nRicominciamo la registrazione dall'inizio.*",
	"location_error_message" : "Non è stato possibile salvare la posizione del tuo negozio.\nInseriscila manualmente attenendoti al seguente formato: *via*, *CAP*, *città*.\nEsempio: *Via Federico Delpino 23, 00171, Roma*",
	
	"description_message": "*Attraverso i pannelli sottostanti potrai selezionare le categorie che descrivono il tuo negozio e condividere la tua posizione con i clienti.*",
	"dealer_welcome_message": "Benvenuto *%s*  del negozio *%s* sono ColliGo, il bot che ti aiuterà a promuovere la tua attività online.\nHai un sito web del negozio?",

	"catagories_done": "Ecco le categorie che hai impostato\n*%s*",
	"catagory_added": "Categoria *%s* aggiunta con successo.\n*[Premere il pulsante Fine per terminare la selezione]*",
	"category_yes_no": "Sei sicuro di voler aggiungere la categoria *%s*?",

	"location_done": "Posizione Registrata: *[%s, %s]*",
	"website_added": "*Sito Web %s impostato con successo*",
	"insert_website": "*Inserisci il link al tuo sito web*",
	"website_error": "*Il sito %s non rispecchia il classico formato di un sito web: Sei sicuro che il messaggio contenga 'http://'?\nInserisci di nuovo il link al tuo sito web.*",
	"website_not_insert": "*Sito web non inserito.*",

	"all_done": "*Registrazione del negozio completata con successo*:\nCategorie del negozio: *%s*\nPosizione del negozio: *%s*.",

	"no_access_here": "*Mi dispiace ma il bot può essere utilizzato solamente all'interno di gruppi o supergruppi*",



	#---------[After Registration Show Categories]---------
	"choice_your_category": "*Attraverso i pannelli sottostanti potrai selezionare la categoria di prodotti da inserire in vetrina per i tuoi clienti*",
	"choice_your_subcategory": "*Inserisci la sotto-categoria di prodotti*",
	"insert_product": "*Inserisci il prodotto che desideri far visionare ai tuoi clienti*",
	"insert_price": "*Inserisci il prezzo a cui desideri vendere %s di %s*",
	"are_you_sure_price":"*Sei sicuro di voler inserire in vetrina %s a %s€?*",
	"shop_window": "*%s* inserito correttamente nella tua vetrina. Desideri inserire altro o visionare la tua vetrina?",
	"shop_window_done": "*Questa è la vetrina della tua bottega con il riepilogo dei prodotti*:\n\n%s",
	"want_to_send": "*Vuoi che la invio ai tuoi clienti o desideri effettuare ulteriori modifiche?*",

	"shop_window_send": "*La vetrina del tuo negozio è pronta per essere visionata dai tuoi clienti.\nDi seguito ti invio il token di accesso che i tuoi clienti dovranno inserire nella chat privata con ColliGo al fine di poter visualizzare la tua vetrina e cominciare così a creare la propria lista della spesa.*",
	"shop_window_send_token": "*Il token di accesso è il seguente:*\n`%s`",
	"shop_window_send_done": "*Il mio compito per oggi è terminato.\nDomani potrai effettuare nuove modifiche oppure allestire una nuova vetrina per la tua bottega!*",
	"all_done_shopping_window": "*Tutto impostato con successo*",

	"edit_shopping_window": "*Seleziona il prodotto che desideri modificare/eliminare.*",
	"edit_action":"*Hai selezionato %s. Che azione desideri effettuare?*",

	"sure_delete_product": "*Sei sicuro di voler eleminare %s dalla tua vetrina?*",
	"deletion_done": "*Prodotto %s eliminato correttamente*",

	"edit_product_price": "*Modifica ora il prezzo a cui desideri vendere %s di %s oppure clicca il bottone sottostante per annullare l'operazione.*", # %(size, product_name)
	"sure_edit_price": "*Sei sicuro di voler inserire in vetrina %s al prezzo di %s€?*",
	"edit_product_price_done": "*Prodotto modificato correttamente.*",


	"cart_successfully_created":"*%s ti informo che '%s' ha completato la creazione della tua lista della spesa, pertanto ti invito a ritirarla al più presto.\n%s\nIl costo complessivo è pari a %s€.*",


	#---------[Customer Replies]---------
	#"pre_insert_token": "*Ciao %s, per visualizzare la vetrina del tuo negoziante di fiducia, utilizza la tastiera sottostante per inserire il token fornito dal gruppo del negoziante*",
	#"insert_token": "*Ciao %s, per visualizzare la vetrina del tuo negoziante di fiducia, per favore inserisci il Token di accesso fornito nel gruppo del negozio.*",
	

	"insert_token": "Ciao *%s*, questo è l'elenco dei *negozi registrati*:\n%s",
	


	#"copy_token": "*Copia il token del negozio mostrato nella lista precedente ed incollalo per iniziare ad acquistare prodotti dalla bottega selezionata.*",
	"want_to_buy":"*Desideri acquistare presso uno dei seguenti venditori?*",
	"show_shops":"*La tastiera sottostante mostra tutti i negozi registrati a ColliGo. Se ne conosci uno selezionalo per iniziare a fare la spesa.*",

	"no_dont_buy":"*Mi dispiace che hai deciso di non acquistare nessun prodotto. Qui troverai comunque l'elenco dei negozi registrati.*",

	"shop_window_customer":"Questa è la vetrina della bottega *'%s'*, situata in *%s* con il riepilogo dei prodotti:\n*%s*",
	"show_shopping_window_customer":"*Vuoi aggiungere prodotti al tuo carrello oppure visualizzare il suo contenuto?*",
	"empty_shopping_cart":"*Il tuo carrello è attualmente vuoto.\n\nÈ il momento di comprare qualcosa.*",
	"show_shopping_window_buttons": "*La vetrina del negozio %s è riportata di seguito. Scegli i prodotti che desideri acquistare e conferma di volerli inserire nel carrello.*",
	"add_product_shopping_cart":"*Il costo di %s di %s è pari a %s€*",
	"sure_add_product_cart": "*Sei sicuro di voler aggiungere questo prodotto al tuo carrello o desideri selezionarne un altro?*",
	"add_to_cart_done": "*Prodotto inserito correttamente nel tuo carrello.\nVuoi continuare ad inserire prodotti o vedere il contenuto del tuo carrello?*",


	"cart_content":"*Questo è il contenuto del tuo carrello:\n%s\n\nIl costo complessivo è pari a: %s€*",
	"process_checkout":"*Desideri andare alla cassa o aggiungere altri prodotti?*",

	"checkout_main":"*Prima di inviare la tua lista della spesa al negozio '%s', controlla che tu non abbia scordato nulla.\n\nVuoi eliminare alcuni prodotti dal tuo carrello o desideri procedere all'invio della lista della spesa?*",

	"delete_product":"*Seleziona il prodotto che desideri eliminare dal tuo carrello*",
	"sure_delete_product_in_cart": "*Sei sicuro di voler eliminare %s di %s?*",
	"delete_product_success": "*Prodotto correttamente eliminato dal tuo carrello*",

	"arrived_new_shopping_cart":"*È arrivata una nuova lista della spesa dal cliente %s.\n%s\nIl costo complessivo è pari a: %s€*",

	"send_shopping_cart_done": "*Lista della spesa inviata con successo*",



	#---------[Editing shopping window]--------
	"edit_old_shopping_window": "*Questa è l'ultima vetrina che hai inserito:\n%s\n\nDesideri modificarla?*",
	"what_do_you_want": "Cosa desideri effettuare?",
	"choice_your_category_edit": "*Attraverso i pannelli sottostanti potrai selezionare la categoria di prodotti per effettuare una modifica sulla tua vetrina.*",

	"first_tutorial":"*Se desideri ricevere un video tutorial su come effettuare la registrazione del tuo negozio clicca il seguente bottone*",
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
	"no_show_shop_window": "Fine - vedi la vetrina",

	#---------[Message: shop_window_done]---------
	"yes_send_shop_window": "Si - Invia ai clienti",
	"no_send_shop_window": "No - Modifica i Prodotti",

	#---------[Message: edit_action]---------
	"delete_product":"Eliminare il Prodotto",
	"edit_product_price": "Modificare il prezzo",

	"sure_delete_product": "Si - Elimina il Prodotto",
	"not_sure_delete_product": "No - Torna alla Vetrina",

	"yes_edit_price": "Si - Modifica il Prezzo",

	"back_button":"🔙Indietro🔙",


	#---------[Customer Buttons]---------
	"insert_token": "Inserisci il Token",

	"add_product": "Aggiungi un prodotto",
	"show_shopping_cart": "Visualizza il carrello",

	"add_product_done": "Aggiungi",
	"select_other_product": "Seleziona un altro prodotto",

	"add_other_products": "Aggiungi altri prodotti",

	"checkout": "Cassa",
	"add_again":"Aggiungi ancora",

	"delete_product":"Elimina prodotto",
	"send_shopping_cart": "Invia lista della spesa",


	#---------[New Buttons - Editing shopping window]---------
	"edit_shopping_window":"Modifica la vetrina",
	
	"add_some_products": "Inserisci nuovi prodotti",
	"delete_some_products":"Elimina i prodotti",
	"edit_shopping_window_prices": "Modifica i prezzi",

	#---------[New Buttons - Pre Customer Shopping]---------
	"want_to_buy_yes": "SI - Mostra i Negozi",
	"want_to_buy_no": "NO - Aggiorna lista Negozi",
	"update_shop_list": "Aggiorna Lista"
}

def makeAKeyboard(alist, parti):
    length = len(alist)
    keyboard =  [alist[i*length // parti: (i+1)*length // parti] for i in range(parti)]
    keyboard.append([bot_buttons['stop_button']])
    return ReplyKeyboardMarkup(keyboard)

def make_keyboard(alist, parti):
    length = len(alist)
    keyboard =  [alist[i*length // parti: (i+1)*length // parti] for i in range(parti)]
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

def make_upper_end_back_keyboard(alist, parti): 
   	length = len(alist)
   	keyboard = []
   	keyboard.append([bot_buttons['back_button']])
   	keyboard =  keyboard + [alist[i*length // parti: (i+1)*length // parti] for i in range(parti)]
   	keyboard.append([bot_buttons['stop_button']])
   	return ReplyKeyboardMarkup(keyboard)


#---------[New Keyboard - Editing shopping window]---------
edit_shopping_window_keyboard = ReplyKeyboardMarkup([
	[bot_buttons['edit_shopping_window']],
	[bot_buttons['stop_button']]
])

edit_shopping_window_execute_keyboard = ReplyKeyboardMarkup([
	[bot_buttons['add_some_products']],
	[bot_buttons['delete_some_products']],
	[bot_buttons['edit_shopping_window_prices']],
	[bot_buttons['back_button']]
])


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
], one_time_keyboard = True, resize_keyboard = True)

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
], one_time_keyboard = True, resize_keyboard = True)

yes_no_categories_keyboard = ReplyKeyboardMarkup([
	[bot_buttons['yes_category']],
	[bot_buttons['no_category']]
])

want_to_buy_keyboard = ReplyKeyboardMarkup([
	[bot_buttons['want_to_buy_yes']],
	[bot_buttons['want_to_buy_no']]
])

update_shop_list_keyboard = ReplyKeyboardMarkup([
	[bot_buttons['update_shop_list']]
])


categories_names_list = Utility_Obj.get_all_merchant_categories()	# Contains all categories names


categories_keyboard = makeAKeyboard(categories_names_list, 5)



def deleteMessages(context):
	chat_id, messages_to_delete = context.job.context
	for message_id in messages_to_delete:
		try:	context.bot.delete_message(chat_id=chat_id, message_id=message_id)
		except Exception as e:	continue


def automatize_message(context):
	chat_id, my_name, merchant_name, formatted_cart, total = context.job.context

	message = bot_replies['cart_successfully_created'] %(my_name, merchant_name, formatted_cart, total)
	context.bot.send_message(chat_id=chat_id, text = message,  parse_mode = ParseMode.MARKDOWN)

def unknown_function_for_groups(update, context):
	try:
		chat_id = update.message.chat_id
		first_name = update.message.chat.first_name
		first_name = first_name if first_name != None else update.message.from_user.first_name
		group_title = update.message.chat.title
		

		
		Utility_Obj.set_user_data(chat_id, context, main_keyboard, group_title)
		Utility_Obj.append_messages_to_delete(chat_id, context, update.message.message_id)
		telegram_link = Utility_Obj.set_telegram_link(update, context)
		

		group_token = Utils_Obj.make_token(chat_id)
		if not Utility_Obj.check_if_user_has_done(chat_id, context):
			if Dealer_Persistence_Obj.is_token_in_persistence(group_token):
				if Dealer_Persistence_Obj.get_shopping_window_date_day_by_token(group_token) == datetime.now().day:
					message = bot_replies['all_done_shopping_window']
					keyboard = ReplyKeyboardRemove()
				else:
					old_shopping_window = Dealer_Persistence_Obj.get_shopping_window_by_token(group_token)
					old_shopping_window_str = Utility_Obj.format_shopping_window(old_shopping_window)
					message = bot_replies['edit_old_shopping_window'] % old_shopping_window_str #bot_replies['main_message']
					keyboard = edit_shopping_window_keyboard#Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context)
					Utility_Obj.set_main_keyboard_by_chat_id(chat_id, keyboard, context)
				


				reply_message = update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard)
				Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)

				
				if message == bot_replies['all_done_shopping_window']:
					job = context.job_queue.run_once(deleteMessages, 1, context=update.message)
					messages_to_delete = Utility_Obj.get_messages_to_delete(chat_id, context)
					job.context = (chat_id, messages_to_delete)
					Utility_Obj.reset_messages_to_delete(chat_id, context)
				return ConversationHandler.END
			else:	#if dealer is not in persistence file
				keyboard = Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context)
				message = bot_replies['main_message']

				reply_message = update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard)
				Utility_Obj.append_messages_to_delete(chat_id, context, reply_message.message_id)
				return ConversationHandler.END
	except Exception as e:	print("unknown_function_for_groups:", str(e))





