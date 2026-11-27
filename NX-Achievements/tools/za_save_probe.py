#!/usr/bin/env python3
"""Probe a Pokemon Legends Z-A save: decrypt SwishCrypto and dump SCBlocks.

Reference implementation of the C watcher's parser. Run with a decrypted or
encrypted `main` save from JKSV.
"""
import hashlib
import struct
import sys
from pathlib import Path

INTRO = bytes.fromhex(
    '9ec99cd70ed33c44fb9303dceb39b42a'
    '1947e9634ba2334416bf82a2ba6355b6'
    '3d9df24b5f7b6ab2621dc21b68e5c8b5'
    '3a059000e8a8103de2ecf00cb2ed4f6d'
)
OUTRO = bytes.fromhex(
    'd6c01c598bc8b8cb46e153fc828c7575'
    '13e045df32693c75f059f8d9a25fb217'
    'e08052dbea8973997579afcb2e8007e6'
    'f126e0030ae66ff641bf7e59c2ae55fd'
)
XORPAD = bytes.fromhex(
    'a092d10607db32a1ae01f5c51e844fe3'
    '53ca37f4a7b04da018b7c297da5f532b'
    '75fa4816f8d48a6f6105f4e2fd04b5a3'
    '0ffc4492cb32e61bb9b12e01b0565336'
    'd2d1503dde5b2e0e52fddf2f7bca6350'
    'a4675d2317c052e1a6307c2bb670365b'
    '2a276933f5637b363f269ba3ed7a5300'
    'a448b3509e14a052de7e102b1b776e00'
)
XP = XORPAD  # 0x80 bytes, last byte is padding


def crypt_xor(data: bytearray):
    """Port of PKHeX SwishCrypto.CryptStaticXorpadBytes (including its 1-byte overlap)."""
    size = len(XORPAD) - 1  # 0x7F
    iterations = (len(data) - 1) // size
    off = 0
    for _ in range(iterations):
        for i in range(min(len(XORPAD), len(data) - off)):
            data[off + i] ^= XORPAD[i]
        off += size
    for i in range(len(data) - off - 1, -1, -1):
        data[off + i] ^= XORPAD[i]


def hash_valid(data: bytes) -> bool:
    payload, stored = data[:-32], data[-32:]
    return hashlib.sha256(INTRO + payload + OUTRO).digest() == stored


class XorShift32:
    @staticmethod
    def _advance(state: int) -> int:
        state ^= (state << 2) & 0xFFFFFFFF
        state ^= state >> 15
        state ^= (state << 13) & 0xFFFFFFFF
        return state & 0xFFFFFFFF

    def __init__(self, seed: int):
        state = seed & 0xFFFFFFFF
        for _ in range(state.bit_count()):
            state = self._advance(state)
        self.s = state
        self.counter = 0

    def next_byte(self) -> int:
        result = (self.s >> (self.counter << 3)) & 0xFF
        if self.counter == 3:
            self.s = self._advance(self.s)
            self.counter = 0
        else:
            self.counter += 1
        return result

    def next32(self) -> int:
        return (self.next_byte() | (self.next_byte() << 8) |
                (self.next_byte() << 16) | (self.next_byte() << 24)) & 0xFFFFFFFF


# SCTypeCode sizes from PKHeX.
TYPE_SIZE = {
    0x01: 0,  # Bool1
    0x02: 0,  # Bool2
    0x03: 1,  # Bool3
    0x04: 0,  # Object
    0x05: 0,  # Array
    0x08: 1,  # Byte
    0x09: 2,  # UInt16
    0x0A: 4,  # UInt32
    0x0B: 8,  # UInt64
    0x0C: 1,  # SByte
    0x0D: 2,  # Int16
    0x0E: 4,  # Int32
    0x0F: 8,  # Int64
    0x10: 4,  # Single
    0x11: 8,  # Double
}


