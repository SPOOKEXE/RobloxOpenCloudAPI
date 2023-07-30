
from os import path as os_path
from requests import Response
from requests import get as requests_get, post as requests_post
from enum import Enum
from typing import Any
from json import dumps as json_dumps
from io import TextIOWrapper

def get_blurred_value( value : str, visible=6 ) -> str:
	assert type(value) == str, "Passed parameter must be a string."
	return value[:visible] + ("*" * (len(value) - visible))

class URLS(Enum):
	FIND_DECAL_IMAGE_ID = "https://f3xteam.com/bt/getDecalImageID/{}"
	FIND_MESH_RAW_ID = "https://f3xteam.com/bt/getFirstMeshData/{}"

	OPERATIONS_STATUS_API = "https://apis.roblox.com/assets/v1/operations/{}"
	ROBLOX_ASSETS_API = "https://apis.roblox.com/assets/v1/assets"

class AssetTypes(Enum):
	Model = "Model"
	Decal = "Decal"
	Audio = "Audio"

class OperationStatus(Enum):
	Success = 1
	Moderated = 2
	Waiting = 3
	Unavailable = 4
	Exception = 5

class API_Key:
	# api key value
	API_KEY = None
	# group id or user id that owns this api-key
	CREATOR_ID = None

	def __str__(self) -> str:
		return f"API_KEY\nAPI_Key: {get_blurred_value(self.API_KEY)}\nCreatorId: {self.CREATOR_ID}"

	def __init__(self, API_KEY=None, CREATOR_ID=None):
		self.API_KEY = API_KEY
		self.CREATOR_ID = CREATOR_ID

class Asset:
	Name = None
	AssetType = None
	Filepath = None

	def __init__( self, name : str, asset_type : AssetTypes, filepath : str ):
		self.Name = name
		self.AssetType = asset_type
		self.Filepath = filepath

class Requests:

	@staticmethod
	def get( key : API_Key, url : str, *args, **kwargs ) -> Response | Exception:
		try:
			return requests_get(
				url,
				headers={ "x-api-key" : key.API_KEY },
				*args, **kwargs
			)
		except Exception as exception:
			return exception

	@staticmethod
	def post( key : API_Key, url : str, *args, **kwargs ) -> Response | Exception:
		try:
			return requests_post(
				url,
				headers={ "x-api-key" : key.API_KEY },
				*args, **kwargs
			)
		except Exception as exception:
			return exception

class OpenCloudAPI:

	class Internal:
		@staticmethod
		def build_asset_upload_request( account : API_Key, asset : Asset ) -> dict:
			return {
				"assetType" : asset.AssetType,
				"displayName" : asset.Name,
				"description" : "No Description",
				"creationContext" : {
					"creator" : { "userId" : account.CREATOR_ID }
				}
			}

		@staticmethod
		def was_operation_moderation_successful( operation_data : dict ) -> bool | None:
			try:
				# TODO: check equal statement
				print( operation_data )
				state = operation_data.get("moderationResult").get("moderationState")
				return state == "ModerationSuccess"
			except:
				pass
			return None

	@staticmethod
	def from_decal_asset_id_get_image_id( decal_asset_id : int ) -> int:
		try:
			response = requests_get( URLS.FIND_DECAL_IMAGE_ID.format(decal_asset_id) )
			return int(response.text)
		except:
			pass
		return -1
	
	@staticmethod
	def from_mesh_asset_id_get_mesh_id( mesh_asset_id : int ) -> int:
		try:
			response = requests_get( URLS.FIND_MESH_RAW_ID.format(mesh_asset_id) )
			return int(response.text)
		except:
			pass
		return -1

	@staticmethod
	def from_operation_id_get_status( account : API_Key, operation_id : str ) -> (OperationStatus, Any):
		try:
			response = Requests.get(account, URLS.OPERATIONS_STATUS_API.format(operation_id))
		except Exception as exception:
			return (OperationStatus.Exception, exception)

		if response.status_code != 200:
			return (OperationStatus.Unavailable, response.reason)

		try:
			data = response.json()
			moderation_state = OpenCloudAPI.Internal.was_operation_moderation_successful( data )
			if moderation_state == None:
				raise Exception("Moderation result could not be found in response.")
			if moderation_state == False:
				return (OperationStatus.Moderated, None)
			if data.get("done") == True:
				return (OperationStatus.Success, data)
		except Exception as exception:
			return (OperationStatus.Exception, exception)

		return (OperationStatus.Waiting, None)

	@staticmethod
	def upload_asset_return_operation_id( account : API_Key, asset : Asset ) -> str | Exception | None:
		request_data : dict = OpenCloudAPI.Internal.build_asset_upload_request( account, asset )
		file : TextIOWrapper = open(asset.Filepath, 'rb')

		try:
			response = Requests.get(account, URLS.ROBLOX_ASSETS_API, files={
				'request' : (None, json_dumps(request_data)),
				'fileContent' : file
			})
		except Exception as exception:
			return exception

		if response.status_code != 200:
			return None

		try:
			return response.json().get("path")[11:]
		except Exception as exception:
			return exception
