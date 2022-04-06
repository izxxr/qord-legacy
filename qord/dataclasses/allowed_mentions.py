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

import typing

__all__ = (
    "AllowedMentions",
)

class AllowedMentions:
    """Represents the allowed mentions of a message.

    Allowed mentions are used to control the behaviour of mentions done
    in messages that are sent by the bot. You can toggle the mentions
    that should be parsed in the message content.

    Parameters
    ----------
    users: :class:`builtins.bool`
        Whether to enable users mentions in the messages.
    roles: :class:`builtins.bool`
        Whether to enable roles mentions in the messages.
    everyone: :class:`builtins.bool`
        Whether to enable mentions for @everyone/@here in messages.
    replied_user: :class:`builtins.bool`
        Whether to mention the author of replied message in messages
        that contain a reply.
    mentioned_roles: Sequence[:class:`builtins.int`]
        The list of role IDs to mention in the messages. Can contain maximum
        of 100 role IDs. Duplicate IDs will be removed.
    mentioned_users: Sequence[:class:`builtins.int`]
        The list of user IDs to mention in the messages. Can contain maximum
        of 100 user IDs. Duplicate IDs will be removed.
    """

    def __init__(
        self,
        *,
        users: bool = False,
        roles: bool = False,
        everyone: bool = False,
        replied_user: bool = False,
        mentioned_roles: typing.Optional[typing.Sequence[int]] = None,
        mentioned_users: typing.Optional[typing.Sequence[int]] = None,
    ) -> None:

        self._mentioned_roles = set(mentioned_roles) if mentioned_roles is not None else set()
        self._mentioned_users = set(mentioned_users) if mentioned_users is not None else set()

        if len(self._mentioned_roles) > 100 or len(self._mentioned_users) > 100:
            raise ValueError("mentioned_roles and mentioned_users length cannot be greater then 100.")

        self.users = users
        self.roles = roles
        self.everyone = everyone
        self.replied_user = replied_user

    @property
    def mentioned_roles(self) -> typing.Set[int]:
        """The roles that are allowed to be mentioned.

        Returns
        -------
        typing.Set[:class:`builtins.int`]
        """
        return self._mentioned_roles.copy()

    def add_role(self, role_id: int) -> None:
        """Adds a role ID to the set of mentioned roles.

        Parameters
        ----------
        role_id: :class:`builtins.int`
            The ID of role to add.

        Raises
        ------
        ValueError
            Roles limit has reached.
        """
        if len(self._mentioned_roles) == 100:
            raise ValueError("Role mentions cannot contain more than 100 roles.")

        self._mentioned_roles.add(role_id)


    def remove_role(self, role_id: int) -> None:
        """Removes a role ID from the set of mentioned roles.

        If the role ID does not exist, No error is raised.

        Parameters
        ----------
        role_id: :class:`builtins.int`
            The ID of role to remove.
        """
        try:
            self._mentioned_roles.remove(role_id)
        except KeyError:
            return

    @property
    def mentioned_users(self) -> typing.Set[int]:
        """The users that are allowed to be mentioned.

        Returns
        -------
        typing.Set[:class:`builtins.int`]
        """
        return self._mentioned_roles.copy()

    def add_user(self, user_id: int) -> None:
        """Adds a user ID to the set of mentioned users.

        Parameters
        ----------
        user_id: :class:`builtins.int`
            The ID of user to add.

        Raises
        ------
        ValueError
            Users limit has reached.
        """
        if len(self._mentioned_users) == 100:
            raise ValueError("User mentions cannot contain more than 100 users.")

        self._mentioned_users.add(user_id)

    def remove_user(self, user_id: int) -> None:
        """Removes a user ID from the set of mentioned users.

        If the user ID does not exist, No error is raised.

        Parameters
        ----------
        user_id: :class:`builtins.int`
            The ID of user to remove.
        """
        try:
            self._mentioned_users.remove(user_id)
        except KeyError:
            return

    @classmethod
    def all(cls) -> AllowedMentions:
        """Creates a :class:`AllowedMentions` with all options enabled."""
        return cls(
            users=True,
            roles=True,
            everyone=True,
            replied_user=True,
        )

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        ret = {
            "replied_user": self.replied_user,
            "roles": list(self._mentioned_roles),
            "users": list(self._mentioned_users),
        }

        parse = []

        if self.users:
            parse.append("users")
            # When user mentions are parsed, passing explicit user IDs
            # will cause validation error so we will remove user IDs
            ret.pop("users")
        if self.roles:
            parse.append("roles")
            # Same case as above applies here.
            ret.pop("roles")
        if self.everyone:
            parse.append("everyone")

        ret["parse"] = parse
        return ret
