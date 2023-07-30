
def ListUniverseDataStores(api_key, universeId):
	datastores = []

	cursor = ""
	while True:
		response = requests.get(
			STANDARD_DATASTORE_URL.format(universeId),
			headers = {'x-api-key' : api_key} ).json()
		datastores.extend( response.get('datastores') )
		cursor = response.get('nextPageCursor')
		if cursor == "":
			break

	return datastores

def ListUserDataInDataStore(api_key, universeId, datastoreName, prefix="", limit=100):
	URL = STANDARD_DATASTORE_URL.format(universeId) + f"/datastore/entries"
	possible_keys = []
	cursor = ""
	while True:
		response = requests.get(URL, params={
			'datastoreName' : datastoreName,
			'cursor' : cursor,
			'prefix' : prefix,
			'allScopes' : True,
			'limit' : limit
		}, headers={'x-api-key' : api_key} ).json()
		for key in response.get('keys'):
			possible_keys.append( key.get('key') )
		cursor = response.get('nextPageCursor')
		if cursor == "" or cursor == None:
			break
	return possible_keys

def GetDataFromIdInDataStore(api_key, universeId, datastoreName, id):
	URL = STANDARD_DATASTORE_URL.format(universeId) + f"/datastore/entries/entry"
	return requests.get(URL, params={
		'datastoreName' : datastoreName,
		'entryKey' : id
	}, headers={'x-api-key' : api_key} ).json()

def _GetContentMD5(data : str):
	return str(b64encode(md5(bytes(data, encoding='utf8')).digest()), encoding='utf8')

def SetEntryForIdInDataStore(api_key, universeId, datastoreName, id, data : str):
	URL = STANDARD_DATASTORE_URL.format(universeId) + f"/datastore/entries/entry"
	return requests.post(URL,
		params = { 'datastoreName' : datastoreName, 'entryKey' : id, },
		data = data,
		headers = {'x-api-key' : api_key, 'content-md5' : _GetContentMD5(data)}
	).json()

def RemoveEntryForIdInDataStore(api_key, universeId, datastoreName, id):
	URL = STANDARD_DATASTORE_URL.format(universeId) + f"/datastore/entries/entry"
	return requests.delete(URL, params={
		'datastoreName' : datastoreName,
		'entryKey' : id,
	}, headers={'x-api-key' : api_key})
