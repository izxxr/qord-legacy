.. currentmodule:: qord

Releases
========

This page details the changelog containing every notable change of every releases.

- The release with "Unreleased" in title indicates that the release is not yet released and is under development.
- The releases with "Pre-release" in title or if the version ends with an identifier, It indicates that the release was a pre-release.

v0.3.0
------

Additions
~~~~~~~~~

- Added support for custom guild emojis.
- Added support for message reactions.
- Added :attr:`Guild.me` property for retreiving bot member.
- Added :attr:`created_at` property on appropriate Discord models.
- Added :meth:`~BaseMessageChannel.messages` method to iterate through channels history.
- Added :meth:`Guild.members` method to iterate through guild members.
- Added :attr:`PrivateChannel.url`, :attr:`GuildChannel.url` and :attr:`Message.url` properties
- Added :meth:`BaseMessageChannel.trigger_typing` and :meth:`BaseMessageChannel.typing` for working with typing indicators.
- Added :meth:`Message.crosspost` for crossposting messages in news channels.

Changes
~~~~~~~~

- :class:`ChannelPermission` now supports equality comparisons.
- All models now shows useful information in :func:`repr()`

Bug fixes
~~~~~~~~~

- Fixed  :attr:`Embed.video` property running into infinite loop.
- Fixed disparity between ``embed`` and ``embeds`` parameters in :meth:`~BaseMessageChannel.send`
- Fixed typing of :attr:`Message.channel` not including DM channels.

v0.3.0a2 (Pre-release)
----------------------

Additions
~~~~~~~~~

- Added handling of HTTP ratelimits.
- Added support for channel permission overwrites.
- Added equality comparison support for various Discord models.
- Added module ``qord.utils``, see :ref:`reference-utilities` for more info.
- Added :attr:`Message.referenced_message` attribute.
- Added :func:`qord.utils.create_timestamp` helper function.
- Added :meth:`Embed.total_length` and :meth:`builtins.len()` support on :class:`Embed`
- Added ``channel`` keyword argument in :attr:`GuildMember.edit`

Improvements/Misc.
~~~~~~~~~~~~~~~~~~

- :attr:`User.mention` string no longer includes ``!``, This is done in order to comply with the recent change done to Discord client. For more information, see `this issue <https://github.com/discord/discord-api-docs/issues/4734>`_
- :attr:`DefaultCache.private_channels` cache is now bound to limit of 256 channels.
- :class:`File` constructor no longer raises :exc:`RuntimeError` on failing to resolve file name and now fallbacks to ``untitled``

Fixes
~~~~~

- Fixed cache not cleaning up on client closure.
- Fixed typing issues across the library.
    - Passing ``None`` is not supported in various places especially ``x_url()`` methods.
    - ``None`` is now allowed in ``reason`` parameters in REST methods.
    - Various methods of cache handlers now return :class:`typing.List` rather than the :attr:`typing.Sequence`
    - Other minor improvements and fixes.
- Fixed :meth:`GuildCache.roles` returning empty list for HTTP retrieved guilds.

v0.3.0a1 (Pre-release)
----------------------

Breaking Changes
~~~~~~~~~~~~~~~~~

- Event system restructure

    - Custom events are now created using BaseEvent
    - :meth:`Client.invoke_event()` now takes single BaseEvent instance.
    - BaseEvent is no longer a protocol, all custom events must inherit it.
    - New protocol class BaseGatewayEvent has been added for gateway related events.
    - MessagesSupport was renamed to BaseMessageChannel for consistency.

Additions
~~~~~~~~~

- Added :class:`MessageType` enumeration.
- Added support for message embeds.
- Added support for message allowed mentions.
- Added support for message flags.
- Added support for message references.
- Added :meth:`Message.edit()` and :meth:`Message.delete()` methods.
- Added :meth:`Shard.disconnect()` and :meth:`~Shard.reconnect()` methods.
- Added :meth:`PrivateChannel.close()` method.
- Added :attr:`Intents.message_content` privileged intent flag.
- Added support for embeds, files and other options in :meth:`~BaseMessageChannel.send()`

Fixes
~~~~~

- Fix various crashes on startup.
- Fix minor bugs.

Improvements
~~~~~~~~~~~~

- Startup time has minor improvements.
- Library is now completely typed, there may be breaking type changes.

v0.2.0
------

Additions
~~~~~~~~~

- Added support for guild roles.
- Added support for guild members.
- Added support for permissions.
- Added support for guild channels.
- Added support for messages.
- Added :attr:`User.proper_name` property.
- Added :attr:`User.mention` property.

Improvements
~~~~~~~~~~~~

- :attr:`Guild.cache` is no longer optional.
- Startup time has been significantly improved.

Fixes
~~~~~

- Fixed :meth:`GuildCache.clear()` not getting called upon guild evictions.
- Fixed extension parameter incorrectly behaving for various URL methods.
- Fixed shards closing on receiving unhandleable OP code.
- Fixed client not properly handling graceful closure in some cases.
- Fixed :meth:`Client.launch()` raising RuntimeError upon relaunching the client after closing.


v0.2.0a1 (Pre-release)
----------------------

Additions
~~~~~~~~~

Add support for users.
Add support for guilds.
Add support for caching.

Improvements
~~~~~~~~~~~~

- Event listeners tasks now have proper exception handling.
- Various performance improvements.

Fixes
~~~~~

- Fixed wrong instance check on manually passing a client session.

v0.1.0
------

- Initial release.
