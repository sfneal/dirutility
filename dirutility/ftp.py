# Connect to a server via FTP and execute commands
import ftplib
import os


class FTP:
    def __init__(self, host, username, password, port=21):
        self._session = self.connect(host, port, username, password)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    @property
    def session(self):
        """Return ftplib.FTP object to give exposure to methods."""
        return self._session

    @staticmethod
    def connect(host, port, username, password):
        """Connect and login to an FTP server and return ftplib.FTP object."""
        # Instantiate ftplib client
        session = ftplib.FTP()

        # Connect to host without auth
        session.connect(host, port)

        # Authenticate connection
        session.login(username, password)
        return session

    def disconnect(self):
        """Send a QUIT command to the server and close the connection (polite way)."""
        self.session.quit()
        return True

    def close(self):
        """Close the connection unilaterally, FTP instance is unusable after call."""
        self.session.close()
        return True

    def put(self, local, remote):
        """Upload a local file to a directory on the remote ftp server."""
        return self._store_binary(local, remote)

    def get(self, remote, local=None, keep_dir_structure=False):
        """
        Download a remote file on the fto sever to a local directory.

        :param remote: File path of remote source file
        :param local: Directory of local destination directory
        :param keep_dir_structure: If True, replicates the remote files folder structure
        """
        if local and os.path.isdir(local):
            os.chdir(local)

        elif keep_dir_structure:
            # Replicate the remote files folder structure
            for directory in remote.split(os.sep)[:-1]:
                if not os.path.isdir(directory):
                    os.mkdir(directory)
                os.chdir(directory)

        # Change to the correct directory if remote is a path not just a name
        if os.sep in remote:
            directory, file_name = remote.rsplit(os.sep, 1)
            self.chdir(directory)
        else:
            file_name = remote

        # Download the file and get response
        response = self._retrieve_binary(file_name)

        # Rename downloaded files if local is a file_name string
        if local and isinstance(local, str):
            os.rename(file_name, local)
        return response

    def chdir(self, directory_path, make=False):
        """Change directories and optionally make the directory if it doesn't exist."""
        if os.sep in directory_path:
            for directory in directory_path.split(os.sep):
                if make and not self.directory_exists(directory):
                    try:
                        self.session.mkd(directory)
                    except ftplib.error_perm:
                        # Directory already exists
                        pass
                self.session.cwd(directory)
        else:
            self.session.cwd(directory_path)

    def listdir(self, directory_path=None, hidden_files=False):
        """
        Return a list of files and directories in a given directory.

        :param directory_path: Optional str (defaults to current directory)
        :param hidden_files: Include hidden files
        :return: Directory listing
        """
        # Change current directory if a directory path is specified, otherwise use current
        if directory_path:
            self.chdir(directory_path)

        # Exclude hidden files
        if not hidden_files:
            return [path for path in self.session.nlst() if not path.startswith('.')]

        # Include hidden files
        else:
            return self.session.nlst()

    def rename(self, from_name, to_name):
        """Rename a file from_name on the server to to_name."""
        return self.session.rename(from_name, to_name)

    def delete(self, file_path):
        """Remove the file named filename from the server."""
        if os.sep in file_path:
            directory, file_name = file_path.rsplit(os.sep, 1)
            self.chdir(directory)
            return self.session.delete(file_name)

        else:
            return self.session.delete(file_path)

    def directory_exists(self, directory):
        """Check if directory exists (in current location)"""
        file_list = []
        self.session.retrlines('LIST', file_list.append)
        return any(f.split()[-1] == directory and f.upper().startswith('D') for f in file_list)

    def set_verbosity(self, level):
        """Set the instance’s debugging level, controls the amount of debugging output printed."""
        self.session.set_debuglevel(level)

    def _retrieve_binary(self, file_name):
        """Retrieve a file in binary transfer mode."""
        with open(file_name, 'wb') as f:
            return self.session.retrbinary('RETR ' + file_name, f.write)

    def _store_binary(self, local_path, remote):
        """Store a file in binary via ftp."""
        # Destination directory
        dst_dir = os.path.dirname(remote)

        # Destination file name
        dst_file = os.path.basename(remote)

        # File upload command
        dst_cmd = 'STOR {0}'.format(dst_file)

        with open(local_path, 'rb') as local_file:
            # Change directory if needed
            if dst_dir != dst_file:
                self.chdir(dst_dir, make=True)

            # Upload file & return response
            return self.session.storbinary(dst_cmd, local_file)
