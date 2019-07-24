class TextDump:
    def __init__(self, file_path):
        self.file_path = file_path

    @staticmethod
    def _encode_data(data):
        """Encode data as a string in order to write to a text file."""
        if isinstance(data, (list, tuple, set)):
            return '\n'.join(data)
        else:
            return data

    def read(self):
        with open(self.file_path, 'r') as txt:
            return txt.read()

    def write(self, data):
        with open(self.file_path, 'w') as txt:
            return txt.write(self._encode_data(data))

    def append(self, data):
        with open(self.file_path, 'a') as txt:
            return txt.write(self._encode_data(data))
