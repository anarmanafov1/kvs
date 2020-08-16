from bloomfilter import BloomFilter
from binio import kv_iter, kv_reader, kv_writer

BF_SIZE = 10000
BF_HASH_COUNT = 5


class SSTable:
    """Represents a Sorted-String-Table (SSTable) on disk"""

    def __init__(self, path, bf=None):
        self.path = path
        self.bf = bf
        if not self.bf:
            self._sync()

    def _sync(self):
        self.bf = BloomFilter(BF_SIZE, BF_HASH_COUNT)
        for key, _ in self.entries():
            self.bf.add(key)

    @classmethod
    def create(cls, path, memtable):
        bf = BloomFilter(BF_SIZE, BF_HASH_COUNT)
        with kv_writer(path) as writer:
            for key, value in memtable.entries():
                writer.write_entry(key, value)
                bf.add(key)
        return cls(path, bf)

    def entries(self):
        yield from kv_iter(self.path)

    def search(self, search_key):
        if not self.bf.exists(search_key):
            return None
        with kv_reader(self.path) as r:
            while r.has_next():
                key = r.read_key()
                # stop if the key is too big
                if key > search_key:
                    return None
                if key == search_key:
                    return r.read_value()
                # jump to the next key
                value_size = r.read_value_size()
                if value_size > 0:
                    r.skip(value_size)
        return None
