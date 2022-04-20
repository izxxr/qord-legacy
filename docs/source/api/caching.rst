.. currentmodule:: qord

.. _api-caching:

Caching
=======

Caching is an important part of maintaining a stateful bot. In order to avoid excessive
API calls, The data sent over gateway by Discord is cached by the client and can be retrieved
from cache when needed rather than fetching from the API. Discord sends gateway events that
allow us to easily track updates in the cached data.


.. _api-caching-cache-handlers:

Cache Handlers
--------------

Qord provides a user friendly API for caching. By default, The library provides :ref:`default cache
handlers <api-caching-default-handlers>` that suit most of the use cases. On a large scale however, you might need to maintain
custom caching using some system such as Redis. To acheive this, There are some :ref:`abstract classes <api-caching-abstract-classes>`
provided by the library that allow you to implement custom cache handlers according to your needs.

Two different cache handlers are used by the library for caching entities sent over gateway.

- :class:`ClientCache` (Accessed through :attr:`Client.cache`)
- :class:`GuildCache` (Accessed through :attr:`Guild.cache`)

The :class:`ClientCache` handler is used for storing global entities such as guilds, users and
messages etc. It can be accessed through the :attr:`Client.cache` property.

On the other hand, the :class:`GuildCache` handler is used to store entities specific to a
:class:`Guild`. Each :class:`Guild` has a separate cache handler for storing objects
related to that guild that can be accessed by :attr:`Guild.cache` property.


.. _api-caching-abstract-classes:

Abstract classes
----------------

Methods and attributes of each of the handlers described above are documented in detail below.

ClientCache
~~~~~~~~~~~

.. autoclass:: ClientCache
    :members:

GuildCache
~~~~~~~~~~

.. autoclass:: GuildCache
    :members:

.. _api-caching-default-handlers:

Default Handlers
----------------

These classes are default implementation for caching provided by the library.

DefaultClientCache
~~~~~~~~~~~~~~~~~~

.. autoclass:: DefaultClientCache
    :members:

DefaultGuildCache
~~~~~~~~~~~~~~~~~

.. autoclass:: DefaultGuildCache
    :members:
