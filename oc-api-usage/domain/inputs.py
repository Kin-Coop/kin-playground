from dataclasses import dataclass
from typing import Optional


@dataclass
class AccountReferenceInput:
    slug: Optional[str]


@dataclass
class CollectiveCreateInput:
    name: str
    description: str
    slug: Optional[str]


@dataclass
class IndividualCreateInput:
    name: str
    email: str
