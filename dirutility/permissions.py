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


def get_permissions_mode(permission_octal, name):
    """Retrieve a user permissions bitwise code."""
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


def get_permissions_octal(file_path):
    """Return file permissions in absolute notation (octal) format."""
    return stat.S_IMODE(os.lstat(file_path).st_mode)


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


def octal_permissions_mode(user=(False, False, False), group=(False, False, False), other=(False, False, False)):
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


def add_read_permissions(path):
    """Add read permissions from this path, while keeping all other permissions intact."""
    reading = PERMISSIONS['user']['read'] + PERMISSIONS['group']['read'] + PERMISSIONS['other']['read']
    os.chmod(path, reading)


def add_write_permissions(path):
    """Add write permissions from this path, while keeping all other permissions intact."""
    writing = PERMISSIONS['user']['write'] + PERMISSIONS['group']['write'] + PERMISSIONS['other']['write']
    os.chmod(path, writing)


def no_access_permissions(path):
    """Add read permissions from this path, while keeping all other permissions intact."""
    reading = PERMISSIONS['user']['execute'] + PERMISSIONS['group']['execute'] + PERMISSIONS['other']['execute']
    os.chmod(path, reading)


def add_rwe_user(path):
    """Add read, write & execute permissions for owner user."""
    os.chmod(path, PERMISSIONS['user']['all'])


def add_rwe_group(path):
    """Add read, write & execute permissions for group users."""
    os.chmod(path, PERMISSIONS['group']['all'])


def add_rwe_other(path):
    """Add read, write & execute permissions for all users."""
    os.chmod(path, PERMISSIONS['other']['all'])
