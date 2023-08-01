
import argparse

from sys import path as sys_path, argv
from os import path as os_path

FILE_DIRECTORY = os_path.dirname(os_path.realpath(__file__))

sys_path.append( os_path.join( FILE_DIRECTORY, ".." ) )

from python import API_Key, AssetsAPI, DatastoreAPI, MessagingServiceAPI

sys_path.pop()

parser = argparse.ArgumentParser()
parser.add_argument("-k", "--Key", help="API Key for Open Cloud", required=True, type=str)
parser.add_argument("-i", "--Id", help="CreatorId for the specified API Key -> UserId or GroupId.", required=True, type=int)

if __name__ == "__main__":

	args = parser.parse_args()

	key = API_Key(args.Key, args.Id)
