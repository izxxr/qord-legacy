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

Intents
~~~~~~~

.. autoclass:: Intents()
    :members:

UserFlags
~~~~~~~~~

.. autoclass:: UserFlags()
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
