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

    def dragon_name(self, name: str) -> List[Dict[str, str]]:
        """
        Fetch Dragon data by its name and return its content

        Args:
        name (str): The name of the dragon to retrieve.

        Returns:
        List[Dict[str, Any]]: A list containing the details of the dragon in JSON format (as dictionaries).
        """
        url = f"{self.DRAGONS_API_ENDPOINT}?dragonName={name}"
        headers = {}
        payload = {}
        
        try:
           response = requests.request("GET", url, headers=headers, data=payload, timeout=5)
           content = response.text
           dragon_data = json.loads(content)
           return dragon_data
        
        except requests.HTTPError as err:
            print(f"HTTP Error occured: {err}")


    def dragon_family(self,  family: str) -> List[Dict[str, str]]:
            """
            Fetch Dragon data by its family colour and return all dragon content with similar colour
            
            Args:
            name (str): The name of the dragon to retrieve.

            Returns:
            List[Dict[str, Any]]: A list containing the details of the dragon in JSON format (as dictionaries).
            """
            url = f"{self.DRAGONS_API_ENDPOINT}?family={family}"
            headers = {}
            payload ={}
            
            try:
                response = requests.request("GET", url, headers=headers, data=payload, timeout=5)
                dragon_family = response.text
                return dragon_family
            
            except requests.HTTPError as err:
                 print(f"HTTPError occured: {err}")
                 
    def dragon_list(self):
        """
           
        """
         

if __name__ == '__main__':
     dragon = DragonsAPI()
     print(dragon.dragon_family("black"))
     #print(dragon.dragon_name("Herma"))

