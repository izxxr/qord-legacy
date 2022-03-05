.. currentmodule:: qord

API Reference
=============

Welcome to API Reference of Qord. This section details every single aspect of the
core API.

The Starter Point
-----------------

Client
~~~~~~

.. autoclass:: Client
    :members:


Abstract Classes
~~~~~~~~~~~~~~~~

Other classes provided by the library can inherit these classes to implement the
relevant common functionality.

MessagesSupported
~~~~~~~~~~~~~~~~~

.. autoclass:: MessagesSupported()
    :members:

Cache Handlers
--------------

The classes documented below implement the logic of caching for various entities sent
by Discord over gateway like users and guilds etc.

By default the library provides cache handlers that implement "in memory" caching
usually suitable for most use cases. However if you want to write custom cache handlers
for a specific use case, Qord also allows you to do that too. Following abstract classes
will help you achieve that:

- :class:`Cache`
- :class:`GuildCache`

Cache
~~~~~

.. autoclass:: Cache()
    :members:

GuildCache
~~~~~~~~~~

.. autoclass:: GuildCache()
    :members:

DefaultCache
~~~~~~~~~~~~

.. autoclass:: DefaultCache()
    :inherited-members:
    :members:

DefaultGuildCache
~~~~~~~~~~~~~~~~~~

.. autoclass:: DefaultGuildCache()
    :inherited-members:
    :members:


Events
------

Qord provides a rich interface for handling of events dispatches sent over gateway. Below
documentation describes the structure of various gateway events.

The recommended way to register an event listener, is to use the :meth:`Client.event`
decorator to decorate the callback coroutine. Example::

    @client.event(qord.GatewayEvent.MESSAGE_CREATE)
    async def on_message_create(event):
        pass

Also see :class:`GatewayEvent` that details the events names that are sent over gateway.

BaseEvent
~~~~~~~~~

.. autoclass:: qord.events.BaseEvent()
    :members:

GatewayDispatch
~~~~~~~~~~~~~~~

.. autoclass:: qord.events.GatewayDispatch()
    :members:

ShardReady
~~~~~~~~~~

.. autoclass:: qord.events.ShardReady()
    :members:

Ready
~~~~~

.. autoclass:: qord.events.Ready()
    :members:

Resumed
~~~~~~~

.. autoclass:: qord.events.Resumed()
    :members:

UserUpdate
~~~~~~~~~~

.. autoclass:: qord.events.UserUpdate()
    :members:

GuildAvailable
~~~~~~~~~~~~~~

.. autoclass:: qord.events.GuildAvailable()
    :members:

GuildUnavailable
~~~~~~~~~~~~~~~~

.. autoclass:: qord.events.GuildUnavailable()
    :members:

GuildJoin
~~~~~~~~~

.. autoclass:: qord.events.GuildJoin()
    :members:


GuildLeave
~~~~~~~~~~

.. autoclass:: qord.events.GuildLeave()
    :members:

GuildUpdate
~~~~~~~~~~~

.. autoclass:: qord.events.GuildUpdate()
    :members:

RoleCreate
~~~~~~~~~~

.. autoclass:: qord.events.RoleCreate()
    :members:

RoleUpdate
~~~~~~~~~~

.. autoclass:: qord.events.RoleUpdate()
    :members:

RoleDelete
~~~~~~~~~~

.. autoclass:: qord.events.RoleDelete()
    :members:

GuildMemberAdd
~~~~~~~~~~~~~~

.. autoclass:: qord.events.GuildMemberAdd()
    :members:

GuildMemberUpdate
~~~~~~~~~~~~~~~~~

.. autoclass:: qord.events.GuildMemberUpdate()
    :members:

GuildMemberRemove
~~~~~~~~~~~~~~~~~

.. autoclass:: qord.events.GuildMemberRemove()
    :members:


ChannelCreate
~~~~~~~~~~~~~

.. autoclass:: qord.events.ChannelCreate()
    :members:


ChannelUpdate
~~~~~~~~~~~~~

.. autoclass:: qord.events.ChannelUpdate()
    :members:

ChannelPinsUpdate
~~~~~~~~~~~~~~~~~

.. autoclass:: ChannelPinsUpdate()
    :members:

ChannelDelete
~~~~~~~~~~~~~

.. autoclass:: qord.events.ChannelDelete()
    :members:

TypingStart
~~~~~~~~~~~

.. autoclass:: qord.events.TypingStart()
    :members:

MessageCreate
~~~~~~~~~~~~~

.. autoclass:: qord.events.MessageCreate()
    :members:


MessageUpdate
~~~~~~~~~~~~~

.. autoclass:: qord.events.MessageUpdate()
    :members:


MessageDelete
~~~~~~~~~~~~~

.. autoclass:: qord.events.MessageDelete()
    :members:


MessageBulkDelete
~~~~~~~~~~~~~~~~~~~

.. autoclass:: qord.events.MessageBulkDelete()
    :members:


