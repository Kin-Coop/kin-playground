from dataclasses import dataclass

from gql.transport.aiohttp import AIOHTTPTransport
from gql import Client as GqlClient

from client import UserClient, AdminClient


@dataclass
class ClientFactory:
    base_url: str
    host_slug: str

    def create_user_client(self, token: str) -> UserClient:
        return UserClient(self._create_gql_client(token), host_slug=self.host_slug)

    def create_admin_client(self, token: str) -> AdminClient:
        return AdminClient(self._create_gql_client(token), host_slug=self.host_slug)

    def _create_gql_client(self, token: str):
        transport = AIOHTTPTransport(url=self.base_url, headers={'Authorization': f'Bearer {token}'})
        return GqlClient(transport=transport, fetch_schema_from_transport=True)
