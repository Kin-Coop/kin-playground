from os import environ as env

from client import ClientFactory, UnexpectedErrors
from model import ProcessHostApplicationAction, MemberRole


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


def main(*, user_1_token: str, user_2_token: str, admin_token: str):
    client_factory = ClientFactory(base_url=OC_BASE_URL, host_slug=KIN_HOST_SLUG)
    user_1_client = client_factory.create_user_client(user_1_token)
    user_2_client = client_factory.create_user_client(user_2_token)
    admin_client = client_factory.create_admin_client(admin_token)

    user_1_client.create_collective(**CREATE_COLLECTIVE_PARAMS)
    admin_client.process_host_application(**PROCESS_HOST_APPLICATION_PARAMS)

    user_2_account = user_2_client.get_logged_in_account()

    user_1_client.invite_member(
        collective_slug=SAVING_CLUB_SLUG, invitee_slug=user_2_account['slug'], member_role=MemberRole.CONTRIBUTOR
    )


if __name__ == '__main__':
    try:
        main(user_1_token=env['USER_1_TOKEN'], user_2_token=env['USER_2_TOKEN'], admin_token=env['ADMIN_TOKEN'])
    except UnexpectedErrors as e:
        print('\nUnexpected errors:', e)
