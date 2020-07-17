from os import path
from memtable import Memtable

class CommitLog:
    def __init__(self, log_path):
        self.fd = None
        self.log_path = log_path
        self.recovered_memtable = None
        self.__resume()
     
    def __resume(self):
        # recover the memtable if necessary
        if path.exists(self.log_path):
            memtable = Memtable()
            self.fd = open(self.log_path, 'r+')
            record = self.fd.readline()
            while record:
                key, value = record.rstrip().split(',')
                if value:
                    memtable.set(key, value)
                else:
                    memtable.unset(key)
                record = self.fd.readline()
            # check if it has any data
            if memtable.approximate_bytes() > 0:
                self.recovered_memtable = memtable
        else:
            self.fd = open(self.log_path, 'w')

    def record_set(self, k, v):
        self.fd.write(f"{k},{v}\n")
        self.fd.flush()

    def record_unset(self, k):
        self.fd.write(f"{k},\n")
        self.fd.flush()

    def purge(self):
        self.fd.close()
        self.fd = open(self.log_path, 'w')

