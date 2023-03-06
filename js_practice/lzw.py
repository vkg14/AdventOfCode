from dataclasses import dataclass, field
from typing import Dict
from struct import pack
from sys import getsizeof


def read_chunks(filename, chunk_size=1):
    """
    Generator to read chunks (of 1 byte by default). Why is this so slow?
    """
    with open(filename) as f:
        nxt = f.read(chunk_size)
        while nxt:
            yield nxt
            nxt = f.read(chunk_size)


@dataclass
class TrieNode:
    encoding: int
    depth: int
    children: Dict[str, 'TrieNode'] = field(default_factory=dict)


class LZW:
    MAX_LENGTH = 100
    MAX_ENCODINGS = 2**16  # To fit in a 2-byte struct pack.

    def encode_trie(self, filename):
        """
        Use LZW algorithm and build prefix tree to prevent repeated storage of characters.
        Pack each code into 2 bytes (unsigned short, H) and write to a binary file.
        Since we are packing each code into 2 bytes, we can fit values from [0, 2^16).
        """
        root = TrieNode(encoding=-1, depth=0)
        for i in range(256):
            root.children[chr(i)] = TrieNode(encoding=i, depth=1)
        encoding = []
        encoded_file = 'outputs/encoded_trie'
        nxt_i = 256
        curr = root
        with open(encoded_file, 'wb') as ef:
            for c in read_chunks(filename):
                if c not in curr.children:
                    encoding.append(curr.encoding)
                    ef.write(pack('>H', curr.encoding))
                    if nxt_i < self.MAX_ENCODINGS and curr.depth < self.MAX_LENGTH:
                        # Only create a child if within max_depth and max_encodings bounds
                        curr.children[c] = TrieNode(encoding=nxt_i, depth=curr.depth + 1)
                        nxt_i += 1
                    curr = root.children[c]
                else:
                    # Move down tree since curr has a child associated with character c
                    curr = curr.children[c]
            if curr.depth > 0:
                encoding.append(curr.encoding)
                ef.write(pack('>H', curr.encoding))
        print(f'Trie is {getsizeof(root)} bytes')
        return encoding

    def encode_dict(self, filename):
        # Assuming ASCII
        d = {chr(i): i for i in range(256)}
        encoded_file = 'outputs/encoded_dict'
        builder = ""
        encoded = []
        nxt_i = 256
        with open(encoded_file, 'wb') as ef:
            for c in read_chunks(filename):
                nxt_builder = builder + c
                if nxt_builder in d:
                    builder = nxt_builder
                else:
                    # Seeing string for the first time, previous iteration string in dictionary
                    encoded.append(d[builder])
                    ef.write(pack('>H', encoded[-1]))
                    if len(builder) < self.MAX_LENGTH and nxt_i < self.MAX_ENCODINGS:
                        d[nxt_builder] = nxt_i
                        nxt_i += 1
                    builder = c
            # Cover the last character or the last string, which is guaranteed to be in the dictionary
            if builder:
                encoded.append(d[builder])
                ef.write(pack('>H', encoded[-1]))
        print(f'Dict is {getsizeof(d)} bytes')
        return encoded

    @staticmethod
    def decode(encoded):
        d = {i: chr(i) for i in range(256)}
        decoded = [d[encoded[0]]]
        nxt_i = 256
        for i in range(1, len(encoded)):
            nxt = encoded[i]
            if nxt not in d:
                # This means that the next pattern is the one that was *just* recorded
                # Implies: the pattern started and ended with same character
                decoded.append(decoded[-1] + decoded[-1][0])
            else:
                decoded.append(d[nxt])
            # Second to last entry with the first char of the last entry
            d[nxt_i] = decoded[-2] + decoded[-1][0]
            nxt_i += 1
        return ''.join(decoded)


if __name__ == '__main__':
    lzw = LZW()
    input_file = "inputs/pg-huckleberry_finn.txt"
    # input_file = "inputs/example_lzw.txt"
    encoded_t = lzw.encode_trie(input_file)
    encoded_d = lzw.encode_dict(input_file)
    decoded = lzw.decode(encoded_t)
    print(f'Trie encoded length is {len(encoded_t)}.')
    print(f'Dict encoded length is {len(encoded_d)}.')
    assert encoded_d == encoded_t, f"Expected these to be equal\n{encoded_t}\n{encoded_d}"
