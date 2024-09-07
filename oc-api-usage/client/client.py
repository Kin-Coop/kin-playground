import json
from typing import Optional, Collection

from gql import Client as GqlClient, gql
from gql.transport.exceptions import TransportQueryError

from model import ProcessHostApplicationAction, MemberRole


class UnexpectedErrors(Exception):
    pass


class Client:
    def __init__(self, gql_client: GqlClient, host_slug: str):
        self._host_slug = host_slug
        self._gql_client = gql_client

    def get_logged_in_account(self) -> dict:
        response = self._execute('get_logged_in_account')
        return response['loggedInAccount']

    def _execute(
            self, document_name: str, variable_values: dict = None, *, tolerated_error: str = None
    ) -> Optional[dict]:

        with open(f'documents/{document_name}.gql', 'r') as f:
            document = gql(f.read())

        print('\nCalling:', document_name)
        try:
            response = self._gql_client.execute(document, variable_values=variable_values)
            print('Response:', json.dumps(response, indent=2))
            return response
        except TransportQueryError as error:
            error_messages = [e['message'] for e in error.errors]
            print('Errors:', error_messages)
            unexpected_errors = [
                msg for msg in error_messages if not tolerated_error or tolerated_error not in msg
            ]
            if not unexpected_errors:
                return None
            raise UnexpectedErrors(unexpected_errors)


class UserClient(Client):

    def create_collective(
            self, *,
            collective_name: str,
            collective_slug: str,
            collective_description: str,
            individual_name: str,
            individual_email: str,
    ):
        return self._execute(
            'create_collective',
            {
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
            },
            tolerated_error='account already exists'
        )

    def invite_member(
            self, *,
            collective_slug: str,
            invitee_slug: str,
            member_role: MemberRole
    ):
        return self._execute(
            'invite_member',
            {
                'memberAccount': {
                    'slug': collective_slug,
                },
                'account': {
                    'slug': invitee_slug,
                },
                'role': str(member_role),
            }
        )


class AdminClient(Client):

    def process_host_application(self, *, account_slug: str, action: ProcessHostApplicationAction):
        return self._execute(
            'process_host_application',
            {
                'account': {
                    'slug': account_slug,
                },
                'host': {
                    'slug': self._host_slug,
                },
                'action': str(action),
            },
            tolerated_error='collective application has already been approved'
        )
