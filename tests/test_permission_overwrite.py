"""Tests for qord.PermissionOverwrite"""

from qord import PermissionOverwrite, Permissions
import unittest


class TestPermissionOverwrite(unittest.TestCase):
    def test_attrs_comparison(self):
        overwrite = PermissionOverwrite()

        overwrite.send_messages = True
        overwrite.manage_channels = False

        overwrite2 = PermissionOverwrite(send_messages=True, manage_channels=False)
        assert overwrite2 == overwrite

    def test_pairs(self):
        overwrite = PermissionOverwrite(
            manage_channels=True,
            manage_messages=True,
            send_messages=False,
            connect=False,
        )

        allow = Permissions(manage_channels=True, manage_messages=True)
        deny = Permissions(send_messages=True, connect=True)

        overwrite_allow, overwrite_deny = overwrite.permissions()

        assert overwrite_allow == allow
        assert overwrite_deny == deny

        overwrite_with_permissions = PermissionOverwrite.from_permissions(allow, deny)
        assert overwrite_with_permissions == overwrite

if __name__ == "__main__":
    unittest.main()