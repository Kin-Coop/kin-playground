from dataclasses import dataclass
from enum import Enum


AccountType = Enum('AccountType', [
    'BOT',
    'COLLECTIVE',
    'EVENT',
    'FUND',
    'INDIVIDUAL',
    'ORGANIZATION',
    'PROJECT',
    'VENDOR'
])


@dataclass
class Account:
    id_: str
    slug: str
    type: AccountType
    name: str
    legal_name: str

    @classmethod
    def from_data(cls, data: dict) -> 'Account':
        return cls(
            id_=data['id'],
            slug=data['slug'],
            type=AccountType._member_map_[data['type']],
            name=data['name'],
            legal_name=data['legalName'],
        )
