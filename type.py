class Symbol:
    def __init__(self, name):
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name


class ArrayIterator:
    def __init__(self, arr):
        self.max_num = len(arr)
        self.arr = arr
        self.index = 0

    def __iter__(self):
        return self

    def has_next(self):
        return self.index < self.max_num

    def next(self):
        self.index += 1
        if self.index < self.max_num:
            return self.arr[self.index]
        else:
            raise StopIteration

    def __next__(self):
        return self.next()
