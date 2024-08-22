from gql import Client as GqlClient, gql

from utils import tolerant_of
from value_objects import ProcessHostApplicationAction


class Client:
    def __init__(self, gql_client: GqlClient, host_slug: str):
        self._host_slug = host_slug
        self._gql_client = gql_client

    def _execute(self, document_name: str, variable_values: dict = None) -> dict:
        with open(f'documents/{document_name}.gql', 'r') as f:
            document = gql(f.read())
        return self._gql_client.execute(document, variable_values=variable_values)


class UserClient(Client):

    @tolerant_of('account already exists')
    def create_collective(
            self, *,
            collective_name: str,
            collective_slug: str,
            collective_description: str,
            individual_name: str,
            individual_email: str,
    ):
        return self._execute('create_collective', {
            'collective': {
                'name': collective_name,
                'slug': collective_slug,
                'description': collective_description,
            },
            'host': {
                'slug': self._host_slug
            },
            'user': {
                'name': individual_name,
                'email': individual_email,
            },
        })


class AdminClient(Client):

    @tolerant_of('collective application has already been approved')
    def process_host_application(self, *, account_slug: str, action: ProcessHostApplicationAction):
        return self._execute('process_host_application', {
            'account': {
                'slug': account_slug,
            },
            'host': {
                'slug': self._host_slug,
            },
            'action': action.name,
        })
