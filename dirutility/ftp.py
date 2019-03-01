# Connect to a server via FTP and execute commands
import os
import ftplib


class FTP:
    def __init__(self, host, port, username, password):
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
        self._session.quit()
        return True

    def close(self):
        """Close the connection unilaterally, FTP instance is unusable after call."""
        self._session.close()
        return True

    def put(self, src, dst):
        """Upload a local file a specific directory on an FTP server."""
        # Destination directory
        dst_dir = os.path.dirname(dst)

        # Destination file name
        dst_file = os.path.basename(dst)

        # File upload command
        dst_cmd = 'STOR {0}'.format(dst_file)

        with open(src, 'rb') as local_file:
            # Change directory if needed
            if dst_dir != dst_file:
                self.chdir(dst_dir)

            # Upload file
            self._session.storbinary(dst_cmd, local_file)

            # Reset current working directory to root
            self._session.cwd('/')

    def chdir(self, directory_path):
        """Change directories - create if it doesn't exist."""
        for directory in directory_path.split(os.sep):
            # print(self.session.pwd(), directory)
            if not self.directory_exists(directory):
                try:
                    self._session.mkd(directory)
                except ftplib.error_perm:
                    # Directory already exists
                    pass
            self._session.cwd(directory)

    def directory_exists(self, directory):
        """Check if directory exists (in current location)"""
        file_list = []
        self._session.retrlines('LIST', file_list.append)
        return any(f.split()[-1] == directory and f.upper().startswith('D') for f in file_list)
