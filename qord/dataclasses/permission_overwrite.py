# MIT License

# Copyright (c) 2022 Izhar Ahmad

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

from qord.flags.permissions import Permissions
import typing

if typing.TYPE_CHECKING:
    _OverwriteValue = typing.Optional[bool]


__all__ = (
    "PermissionOverwrite",
)


class PermissionOverwrite:
    """A class representing the permissions overwrite on a guild channel.

    This class allows you to create permission overwrites that you can
    apply on guild channels.

    While initializing, this class takes the same keyword parameters as
    :class:`Permissions` i.e permissions. The permissions have their default
    value set to ``None`` indicating that no override is configured for the
    permission. The values of ``True`` and ``False`` explicitly indicates the
    allow and deny of the permission, respectively.

    This class supports equality operation with other :class:`PermissionOverwrite`
    instances to check if both have same overrides.
    """
    if typing.TYPE_CHECKING:
        create_instant_invite: _OverwriteValue
        kick_members: _OverwriteValue
        ban_members: _OverwriteValue
        administrator: _OverwriteValue
        manage_channels: _OverwriteValue
        manage_guild: _OverwriteValue
        add_reactions: _OverwriteValue
        view_audit_log: _OverwriteValue
        priority_speaker: _OverwriteValue
        stream: _OverwriteValue
        view_channel: _OverwriteValue
        send_messages: _OverwriteValue
        send_tts_messages: _OverwriteValue
        manage_messages: _OverwriteValue
        embed_links: _OverwriteValue
        attach_files: _OverwriteValue
        read_message_history: _OverwriteValue
        mention_everyone: _OverwriteValue
        use_external_emojis: _OverwriteValue
        view_guild_insights: _OverwriteValue
        connect: _OverwriteValue
        speak: _OverwriteValue
        mute_members: _OverwriteValue
        deafen_members: _OverwriteValue
        move_members: _OverwriteValue
        use_vad: _OverwriteValue
        change_nickname: _OverwriteValue
        manage_nicknames: _OverwriteValue
        manage_roles: _OverwriteValue
        manage_permissions: _OverwriteValue
        manage_webhooks: _OverwriteValue
        manage_emojis_and_stickers: _OverwriteValue
        use_application_commands: _OverwriteValue
        request_to_speak: _OverwriteValue
        manage_events: _OverwriteValue
        manage_threads: _OverwriteValue
        create_public_threads: _OverwriteValue
        create_private_threads: _OverwriteValue
        use_external_stickers: _OverwriteValue
        send_messages_in_threads: _OverwriteValue
        start_embedded_activities: _OverwriteValue
        moderate_members: _OverwriteValue

    def __init__(self, **permissions: _OverwriteValue) -> None:
        invalid = set(permissions).difference(Permissions.__name_value_map__)

        if invalid:
            raise TypeError(f"Invalid parameters for PermissionOverwrite(): {', '.join(invalid)}")

        self._overrides: typing.Dict[str, _OverwriteValue] = {}

        for permission, value in permissions.items():
            if value is None:
                continue
            elif value is True:
                self._overrides[permission] = value
            elif value is False:
                self._overrides[permission] = value
            else:
                raise TypeError(f"The value for parameter {permission!r} must be a bool or None.")

    def __eq__(self, other: typing.Any) -> bool:
        return isinstance(other, PermissionOverwrite) and other._overrides == self._overrides

    def __repr__(self) -> str:
        # _overrides mapping only includes the permissions that are explicitly
        # overriden by the overwrite.
        overrides = self._overrides
        return f"PermissionOverwrite({', '.join(f'{k}={v}' for k, v in overrides.items())})"

    def permissions(self) -> typing.Tuple[Permissions, Permissions]:
        """Returns the (allow, deny) tuple for the overwrite.

        The first element of the tuple is :class:`Permissions` instance
        with all permissions set to ``True`` that are explicitly allowed
        by this overwrite. The second element is :class:`Permissions` with
        all permissions set to ``True`` that are explicitly denied in the
        overwrite.

        Returns
        -------
        Tuple[:class:`Permissions`, :class:`Permissions`]
        """

        allow = Permissions()
        deny = Permissions()

        for permission, override in self._overrides.items():
            if override is True:
                allow._apply(permission, True)
            elif override is False:
                deny._apply(permission, True)

        return allow, deny

    @classmethod
    def from_permissions(cls: typing.Type[PermissionOverwrite], allow: Permissions, deny: Permissions) ->  PermissionOverwrite:
        """Creates a :class:`PermissionOverwrite` with the given pair of permissions.

        Parameters
        ----------
        allow: :class:`Permissions`
            The permissions with all permissions set to ``True`` that are
            explicitly allowed in the overwrite.
        deny: :class:`Permissions`
            The permissions with all permissions set to ``True`` that are
            explicitly denied in the overwrite.

        Returns
        -------
        :class:`PermissionOverwrite`
        """

        overwrite = cls()
        overrides = overwrite._overrides

        # TODO: Is there a faster alternative to this?

        for permission in Permissions.__name_value_map__:
            if allow._has(permission):
                overrides[permission] = True
            elif deny._has(permission):
                overrides[permission] = False

        return overwrite

# Setting default values on PermissionOverwrite object
for permission in Permissions.__name_value_map__:
    # Since 'permission' value can change during this for loop, we have to
    # pass it in fget and fset as a default parameter to have the correct
    # value in getter and setter.
    def fget(self, permission=permission):
        return self._overrides.get(permission)

    def fset(self, value, permission=permission):
        if value is not None and not isinstance(value, bool):
            raise TypeError(f"The value for {permission!r} must be a bool or None.")

        if value is None:
            self._overrides.pop(permission, None)
        else:
            self._overrides[permission] = value

    prop = property(
        fget=fget,
        fset=fset,
        doc=f"Overwrite value for :attr:`~Permissions.{permission}` permission."
    )
    setattr(PermissionOverwrite, permission, prop)
