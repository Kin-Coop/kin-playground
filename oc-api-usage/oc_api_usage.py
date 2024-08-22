from os import environ as env

from factory import ClientFactory
from value_objects import ProcessHostApplicationAction

OC_BASE_URL = 'https://api.opencollective.com/graphql/v2'

KIN_HOST_SLUG = 'kincooperative'
SAVING_CLUB_SLUG = 'temp-saving-club'

CREATE_COLLECTIVE_PARAMS = {
    'collective_name': 'Temporary Saving Club',
    'collective_slug': SAVING_CLUB_SLUG,
    'collective_description':
        'A collective for testing integration of Kin Coop with Open Collective. Feel free to delete.',
    'individual_name': 'Jay Bloggs',
    'individual_email': 'jay@bloggs.com'
}

PROCESS_HOST_APPLICATION_PARAMS = {
    'account_slug': SAVING_CLUB_SLUG,
    'action': ProcessHostApplicationAction.APPROVE
}


def main(*, user_token: str, admin_token: str):
    client_factory = ClientFactory(base_url=OC_BASE_URL, host_slug=KIN_HOST_SLUG)
    user_client = client_factory.create_user_client(user_token)
    admin_client = client_factory.create_admin_client(admin_token)

    user_client.create_collective(**CREATE_COLLECTIVE_PARAMS)
    admin_client.process_host_application(**PROCESS_HOST_APPLICATION_PARAMS)


if __name__ == '__main__':
    main(
        user_token=env['USER_TOKEN'],
        admin_token=env['ADMIN_TOKEN']
    )
