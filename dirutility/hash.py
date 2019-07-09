try:
    from hashlib import md5, sha256, sha1, blake2b, blake2s, sha512, shake_128
    from xxhash import xxh32, xxh64


    class _HashAlgos:
        def __init__(self, string):
            self.string = string

            self._md5 = None
            self._sha1 = None
            self._sha256 = None
            self._sha512 = None
            self._blake2b = None
            self._blake2s = None
            self._shake_128 = None
            self._xxh32 = None
            self._xxh64 = None

        def _get_md5(self):
            """Hash a string using the md5 algo and return in hexdigested form."""
            return md5(self.string).hexdigest()

        def _get_sha1(self):
            """Hash a string using the sha256 algo and return in hexdigested form."""
            return sha1(self.string).hexdigest()

        def _get_sha256(self):
            """Hash a string using the sha256 algo and return in hexdigested form."""
            return sha256(self.string).hexdigest()

        def _get_sha512(self):
            """Hash a string using the sha512algo and return in hexdigested form."""
            return sha512(self.string).hexdigest()

        def _get_blake2b(self):
            """Hash a string using the blake2b algo and return in hexdigested form."""
            return blake2b(self.string).hexdigest()

        def _get_blake2s(self):
            """Hash a string using the blake2b algo and return in hexdigested form."""
            return blake2s(self.string).hexdigest()

        def _get_shake_128(self):
            """Hash a string using the shake_128 algo and return in hexdigested form."""
            return shake_128(self.string).hexdigest(128)

        def _get_xxh32(self):
            """Hash a string using the xxh32 algo and return in hexdigested form."""
            return xxh32(self.string).hexdigest()

        def _get_xxh64(self):
            """Hash a string using the xxh64 algo and return in hexdigested form."""
            return xxh64(self.string).hexdigest()


    class Hash(_HashAlgos):
        def __init__(self, string):
            super(Hash, self).__init__(string)

        def md5(self):
            """Return a hexdigested md5 hash."""
            if not self._md5:
                self._md5 = self._get_md5()
            return self._md5

        def sha1(self):
            """Return a hexdigested sha256 hash."""
            if not self._sha1:
                self._sha1 = self._get_sha1()
            return self._sha1

        def sha256(self):
            """Return a hexdigested sha256 hash."""
            if not self._sha256:
                self._sha256 = self._get_sha256()
            return self._sha256

        def sha512(self):
            """Return a hexdigested sha256 hash."""
            if not self._sha512:
                self._sha512 = self._get_sha512()
            return self._sha512

        def blake2b(self):
            """Return a hexdigested blake2b hash."""
            if not self._blake2b:
                self._blake2b = self._get_blake2b()
            return self._blake2b

        def blake2s(self):
            """Return a hexdigested blake2s hash."""
            if not self._blake2s:
                self._blake2s = self._get_blake2s()
            return self._blake2s

        def shake_128(self):
            """Return a hexdigested shake_128 hash."""
            if not self._shake_128:
                self._shake_128 = self._get_shake_128()
            return self._shake_128

        def xxh32(self):
            """Return a hexdigested xxh32 hash."""
            if not self._xxh32:
                self._xxh32 = self._get_xxh32()
            return self._xxh32

        def xxh64(self):
            """Return a hexdigested xxh64 hash."""
            if not self._xxh64:
                self._xxh64 = self._get_xxh64()
            return self._xxh64

except ImportError:
    class Hash:
        def __init__(self, *args, **kwargs):
            pass
