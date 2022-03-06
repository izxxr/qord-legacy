.. currentmodule:: qord

Events API Reference
====================

Qord implements a rich interface for handling the events sent by Discord
over gateway. These events are generally used to track the state of various
entities.

The recommended way to register an event listener, is to use the :meth:`Client.event`
decorator to decorate the callback coroutine. Example::

    @client.event(qord.GatewayEvent.MESSAGE_CREATE)
    async def on_message_create(event):
        pass

The :class:`GatewayEvent` enumeration details the event names that are sent over gateway.

.. note::
    Toggling certain :class:`Intents` flags will also disable or enable related
    events to that intent for your bot. It is recommended to keep at least the
    :attr:`Intents.guilds` intent enabled for proper functioning of libary.

Custom events
~~~~~~~~~~~~~

Custom events are useful for several use cases and library allows you to create
them and easily invoke them::

    from qord import events
    from dataclasses import dataclass

    # For `event_name` parameter, make sure not to use an existing
    # event name reserved by the library.

    @dataclass
    class ApplicationSubmit(events.BaseEvent, event_name="application_submit"):
        id: int
        name: str

    @client.event("application_submit")
    async def on_application_submit(event):
        print("Application submitted.")
        print(f"Name: {event.name}")
        print(f"ID: {event.id}")

You can then invoke the event somewhere else::

    event = ApplicationSubmit(id=1, name="Jake")
    client.invoke_event(event)


BaseEvent
~~~~~~~~~

.. autoclass:: qord.events.BaseEvent()
    :members:

BaseGatewayEvent
~~~~~~~~~~~~~~~~

.. autoclass:: qord.events.BaseGatewayEvent()
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
