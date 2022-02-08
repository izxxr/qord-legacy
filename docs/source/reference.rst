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


Data classes
------------

Shard
~~~~~

.. autoclass:: Shard()
    :members:

Flags
-----

Flags
~~~~~

.. autoclass:: Flags()
    :members:

Intents
~~~~~~~

.. autoclass:: Intents()
    :members:

Exceptions
----------

These are the exceptions raised by the library. All of these exceptions inherit a common
class :exc:`QordException`.

.. autoexception:: QordException()
.. autoexception:: ClientSetupRequired()
.. autoexception:: HTTPException()
.. autoexception:: HTTPBadRequest()
.. autoexception:: HTTPForbidden()
.. autoexception:: HTTPNotFound()
.. autoexception:: HTTPServerError()
.. autoexception:: ShardException()
.. autoexception:: ShardCloseException()
.. autoexception:: MissingPrivilegedIntents()
