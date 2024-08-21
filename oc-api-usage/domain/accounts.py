from dataclasses import dataclass
from enum import Enum, auto


class AccountType(Enum):
    BOT = auto()
    COLLECTIVE = auto()
    EVENT = auto()
    FUND = auto()
    INDIVIDUAL = auto()
    ORGANIZATION = auto()
    PROJECT = auto()
    VENDOR = auto()

    @classmethod
    def from_string(cls, string) -> 'AccountType':
        return AccountType(cls._member_map_[string])


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
            type=AccountType.from_string(data['type']),
            name=data['name'],
            legal_name=data['legalName'],
        )
