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

# Thanks to discord.py for being a good base design for Flags.
# This is inspired by discord.py

class Flags:
    r"""A class that interfaces manipulating bitwise flags.

    This class provides a user friendly way of interacting with bitwise values
    returned by Discord. The most common example is :class:`Permissions`.

    This class is documented for allowing users to create custom flags classes. The
    way this class works can be described by the example below::

        class MyFlags(qord.Flags):
            foo = 1 << 0
            bar = 1 << 2
            baz = 1 << 3
            bac = 1 << 4

        >>> flags = MyFlags(foo=True, bar=False)
        >>> flags.foo
        True
        >>> flags.bar
        False
        >>> flags.value
        5
        >>> flags = MyFlags(5)
        >>> flags.foo
        True
        >>> flags.bar
        False
        >>> flags.bar = False
        >>> flags.value
        1

    When initializing, Either a bitwise value can be passed as first positional argument
    or flags can be toggled using :class:`builtins.bool`. Accessing a flag from
    non-initialized flags class returns it's raw value.

    .. tip::
        This class also supports comparison with other :class:`Flags` instances
        as well as :class:`~builtins.int` casting. On iterating, Yields the flag
        name and it's toggle as :class:`~builtins.bool`.

    .. note::
        The parameters documented below are passed during subclassing this class.

    Parameters
    ----------
    ignore_extraneous: :class:`builtins.bool`
        Whether to ignore extra flags passed during initalization and not
        raise :exc:`TypeError`. Defaults to ``False``.

    Attributes
    ----------
    value: :class:`builtins.int`
        The raw flags value.
    """
    __name_value_map__: typing.Dict[str, int]
    __flags_settings__: typing.Dict[str, typing.Any]


    def __init__(self, value: int = 0, **flags: bool) -> None:
        self.value = value

        ignore_extraneous = self.__flags_settings__.get("ignore_extraneous", False)

        for flag, toggle in flags.items():
            if not flag in self.__name_value_map__ and not ignore_extraneous:
                raise TypeError(f"{flag} is not a valid flag for {self.__class__.__name__}()")

            self._apply(flag, toggle)

    def _apply(self, flag: str, toggle: bool):
        value = self.__name_value_map__[flag]

        if toggle is True:
            self.value |= value
        elif toggle is False:
            self.value &= ~value
        else:
            raise TypeError(f"{flag} value must be a bool, Not {toggle.__class__!r}")

    def _has(self, flag: str) -> bool:
        value = self.__name_value_map__[flag]
        return (self.value & value) > 0

    def __init_subclass__(cls, ignore_extraneous: bool = False) -> None:
        nv_map = {}

        for name, value in vars(cls).items():
            if name.startswith("_") or not isinstance(value, int):
                continue

            nv_map[name] = value
            setattr(cls, name, _Flag(name, value))

        cls.__name_value_map__ = nv_map
        cls.__flags_settings__ = {"ignore_extraneous": ignore_extraneous}

    def __int__(self) -> int:
        return self.value

    def __iter__(self) -> typing.Iterator[typing.Tuple[str, bool]]:
        for name in self.__name_value_map__:
            yield name, getattr(self, name)

    def __repr__(self) -> str:
        flags = list(self.__name_value_map__.keys())
        ret = f"{self.__class__.__name__}(%s)"
        return ret % (", ".join(f"{k}={self._has(k)}" for k in flags))

    __eq__ = lambda self, other: isinstance(other, self.__class__) and self.value == other.value # type: ignore
    __ne__ = lambda self, other: isinstance(other, self.__class__) and self.value != other.value # type: ignore
    __lt__ = lambda self, other: isinstance(other, self.__class__) and self.value < other.value
    __le__ = lambda self, other: isinstance(other, self.__class__) and self.value <= other.value
    __gt__ = lambda self, other: isinstance(other, self.__class__) and self.value > other.value
    __ge__ = lambda self, other: isinstance(other, self.__class__) and self.value >= other.value

class _Flag:
    def __init__(self, name: str, value: int) -> None:
        self.name = name
        self.value = value

    def __get__(self, instance: typing.Optional[Flags], owner: typing.Type[Flags]) -> typing.Union[int, bool]:
        if instance is None:
            return self.value

        return (instance.value & self.value > 0)

    def __set__(self, instance: typing.Optional[Flags], toggle: bool) -> None:
        if instance is None:
            raise AttributeError("Cannot set this attribute on non-instansiated Flags class.")

        instance._apply(self.name, toggle)
