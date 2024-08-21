from enum import Enum, auto


class ProcessHostApplicationAction(Enum):
    APPROVE = auto()
    REJECT = auto()
    SEND_PRIVATE_MESSAGE = auto()
    SEND_PUBLIC_MESSAGE = auto()

    @classmethod
    def from_string(cls, string) -> 'ProcessHostApplicationAction':
        return ProcessHostApplicationAction(cls._member_map_[string])