def parse_blocks(payload: bytes):
    blocks = []
    off = 0
    n = len(payload)
    while off + 5 <= n:
        key = struct.unpack_from('<I', payload, off)[0]
        off += 4
        xk = XorShift32(key)
        typ = payload[off] ^ xk.next_byte()
        off += 1
        if typ in (0x01, 0x02):
            blocks.append((key, typ, b''))
            continue
        if typ == 0x04:  # Object
            if off + 4 > n:
                raise ValueError('truncated object length')
            size = struct.unpack_from('<I', payload, off)[0] ^ xk.next32()
            size = size - 0x100000000 if size >= 0x80000000 else size
            off += 4
            if size < 0 or off + size > n:
                raise ValueError(f'bad object size {size} at {off}')
            raw = bytearray(payload[off:off + size])
            off += size
            for i in range(len(raw)):
                raw[i] ^= xk.next_byte()
            blocks.append((key, typ, bytes(raw)))
            continue
        if typ == 0x05:  # Array
            if off + 4 > n:
                raise ValueError('truncated array length')
            count = struct.unpack_from('<I', payload, off)[0] ^ xk.next32()
            count = count - 0x100000000 if count >= 0x80000000 else count
            off += 4
            sub = payload[off] ^ xk.next_byte()
            off += 1
            sub_size = TYPE_SIZE.get(sub, 0)
            size = count * sub_size
            if size < 0 or off + size > n:
                raise ValueError(f'bad array size {size} sub={sub:#x} count={count} at {off}')
            raw = bytearray(payload[off:off + size])
            off += size
            for i in range(len(raw)):
                raw[i] ^= xk.next_byte()
            blocks.append((key, typ, bytes(raw), sub, count))
            continue
        size = TYPE_SIZE.get(typ)
        if size is None or size == 0:
            raise ValueError(f'unknown type {typ:#x} for key {key:#x} at {off}')
        raw = bytearray(payload[off:off + size])
        off += size
        for i in range(len(raw)):
            raw[i] ^= xk.next_byte()
        blocks.append((key, typ, bytes(raw)))
    return blocks, off


def main():
    for arg in sys.argv[1:]:
        path = Path(arg)
        data = path.read_bytes()
        print(f'FILE {path} size={len(data)} hashValid={hash_valid(data)}')
        payload = bytearray(data[:-32])
        crypt_xor(payload)
        try:
            blocks, consumed = parse_blocks(bytes(payload))
        except Exception as e:
            print(f'  PARSE ERROR {type(e).__name__}: {e}')
            continue
        print(f'  blocks={len(blocks)} consumed={consumed}/{len(payload)}')
        by_key = {b[0]: b for b in blocks}
        for label, key in [
            ('SaveRevision', 0x0926555A), ('Pokedex', 0x2D87BE5C),
            ('Money', 0x4F35D0DD), ('QuestWork', 0xB9B223B9),
            ('EventFlag', 0x58505C5E), ('EventWork', 0xFADA7742),
            ('InfiniteRoyale', 0x8929BFB6), ('InfiniteRank', 0x7C896A83),
            ('Clothing', 0x64235B3D), ('FashionTops', 0xD4BCE690),
            ('FashionBottoms', 0x4DCB6EBC), ('Item', 0x21C9BD44),
            ('TicketPoints', 0x9A730DE1), ('TicketPointsInf', 0x1D7EE369),
            ('PlayTime', 0xEDAFF794), ('PlayedSeconds', 0xCE3AF8F2),
        ]:
            b = by_key.get(key)
            if b is None:
                print(f'  {label:18} {key:#010x} MISSING')
                continue
            typ = b[1]
            dat = b[2]
            extra = ''
            if len(b) > 3:
                extra = f' sub={b[3]:#x} count={b[4]}'
            if typ == 0x0A and len(dat) == 4:
                extra += f' value={struct.unpack("<I", dat)[0]}'
            elif typ == 0x0B and len(dat) == 8:
                extra += f' value={struct.unpack("<Q", dat)[0]}'
            elif typ == 0x09 and len(dat) == 2:
                extra += f' value={struct.unpack("<H", dat)[0]}'
            elif typ == 0x08:
                extra += f' value={dat[0]}'
            print(f'  {label:18} {key:#010x} type={typ:#04x} len={len(dat):#x}{extra}')


if __name__ == '__main__':
    main()
