import os
from subprocess import Popen, PIPE


class SystemCommand:
    def __init__(self, command, decode_output=True, immediate_execution=True):
        """
        Execute a system command.

        When decode_output is True, console output is captured, decoded
        and returned in list a list of strings.

        :param command: Command to execute
        :param decode_output: Optionally capture and decode console output
        :param immediate_execution: Execute system command during initialization
        :return: List of output strings
        """
        # Parameter attributes
        self.command = command
        self._decode_output = decode_output

        # Private attributes
        self._output, self._success = None, False

        # Execute command
        if immediate_execution:
            self.execute()

    def __str__(self):
        return self.command

    def __iter__(self):
        return iter(self._output)

    def __getitem__(self, item):
        return self._output[item]

    def __len__(self):
        return len(self._output)

    @property
    def output(self):
        """Return the standard output produced by execution of the system command."""
        return self._output

    @property
    def success(self):
        """Return a boolean stating weather the command has been successfully executed."""
        return self._success

    def execute(self):
        """Execute a system command."""
        if self._decode_output:
            # Capture and decode system output
            with Popen(self.command, shell=True, stdout=PIPE) as process:
                self._output = [i.decode("utf-8").strip() for i in process.stdout]
                self._success = True
        else:
            # Execute without capturing output
            os.system(self.command)
            self._success = True
        return self
