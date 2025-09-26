from datetime import datetime
from typing import TypedDict


# region DictObjects
class BaseDictObject(TypedDict):
    uuid: str


class MemberDictObject(BaseDictObject):
    name: str


class MessageDictObject(BaseDictObject):
    encrypted_content: str
    author: MemberDictObject
    timestamp: float


class ChannelConfigDictObject(TypedDict):
    max_msg_delete: int


class ChannelDictObject(BaseDictObject):
    members: list[MemberDictObject]
    messages: list[MessageDictObject]
    configuration: ChannelConfigDictObject


# endregion DictObjects


class BaseObject:
    def __init__(self, uuid: str):
        self.uuid: str = uuid

    @classmethod
    def from_dict(self, d: BaseDictObject):
        """Loads data from a BaseDictObject to self

        Args:
            d (BaseDictObject): The dictionary to load from
        """
        self.uuid = d["uuid"]

    def to_dict(self) -> BaseDictObject:
        """Returns itself converted to a BaseDictObject

        Returns:
            BaseDictObject: A dictionary with it's data
        """
        return {"uuid": self.uuid}


class Member(BaseObject):
    def __init__(self, uuid: str):
        super().__init__(uuid=uuid)

        self.name: str

    @classmethod
    def from_dict(self, d: MemberDictObject) -> None:
        """Loads data from a MemberDictObject to self

        Args:
            d (MemberDictObject): The dictionary to load from
        """

        super().from_dict(d)
        self.name = d["name"]

    def to_dict(self) -> MemberDictObject:
        """Returns itself converted to a MemberDictObject

        Returns:
            MemberDictObject: A dictionary with it's data
        """

        d = {"name": self.name}
        d.update(super().to_dict())

        return d


class Message(BaseObject):
    def __init__(self, uuid: str):
        super().__init__(uuid=uuid)

        self.encrypted_content: str
        self.author: Member
        self.timestamp: datetime

    @classmethod
    def from_dict(self, d: MessageDictObject) -> None:
        """Loads data from a MessageDictObject to self

        Args:
            d (MessageDictObject): The dictionary to load from
        """

        super().from_dict(d)
        self.encrypted_content = d["encrypted_content"]
        self.author = Member.from_dict(d["author"])
        self.timestamp = datetime.fromtimestamp(d["timestamp"])

    def to_dict(self) -> MessageDictObject:
        """Returns itself converted to a MessageDictObject

        Returns:
            MessageDictObject: A dictionary with it's data
        """

        d = {
            "encrypted_content": self.encrypted_content,
            "author": self.author,
            "timestamp": self.timestamp,
        }
        d.update(super().to_dict())

        return d


class ChannelConfig:
    def __init__(self):
        self.max_msg_delete: int

    @classmethod
    def from_dict(self, d: ChannelConfigDictObject):
        """Loads data from a ChannelDictObject to self

        Args:
            d (ChannelConfigDictObject): The dictionary to load from
        """

        self.max_msg_delete = d["max_msg_delete"]

    def to_dict(self) -> ChannelConfigDictObject:
        """Returns itself converted to a ChannelConfigDictObject

        Returns:
            ChannelConfigDictObject: A dictionary with it's data
        """

        d = {"max_msg_delete": self.max_msg_delete}
        return d


class Channel(BaseObject):
    def __init__(self, uuid: str):
        super().__init__(uuid=uuid)

        self.members: list[Member] = []
        self.messages: list[Message] = []

        self.configuration: ChannelConfig = ChannelConfig()

    @classmethod
    def from_dict(self, d: ChannelDictObject):
        """Sets all its own data from a channel dictionary object

        Args:
            d (ChannelDictObject): The dictionary object to load from
        """
        super().from_dict(d)
        self.members = [Member.from_dict(item) for item in d["members"]]
        self.messages = [Message.from_dict(item) for item in d["messages"]]
        self.configuration = ChannelConfig.from_dict(d["configuration"])

        return self

    def to_dict(self) -> ChannelDictObject:
        """Returns itself converted to a ChannelDictObject

        Returns:
            ChannelDictObject: A dictionary with it's data
        """
        d = {
            "members": [item.to_dict() for item in self.members],
            "messages": [item.to_dict() for item in self.messages],
            "configuration": self.configuration.to_dict(),
        }
        d.update(super().to_dict())

        return d
