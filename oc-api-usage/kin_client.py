from gql import Client, gql

import documents
from queries import Account


class KinClient:
    def __init__(self, gql_client: Client):
        self.gql_client = gql_client

    def get_host(self, slug: str):
        response = self.gql_client.execute(gql(documents.GET_HOST), variable_values={'slug': slug})
        return Account.from_data(response['host'])
