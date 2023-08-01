
import requests

if __name__ == "__main__":
	print("You are meant to import this module, not run it directly.")
	exit()

class URLs:
	MESSAGING_SERVICE_API = "https://apis.roblox.com/messaging-service/v1/universes/{}/topics/{}"

class API_Key:
	# api key value
	KEY = None
	# group id or user id that owns this api-key
	CREATOR_ID = None

	def __str__(self) -> str:
		return f"API_KEY:\nKey: {self.KEY}\nCreatorId: {self.CREATOR_ID}"

	def __init__(self, KEY=None, CREATOR_ID=None):
		self.KEY = KEY
		self.CREATOR_ID = CREATOR_ID

class _RequestWrapper:

	@staticmethod
	def get( key : API_Key, url : str, *args, **kwargs ) -> requests.Response | Exception:
		try:
			return requests.get(
				url,
				headers={ "x-api-key" : key.API_KEY },
				*args, **kwargs
			)
		except Exception as exception:
			return exception

	@staticmethod
	def post( key : API_Key, url : str, *args, **kwargs ) -> requests.Response | Exception:
		try:
			return requests.post(
				url,
				headers={ "x-api-key" : key.KEY },
				*args, **kwargs
			)
		except Exception as exception:
			return exception

class MessagingServiceAPI:

	@staticmethod
	def publish_message( account : API_Key, universeId : int, topic : str, message : str ) -> requests.Response | Exception:
		try:
			return _RequestWrapper.post(
				account,
				URLs.MESSAGING_SERVICE_API.format(universeId, topic),
				json = {'message' : message}
			).json()
		except Exception as exception:
			return exception

class DatastoreAPI:
	pass

class AssetsAPI:
	pass
