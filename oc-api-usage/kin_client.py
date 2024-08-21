from dataclasses import asdict
from enum import Enum

from gql import Client as GqlClient, gql
from gql.transport.exceptions import TransportQueryError

from domain.accounts import Account
from domain.actions import ProcessHostApplicationAction
from domain.inputs import AccountReferenceInput, IndividualCreateInput, CollectiveCreateInput

GRAPHQL_DOCUMENT_DIR = 'graphql'

KIN_HOST_SLUG = 'kincooperative'
OC_CLIENT_ID = 'c3f66ec8d528d04e1c5a'


def tolerant_of(error_message):
    def is_acceptable(error: TransportQueryError):
        for e in error.errors:
            if error_message in e['message']:
                return True
            return False

    def wrap(func):
        def wrapped_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except TransportQueryError as error:
                if is_acceptable(error):
                    return None
                raise error
        return wrapped_func

    return wrap


class Client:
    def __init__(self, gql_client: GqlClient):
        self.gql_client = gql_client

    def get_account(self, slug: str) -> Account:
        response = self._execute('get_account', {'slug': slug})
        return Account.from_data(response['account'])

    def _execute(self, document_name: str, inputs: dict = None) -> dict:
        with open(f'{GRAPHQL_DOCUMENT_DIR}/{document_name}.gql', 'r') as f:
            document = gql(f.read())
        return self.gql_client.execute(document, variable_values=_sanitise_dict(inputs))


class UserClient(Client):

    @tolerant_of('account already exists')
    def create_collective(self, collective: CollectiveCreateInput, user: IndividualCreateInput) -> Account:
        response = self._execute('create_collective', {
            'collective': collective, 'host': AccountReferenceInput(KIN_HOST_SLUG), 'user': user,
        })
        return Account.from_data(response['createCollective'])


class AdminClient(Client):

    @tolerant_of('collective application has already been approved')
    def process_host_application(
            self, account: AccountReferenceInput, action: ProcessHostApplicationAction
    ) -> Account:
        response = self._execute('process_host_application', {
            'account': account, 'host': AccountReferenceInput(KIN_HOST_SLUG), 'action': action,
        })
        return Account.from_data(response['processHostApplication']['account'])


def _sanitise(value):
    if isinstance(value, dict):
        return _sanitise_dict(value)
    if isinstance(value, Enum):
        return value.name
    try:
        return asdict(value)
    except TypeError:
        return value


def _sanitise_dict(data: dict):
    return {k: _sanitise(v) for k, v in data.items()}
