from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase
import os


def get_mongo_uri():
    return f"mongodb+srv://{os.environ.get('MONGO_USER')}:{os.environ.get('MONGO_PASSWORD')}@{os.environ.get('MONGO_CLUSTER')}/?retryWrites=true&w=majority&appName=Cluster0"


class MongoClient:
    _client: AsyncIOMotorClient = None

    def __init__(self, db_name):
        self.db_name = db_name

    # get a cursor to the database and collection
    def get_database(self) -> AsyncIOMotorDatabase:
        """
        Retrieve a database by name
        """
        return self._client[self.db_name]

    def collection(self, col_name) -> AsyncIOMotorCollection:
        return self._client[self.db_name][col_name]

    async def connect_db(self):
        """
        Connect to the database on startup
        """
        try:
            self._client = AsyncIOMotorClient(get_mongo_uri())
            print("Connected to mongo.")
        except Exception as e:
            print("Error connecting to mongo.")
            raise e

    async def disconnect_db(self):
        """ Disconnect from the database on shutdown """
        if self._client is None:
            return
        self._client.close()
        print("disconnected from mongo")
