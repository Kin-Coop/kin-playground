from os import environ as env

from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport

from kin_client import KinClient

OC_BASE_URL = 'https://api.opencollective.com/graphql/v2'


def main(token: str):
    transport = AIOHTTPTransport(url=OC_BASE_URL, headers={'Authorization': f'Bearer {token}'})
    gql_client = Client(transport=transport, fetch_schema_from_transport=True)
    kin_client = KinClient(gql_client)

    kin_host = kin_client.get_host('kincooperative')

    print(kin_host)


if __name__ == '__main__':
    main(env['TOKEN'])
