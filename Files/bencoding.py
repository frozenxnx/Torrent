from collections import OrderedDict

TOKEN_INTEGER = b'i'
TOKEN_LIST = b'l'
TOKEN_DICT = b'd'
TOKEN_END = b'e'
TOKEN_STRING_SEPARATOR = b':'

class Decoder:
    def __init__(self, data: bytes):
        if not isinstance(data, bytes):
            raise TypeError('data must be of type bytes')
        self._data = data
        self._index = 0

    def decode(self):
        c = self._peek()
        if c is None:
            raise EOFError('Unexpected end of file')

        if c == TOKEN_INTEGER:
            self._consume()
            return self._decode_int()
        elif c == TOKEN_LIST:
            self._consume()
            return self._decode_list()
        elif c == TOKEN_DICT:
            self._consume()
            return self._decode_dict()
        elif c == TOKEN_END:
            return None
        elif c in b'0123456789':
            return self._decode_string()
        else:
            raise RuntimeError(f'Invalid token {c} at position {self._index}')

    def _peek(self):
        if self._index >= len(self._data):
            return None
        return self._data[self._index:self._index + 1]

    def _consume(self):
        self._index += 1

    def _read(self, length: int) -> bytes:
        if self._index + length > len(self._data):
            raise IndexError(f'Cannot read {length} bytes from position {self._index}')
        res = self._data[self._index:self._index + length]
        self._index += length
        return res

    def _read_until(self, token: bytes) -> bytes:
        try:
            occurrence = self._data.index(token, self._index)
            result = self._data[self._index:occurrence]
            self._index = occurrence + 1
            return result
        except ValueError:
            raise RuntimeError(f'Unable to find token {token}')

    def _decode_int(self):
        return int(self._read_until(TOKEN_END))

    def _decode_string(self):
        bytes_to_read = int(self._read_until(TOKEN_STRING_SEPARATOR))
        return self._read(bytes_to_read)

    def _decode_list(self):
        res = []
        while self._peek() != TOKEN_END:
            res.append(self.decode())
        self._consume()
        return res

    def _decode_dict(self):
        res = OrderedDict()
        while self._peek() != TOKEN_END:
            key = self.decode()
            value = self.decode()
            res[key] = value
        self._consume()
        return res



class Encoder:
        """
        Encodes a pyhton object to a bencoded sequence of bytes.

        Supported pyhton types is
          -str
          -list
          -dict
          -int
          -bytes

        Any other will be simply ignored
        """

        def __init__(self,data:bytes):
            self._data = data

        def encode(self):
            """
            Encode a python object to bencoded binary string.

            :return: The bencoded binary data.
            """
            return self.encode_next(self._data)

        def encode_next(self,data):
            if type(data) == str:
                return self._encode_string(data)

            if type(data) == list:
                return self._encode_list(data)

            if type(data) == int:
                return self._encode_int(data)

            if type(data) == bytes:
                return self._encode_bytes(data)

            if type(data) == OrderedDict or type(data) == dict:
                return self._encode_dict(data)
            else:
                return None


        def _encode_string(self,value:str):
            res = str(len(value))+ ':' +value
            return str.encode(res)

        def _encode_int(self,value):
            return str.encode('i'+str(value) + 'e')

        def _encode_bytes(self,value:str):
            result = bytearray()
            result+=str.encode(str(len(value)))
            result+=b':'
            result+=value
            return result

        def _encode_list(self,data):
            result =bytearray('l','utf-8')
            result+=b''.join([self.encode_next(item) for item in data])
            result+=b'e'
            return result


        def _encode_dict(self,data:dict)->bytes:
            result = bytearray('d','utf-8')
            for k,v in data.items():
                key = self.encode_next(k)
                value = self.encode_next(v)
                if key and value:
                    result+=key
                    result+=value
                else:
                    raise RuntimeError('Bad dict')
            result +=b'e'
            return result


















