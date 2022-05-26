.. currentmodule:: qord


.. _api-models:

Discord Models
==============

These classes wrap the Discord's complex data models in easy to use interfaces.

It is worth noting that these classes are not meant to be initialized by users and
must only be retrieved from cache or fetched from the API using relevant API methods.


Base Classes
-------------

BaseModel
~~~~~~~~~

.. autoclass:: BaseModel()
    :members:

BaseMessageChannel
~~~~~~~~~~~~~~~~~~

.. autoclass:: BaseMessageChannel()
    :members:

Applications
------------

Application
~~~~~~~~~~~

.. autoclass:: Application()
    :members:
    :inherited-members:

ApplicationInstallParams
~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ApplicationInstallParams()
    :members:
    :inherited-members:

Team
~~~~

.. autoclass:: Team()
    :members:
    :inherited-members:

TeamMember
~~~~~~~~~~

.. autoclass:: TeamMember()
    :members:
    :inherited-members:

Users
-----

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

Guilds
------

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

ScheduledEvent
~~~~~~~~~~~~~~

.. autoclass:: ScheduledEvent()
    :inherited-members:
    :members:

Channels
--------

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

ChannelPermission
~~~~~~~~~~~~~~~~~

.. autoclass:: ChannelPermission()
    :members:

StageInstance
~~~~~~~~~~~~~

.. autoclass:: StageInstance()
    :inherited-members:
    :members:

Messages
--------

Message
~~~~~~~

.. autoclass:: Message()
    :inherited-members:
    :members:

Attachment
~~~~~~~~~~

.. autoclass:: Attachment()
    :inherited-members:
    :members:

Reaction
~~~~~~~~

.. autoclass:: Reaction()
    :members:

ChannelMention
~~~~~~~~~~~~~~

.. autoclass:: ChannelMention()
    :inherited-members:
    :members:


Emojis
------

Emoji
~~~~~

.. autoclass:: Emoji()
    :inherited-members:
    :members:

PartialEmoji
~~~~~~~~~~~~

.. autoclass:: PartialEmoji()
    :members:

Invites
-------

Invite
~~~~~~

.. autoclass:: Invite()
    :members:
    :inherited-members:

PartialInviteGuild
~~~~~~~~~~~~~~~~~~

.. autoclass:: PartialInviteGuild()
    :members:
    :inherited-members:

PartialInviteChannel
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: PartialInviteChannel()
    :members:
    :inherited-members:

PartialInviteApplication
~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: PartialInviteApplication()
    :members:
    :inherited-members:
