import json
from datetime import datetime
class Dealer_Persistence(object):
	def __init__(self):
		try:
			self.persistence_filename = "Dealer_Interaction/src/files/dealer_persistence.json"
			self.read_persistence()
		except:	self.persistence_filename = "files/dealer_persistence.json"	#<--- only for test and __main__

	
	def write_persistence(self, content):
		file = open(self.persistence_filename, 'w')
		json.dump(content, file,indent=4)
		file.close()
	
	def read_persistence(self):
		file = open(self.persistence_filename)
		content = json.load(file)
		file.close()
		return content

	def append_dealer_persistence(self, dealer_token, dealer_infos):
		content = self.read_persistence()
		content[dealer_token] = dealer_infos

		self.write_persistence(content)

	def format_datetime(self, datetime_obj):
		return datetime_obj.strftime("%d/%m/%YCOLLIGO%H:%M")	#"12/05/2020COLLIGO18:53"

	def is_token_in_persistence(self, token):
		content = self.read_persistence()
		return token in content

	def get_shopping_window_date_day_by_token(self, token):
		content = self.read_persistence()
		return int(content[token]['shopping_window_date'].split('/')[0])


if __name__ == '__main__':
	Dealer_Persistence_Obj = Dealer_Persistence()
	print(Dealer_Persistence_Obj.read_persistence())

	dealer_token = "eJzTNTQwMDQ0M7W0NDA0MAYAFHACwg=="
	dealer_infos = {
		"shopping_window_list":[{'name': 'Nepi', 'price': 10.0, 'units':'1.5L'}],
		"shopping_window_date": Dealer_Persistence_Obj.format_datetime(datetime(2020, 5, 12, 18, 53, 48, 314241))
	}

	Dealer_Persistence_Obj.append_dealer_persistence(dealer_token, dealer_infos)
	print(Dealer_Persistence_Obj.read_persistence())
