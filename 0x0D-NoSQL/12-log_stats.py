#!/usr/bin/env python3
""" Log stats """
from pymongo import MongoClient

MONGO_DB = {'host': '127.0.0.1', 'port': 27017}
METHODS = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')

class MongoDB:
    """Class mongo DB connection"""
    def __init__(self, db_name: str, host: str, port: int):
        """
        initialize connection to mongodb
        :db_name: Database name to connect
        :host: host service mongodb
        :port: port to enter
        """
        self.client = MongoClient(f'mongodb://{host}:{port}')
        self.db = self.client[db_name]
        self.collection = None

    def get_collection(self, collection_name: str):
        """
        Get collection

        :collection_name: Collection name to get
        :return: Return collection object
        """
        self.collection = self.db[collection_name]
        return self.collection

    def count_logs(self, method: str = None, path: str = None):
        """
        Count number of logs
        :return: return number of logs
        """
        if method is None and path is None:
            return self.collection.count_documents({})
        elif method is not None and path is not None:
            return self.collection.count_documents({"method": method, "path": path})
        return self.collection.count_documents({'method': method})


def main():
    """
    Client entry. Main program
    """
    mongo_db = MongoDB(db_name='logs', host=MONGO_DB['host'], port=MONGO_DB['port'])
    mongo_db.get_collection(collection_name='nginx')
    print(f'{mongo_db.count_logs()} logs\nMethods:')
    for method in METHODS:
        print(f'\tmethod {method}: {mongo_db.count_logs(method)}')
    print(f'{mongo_db.count_logs("GET", "/status")} status check')


if __name__ == '__main__':
    main()