from __future__ import annotations
from typing import Any, Dict, Optional, TypedDict, Union, Literal, List
from typing_extensions import NotRequired, Required

Snowflake = str
SnowflakeList = List[Snowflake]
ChannelTypeWithoutThread = Literal[0, 1, 2, 3, 4, 5, 6, 13, 15]
ThreadArchiveDuration = Literal[60, 1440, 4320, 10080]
ThreadType = Literal[10, 11, 12]


class _BasePartialChannel(TypedDict):
    id: Snowflake
    name: str
    permissions: str


class PartialChannel(_BasePartialChannel):
    type: ChannelTypeWithoutThread


class ThreadMetadata(TypedDict):
    archived: bool
    auto_archive_duration: ThreadArchiveDuration
    archive_timestamp: str
    archiver_id: NotRequired[Snowflake]
    locked: NotRequired[bool]
    invitable: NotRequired[bool]
    create_timestamp: NotRequired[str]


class PartialThread(_BasePartialChannel):
    type: ThreadType
    thread_metadata: ThreadMetadata
    parent_id: Snowflake


class PartialUser(TypedDict):
    id: Snowflake
    username: str
    discriminator: str
    avatar: Optional[str]


PremiumType = Literal[0, 1, 2]


class User(PartialUser, total=False):
    bot: bool
    system: bool
    mfa_enabled: bool
    local: str
    verified: bool
    email: Optional[str]
    flags: int
    premium_type: PremiumType
    public_flags: int


class Nickname(TypedDict):
    nick: str


class PartialMember(TypedDict):
    roles: SnowflakeList
    joined_at: str
    deaf: str
    mute: str


class Member(PartialMember, total=False):
    avatar: str
    user: User
    nick: str
    premium_since: Optional[str]
    pending: bool
    permissions: str
    communication_disabled_until: str


class RoleTags(TypedDict, total=False):
    bot_id: Snowflake
    integration_id: Snowflake
    premium_subscriber: None


class Role(TypedDict):
    id: Snowflake
    name: str
    color: int
    hoist: bool
    position: int
    permissions: str
    managed: bool
    mentionable: bool
    icon: NotRequired[Optional[str]]
    unicode_emoji: NotRequired[Optional[str]]
    tags: NotRequired[RoleTags]


class EmbedFooter(TypedDict):
    text: str
    icon_url: NotRequired[str]
    proxy_icon_url: NotRequired[str]


class EmbedField(TypedDict):
    name: str
    value: str
    inline: NotRequired[bool]


class EmbedThumbnail(TypedDict, total=False):
    url: Required[str]
    proxy_url: str
    height: int
    width: int


class EmbedVideo(TypedDict, total=False):
    url: str
    proxy_url: str
    height: int
    width: int


class EmbedImage(TypedDict, total=False):
    url: Required[str]
    proxy_url: str
    height: int
    width: int


class EmbedProvider(TypedDict, total=False):
    name: str
    url: str


class EmbedAuthor(TypedDict, total=False):
    name: Required[str]
    url: str
    icon_url: str
    proxy_icon_url: str


EmbedType = Literal['rich', 'image', 'video', 'gifv', 'article', 'link']


class Embed(TypedDict, total=False):
    title: str
    type: EmbedType
    description: str
    url: str
    timestamp: str
    color: int
    footer: EmbedFooter
    image: EmbedImage
    thumbnail: EmbedThumbnail
    video: EmbedVideo
    provider: EmbedProvider
    author: EmbedAuthor
    fields: List[EmbedField]


class PartialMessage(TypedDict):
    channel_id: Snowflake
    guild_id: NotRequired[Snowflake]


ChannelTypeWithoutThread = Literal[0, 1, 2, 3, 4, 5, 6, 13, 15]
ChannelType = Union[ChannelTypeWithoutThread, ThreadType]



class PartialEmoji(TypedDict):
    id: Optional[Snowflake]
    name: Optional[str]


class ChannelMention(TypedDict):
    id: Snowflake
    guild_id: Snowflake
    type: ChannelType
    name: str


class Reaction(TypedDict):
    count: int
    me: bool
    emoji: PartialEmoji


class Attachment(TypedDict):
    id: Snowflake
    filename: str
    size: int
    url: str
    proxy_url: str
    height: NotRequired[Optional[int]]
    width: NotRequired[Optional[int]]
    description: NotRequired[str]
    content_type: NotRequired[str]
    spoiler: NotRequired[bool]
    ephemeral: NotRequired[bool]


MessageActivityType = Literal[1, 2, 3, 5]


class MessageActivity(TypedDict):
    type: MessageActivityType
    party_id: str


class MessageApplication(TypedDict):
    id: Snowflake
    description: str
    icon: Optional[str]
    name: str
    cover_image: NotRequired[str]


class MessageReference(TypedDict, total=False):
    message_id: Snowflake
    channel_id: Snowflake
    guild_id: Snowflake
    fail_if_not_exists: bool


MessageType = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 18, 19, 20, 21]


class _OptionalMemberWithUser(PartialMember, total=False):
    avatar: str
    nick: str
    premium_since: Optional[str]
    pending: bool
    permissions: str
    communication_disabled_until: str


class UserWithMember(User, total=False):
    member: _OptionalMemberWithUser


class Message(PartialMessage):
    id: Snowflake
    author: User
    content: str
    timestamp: str
    edited_timestamp: Optional[str]
    tts: bool
    mention_everyone: bool
    mentions: List[UserWithMember]
    mention_roles: SnowflakeList
    attachments: List[Attachment]
    embeds: List[Embed]
    pinned: bool
    type: MessageType
    member: NotRequired[Member]
    mention_channels: NotRequired[List[ChannelMention]]
    reactions: NotRequired[List[Reaction]]
    nonce: NotRequired[Union[int, str]]
    webhook_id: NotRequired[Snowflake]
    activity: NotRequired[MessageActivity]
    application: NotRequired[MessageApplication]
    application_id: NotRequired[Snowflake]
    message_reference: NotRequired[MessageReference]
    flags: NotRequired[int]
    sticker_items: NotRequired[List[Any]]
    referenced_message: NotRequired[Optional[Message]]
    interaction: NotRequired[Any]
    components: NotRequired[List[Any]]


AllowedMentionType = Literal['roles', 'users', 'everyone']


class AllowedMentions(TypedDict):
    parse: List[AllowedMentionType]
    roles: SnowflakeList
    users: SnowflakeList
    replied_user: bool


class ResolvedData(TypedDict):
    users: Dict[str, Dict[str, User]]
    members: Dict[str, Dict[str, Member]]
    roles: Dict[str, Dict[str, Role]]
    channels: Dict[str, Dict[str, Union[PartialChannel, PartialThread]]]
    messages: Dict[str, Message]
    attachments: Dict[str, Attachment]

class OptionsData(TypedDict):
    ...

class SlashCommand(TypedDict):
    id: Snowflake
    token: str
    version: Literal[1]
    application_id: Snowflake
    type: Literal[1]
    resolved: NotRequired[ResolvedData]
    options: NotRequired[OptionsData]
    guild_id: NotRequired[int]
    locale: NotRequired[str]
    guild_locale: NotRequired[str]

