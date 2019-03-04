import os
import stat


PERMISSIONS = {
    # User permissions
    'user': {
        'read': stat.S_IRUSR,
        'write': stat.S_IWUSR,
        'execute': stat.S_IXUSR,
        'all': stat.S_IRWXU,
    },

    # Group permissions
    'group': {
        'read': stat.S_IRGRP,
        'write': stat.S_IWGRP,
        'execute': stat.S_IXGRP,
        'all': stat.S_IRWXG,
    },

    # Other permissions
    'other': {
        'read': stat.S_IROTH,
        'write': stat.S_IWOTH,
        'execute': stat.S_IXOTH,
        'all': stat.S_IRWXO,
    }
}


def make_octal_permissions_mode(user=(False, False, False), group=(False, False, False), other=(False, False, False)):
    """
    Create a permissions bit in absolute notation (octal).

    The user, group and other parameters are tuples representing Read, Write and Execute values.
    All are set disallowed (set to false) by default and can be individually permitted.

    :param user: User permissions
    :param group: Group permissions
    :param other: Other permissions
    :return: Permissions bit
    """
    # Create single digit code for each name
    mode = ''
    for name in (user, group, other):
        read, write, execute = name

        # Execute
        if execute and not all(i for i in (read, write)):
            code = 1

        # Write
        elif write and not all(i for i in (read, execute)):
            code = 2

        # Write & Execute
        elif all(i for i in (write, execute)) and not read:
            code = 3

        # Read
        elif read and not all(i for i in (write, execute)):
            code = 4

        # Read & Execute
        elif all(i for i in (read, execute)) and not write:
            code = 5

        # Read & Write
        elif all(i for i in (read, write)) and not execute:
            code = 6

        # Read, Write & Execute
        elif all(i for i in (read, write, execute)):
            code = 7
        else:
            code = 0
        mode += str(code)
    return int(mode)


def set_permissions_mode_from_octal(file_path, code):
    """
    Set permissions for a file or directory.

    :param file_path: Path to a file or directory
    :param code: Permission code in absolute notation (octal)
    :return:
    """
    # Unpack permissions tuple
    user, group, other = tuple(str(code[-3:])) if len(str(code)) > 3 else tuple(str(code))
    user, group, other = int(user), int(group), int(other)
    mode = get_permissions_mode(user,
                                'user') & get_permissions_mode(group, 'group') & get_permissions_mode(other, 'other')
    os.chmod(file_path, mode)


def get_permissions_mode(permission_octal, name):
    """Retrieve a user name group permissions bitwise code."""
    read = PERMISSIONS[name]['read']
    write = PERMISSIONS[name]['write']
    execute = PERMISSIONS[name]['execute']

    # Read
    if permission_octal == 4:
        return read & ~write & ~execute

    # Write
    elif permission_octal == 2:
        return ~read & write & ~execute

    # Execute
    elif permission_octal == 1:
        return ~read & ~write & execute

    # Read & Write
    elif permission_octal == 6:
        return read & write & ~execute

    # Read & Execute
    elif permission_octal == 5:
        return read & ~write & execute

    # Write & Execute
    elif permission_octal == 3:
        return ~read & write & execute

    # Read, Write & Execute
    elif permission_octal == 7:
        return read & write & execute

    # No read, write or execute by default
    else:
        return ~read & ~write & ~execute


class Permissions:
    def __init__(self, file_path):
        self.file_path = file_path

    @property
    def octal(self):
        """Return file permissions in absolute notation (octal) format."""
        return stat.S_IMODE(os.lstat(self.file_path).st_mode)

    def allow(self, privilege):
        """Add an allowed privilege (read, write, execute, all)."""
        assert privilege in PERMISSIONS['user'].keys()
        reading = PERMISSIONS['user'][privilege] + PERMISSIONS['group'][privilege] + PERMISSIONS['other'][privilege]
        os.chmod(self.file_path, reading)

    def allow_readonly(self):
        """Add an allowed privilege (read, write, execute, all)."""
        os.chmod(self.file_path, 0o777)

    def allow_rwe(self, name):
        """Allow all privileges for a particular name group (user, group, other)."""
        assert name in PERMISSIONS.keys()
        os.chmod(self.file_path, PERMISSIONS[name]['all'])

    def revoke_access(self):
        """Revoke all access to this path."""
        reading = PERMISSIONS['user']['execute'] + PERMISSIONS['group']['execute'] + PERMISSIONS['other']['execute']
        os.chmod(self.file_path, reading)
