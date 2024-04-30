"""
In this module We use the requests library to intract with the dragon API deployed using AWS gateway
"""

from typing import List, Dict, Any
import requests
import os 
import json


class DragonsAPI:
    """
    This class provides the GET and POST requests for interacting
    with the dragon API
    """

    DRAGONS_API_ENDPOINT = "https://tqibofk44h.execute-api.ap-northeast-3.amazonaws.com/testing/dragons"
   
    authorisation_token = os.getenv('DRAGON_API_TOKEN')

    def __init__(self):
        pass

    def dragon_name(self, name: str) -> List[Dict[str, str]]:
        """
        Fetch Dragon data by its name and return its content

        Args:
        name (str): The name of the dragon to retrieve.

        Returns:
        List[Dict[str, Any]]: A list containing the details of the dragon in string format (as dictionaries).
        """
        url = f"{self.DRAGONS_API_ENDPOINT}?dragonName={name}"
        headers = {
            'Authorization': self.authorisation_token,
            'Content-Type': 'application/json'
        }
        payload = {}

        try:
            response = requests.request(
                "GET", url, headers=headers, data=payload, timeout=5)
            dragon_data = response.text
            return dragon_data

        except requests.HTTPError as err:
            print(f"HTTP Error occured: {err}")

    def dragon_family(self, family: str) -> List[Dict[str, str]]:
        """
        Fetch Dragon data by its family colour and return all dragon content with similar colour

        Args:
        name (str): The name of the dragon to retrieve.

        Returns:
        List[Dict[str, Any]]: A list containing the details of the dragon in string format (as dictionaries).
        """
        url = f"{self.DRAGONS_API_ENDPOINT}?family={family}"
        headers = {
            'Authorization': self.authorisation_token,
            'Content-Type': 'application/json'
        }
        payload = {}

        try:
            response = requests.request(
                "GET", url, headers=headers, data=payload, timeout=5)
            dragon_family = response.text
            return dragon_family

        except requests.HTTPError as err:
            print(f"HTTPError occured: {err}")

    def dragon_list(self):
        """
        Fetch all dragon content data

        Args:
        None

        Returns:
        List[Dict[str, Any]]: A list containing the details of all the dragon in string format (as dictionaries).
        """

        url = self.DRAGONS_API_ENDPOINT
        headers = {
            'Authorization': self.authorisation_token,
            'Content-Type': 'application/json'
        }
        payload = {}

        try:
            response = requests.request(
                "GET", url, headers=headers, data=payload, timeout=5)
            dragon_list = response.text
            return dragon_list

        except requests.HTTPError as err:
            print(f"An HTTPError occured: {err}")


    def create_dragon(self, dragon_attributes: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new dragon entry in the API.

        Args:
            dragon_attributes (Dict[str, Any]): The attributes of the dragon to create.

        Returns:
            Dict[str, Any]: The response from the API after creating the dragon.

        Raises:
            requests.HTTPError: An error occurred while making the HTTP request.
        """

        url = "https://tqibofk44h.execute-api.ap-northeast-3.amazonaws.com/testing/dragons"

        if not dragon_attributes:
            payload = json.dumps(dragon_attributes)
        else:
            payload = json.dumps({
        "description_str": "George is a new dragon, we don't know much about them yet.",
        "dragon_name_str": "George",
        "family_str": "green",
        "location_city_str": "seattle",
        "location_country_str": "usa",
        "location_neighborhood_str": "4th st",
        "location_state_str": "washington"
        })


        headers = {
            'Authorization': self.authorisation_token,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.request(
                "POST", url, headers=headers, data=payload, timeout=5)
            response.raise_for_status()
            return response.status_code()
        
        except requests.HTTPError as err:
            print(f"HTTP Error occurred: {err}")
            return {'error': str(err)}

if __name__ == '__main__':
    dragon = DragonsAPI()
    # print(dragon.dragon_family("black"))
    # print(dragon.dragon_name("Herma"))
    # print(dragon.dragon_list())
    print(dragon.create_dragon(None))
