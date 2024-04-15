"""
In this module We use the requests library to intract with the dragon API deployed using AWS gatewaty
"""

import json
import requests
from typing import List, Dict, Any


class DragonsAPI:
	"""
	This class provides the GET and POST requests for interacting 
	with the dragon API
	"""

	DRAGONS_API_ENDPOINT = "https://tqibofk44h.execute-api.ap-northeast-3.amazonaws.com/testing/dragons"
	def __init__(self):
		pass


	def dragon_name(self, name:str) -> List[Dict[str, str]]:
		"""
		Fetch Dragon by its name and return its content 

		Args:
        name (str): The name of the dragon to retrieve.

        Returns:
        List[Dict[str, Any]]: A list containing the details of the dragon in JSON format (as dictionaries).
        """
		try:
			response = requests.get(f"{self.DRAGONS_API_ENDPOINT}?dragonName={name}", timeout=5)
			response.raise_for_status()
			data = response.content.decode('UTF-8')
			dragon_data = json.loads(data)
			return dragon_data
		except requests.HTTPError as err:
			print("HTTP Error occured: {err}")


	# def list_dragons(self):
	# 	try:
	# 		response = requests.get(self.DRAGONS_API_ENDPOINT, timeout=5)
	# 		response.raise_for_status()
	# 		data = response.content.decode('UTF-8')
	# 		dragons_list = json.loads(data)
	# 		return dragons_list
		
	# 	except requests.HTTPError as err:
	# 		print(f"HTTP Error Occured: {err}")
 



dragon = DragonsAPI()
print(dragon.dragon_name("Herma"))

