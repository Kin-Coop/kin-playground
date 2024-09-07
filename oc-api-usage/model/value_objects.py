from enum import Enum, auto
from typing import Self


class OCEnum(Enum):
    def __str__(self):
        return self.name

    @classmethod
    def from_string(cls, string) -> Self:
        return cls(cls._member_map_[string])


class ProcessHostApplicationAction(OCEnum):
    APPROVE = auto()
    REJECT = auto()
    SEND_PRIVATE_MESSAGE = auto()
    SEND_PUBLIC_MESSAGE = auto()


class MemberRole(OCEnum):
    BACKER = auto()
    ADMIN = auto()
    CONTRIBUTOR = auto()
    HOST = auto()
    ATTENDEE = auto()
    MEMBER = auto()
    FOLLOWER = auto()
    ACCOUNTANT = auto()
    CONNECTED_ACCOUNT = auto()