Enumerations
------------

These classes details the various enumerations including the integers based enumerations
sent by Discord.

GatewayEvent
~~~~~~~~~~~~

.. autoclass:: GatewayEvent()
    :members:

PremiumType
~~~~~~~~~~~

.. autoclass:: PremiumType()
    :members:

ImageExtension
~~~~~~~~~~~~~~

.. autoclass:: ImageExtension()
    :members:

DefaultAvatar
~~~~~~~~~~~~~

.. autoclass:: DefaultAvatar()
    :members:

VerificationLevel
~~~~~~~~~~~~~~~~~

.. autoclass:: VerificationLevel()
    :members:

NSFWLevel
~~~~~~~~~

.. autoclass:: NSFWLevel()
    :members:

NotificationLevel
~~~~~~~~~~~~~~~~~

.. autoclass:: NotificationLevel()
    :members:

ExplicitContentFilter
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ExplicitContentFilter()
    :members:

ChannelType
~~~~~~~~~~~

.. autoclass:: ChannelType()
    :members:

VideoQualityMode
~~~~~~~~~~~~~~~~

.. autoclass:: VideoQualityMode()
    :members:

PremiumTier
~~~~~~~~~~~

.. autoclass:: PremiumTier()
    :members:

MFALevel
~~~~~~~~

.. autoclass:: MFALevel()
    :members:

Data classes
------------

Shard
~~~~~

.. autoclass:: Shard()
    :members:

Bitwise Flags
-------------

Flags
~~~~~

.. autoclass:: Flags()
    :members:

Permissions
~~~~~~~~~~~

.. autoclass:: Permissions()
    :members:

Intents
~~~~~~~

.. autoclass:: Intents()
    :members:

UserFlags
~~~~~~~~~

.. autoclass:: UserFlags()
    :members:

SystemChannelFlags
~~~~~~~~~~~~~~~~~~

.. autoclass:: SystemChannelFlags()
    :members:

Exceptions
----------

These are the exceptions raised by the library. All of these exceptions inherit a common
class :exc:`QordException`.

QordException
~~~~~~~~~~~~~

.. autoexception:: QordException()

ClientSetupRequired
~~~~~~~~~~~~~~~~~~~

.. autoexception:: ClientSetupRequired()

HTTPException
~~~~~~~~~~~~~

.. autoexception:: HTTPException()

HTTPBadRequest
~~~~~~~~~~~~~~

.. autoexception:: HTTPBadRequest()

HTTPForbidden
~~~~~~~~~~~~~

.. autoexception:: HTTPForbidden()

HTTPNotFound
~~~~~~~~~~~~

.. autoexception:: HTTPNotFound()

HTTPServerError
~~~~~~~~~~~~~~~

.. autoexception:: HTTPServerError()

ShardException
~~~~~~~~~~~~~~

.. autoexception:: ShardException()

ShardCloseException
~~~~~~~~~~~~~~~~~~~

.. autoexception:: ShardCloseException()

MissingPrivilegedIntents
~~~~~~~~~~~~~~~~~~~~~~~~

.. autoexception:: MissingPrivilegedIntents()

Discord Models
--------------

BaseModel
~~~~~~~~~

.. autoclass:: BaseModel()
    :members:

User
~~~~

.. autoclass:: User()
    :inherited-members:
    :members:

ClientUser
~~~~~~~~~~

.. autoclass:: ClientUser()
    :inherited-members:
    :members:

Guild
~~~~~

.. autoclass:: Guild()
    :inherited-members:
    :members:

GuildMember
~~~~~~~~~~~

.. autoclass:: GuildMember()
    :inherited-members:
    :members:

Role
~~~~

.. autoclass:: Role()
    :inherited-members:
    :members:

GuildChannel
~~~~~~~~~~~~

.. autoclass:: GuildChannel()
    :inherited-members:
    :members:

CategoryChannel
~~~~~~~~~~~~~~~

.. autoclass:: CategoryChannel()
    :inherited-members:
    :members:

TextChannel
~~~~~~~~~~~

.. autoclass:: TextChannel()
    :inherited-members:
    :members:

NewsChannel
~~~~~~~~~~~

.. autoclass:: NewsChannel()
    :inherited-members:
    :members:

VoiceChannel
~~~~~~~~~~~~

.. autoclass:: VoiceChannel()
    :inherited-members:
    :members:

StageChannel
~~~~~~~~~~~~

.. autoclass:: StageChannel()
    :inherited-members:
    :members:

PrivateChannel
~~~~~~~~~~~~~~

.. autoclass:: PrivateChannel()
    :inherited-members:
    :members:

DMChannel
~~~~~~~~~

.. autoclass:: DMChannel()
    :inherited-members:
    :members:

Message
~~~~~~~

.. autoclass:: Message()
    :inherited-members:
    :members:

ChannelMention
~~~~~~~~~~~~~~

.. autoclass:: ChannelMention()
    :inherited-members:
    :members:
