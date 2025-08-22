from Files.bencoding import Encoder,Decoder

# Integer
assert Decoder(b'i42e').decode() == 42
print("✅ Decoder passed: b'i42e' -> 42")
assert Encoder(42).encode() == b'i42e'
print("✅ Encoder passed: 42 -> b'i42e'")