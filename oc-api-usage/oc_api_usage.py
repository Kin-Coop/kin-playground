from os import environ as env

from gql import Client as GqlClient
from gql.transport.aiohttp import AIOHTTPTransport

from domain.actions import ProcessHostApplicationAction
from domain.inputs import CollectiveCreateInput, IndividualCreateInput, AccountReferenceInput
from kin_client import UserClient, AdminClient

OC_BASE_URL = 'https://api.opencollective.com/graphql/v2'
SAVING_CLUB_SLUG = 'rjf-saving-club-1'


def main(*, user_token: str, admin_token: str):
    user_client = _create_user_client(user_token)
    admin_client = _create_admin_client(admin_token)

    user_client.create_collective(
        CollectiveCreateInput(
            name='My First Saving Club',
            slug=SAVING_CLUB_SLUG,
            description='A club for testing integration of Kin Coop with Open Collective',
        ),
        IndividualCreateInput(name='Rich', email='foo@bar.com'),
    )

    admin_client.process_host_application(
        account=AccountReferenceInput(SAVING_CLUB_SLUG),
        action=ProcessHostApplicationAction.APPROVE,
    )


def _create_user_client(token) -> UserClient:
    return _create_client(UserClient, token)


def _create_admin_client(token) -> AdminClient:
    return _create_client(AdminClient, token)


def _create_client(client_constructor, token):
    transport = AIOHTTPTransport(url=OC_BASE_URL, headers={'Authorization': f'Bearer {token}'})
    gql_client = GqlClient(transport=transport, fetch_schema_from_transport=True)
    return client_constructor(gql_client)


if __name__ == '__main__':
    main(
        user_token=env['USER_TOKEN'],
        admin_token=env['ADMIN_TOKEN']
    )
