class Counter:
    def __init__(self, length=0):
        self.counter = 0
        self.length = length

    def __repr__(self):
        print(str(self.counter))

    def leading_zeros(self):
        if self.length == 3:
            if self.counter < 10:
                count = "00" + str(self.counter)
            elif 9 < self.counter < 100:
                count = "0" + str(self.counter)
            else:
                count = self.counter
        elif self.length == 2:
            if self.counter < 10:
                count = "0" + str(self.counter)
            else:
                count = self.counter
        else:
            count = self.counter
        return count

    @property
    def up(self):
        self.counter += 1
        count = self.leading_zeros()
        return str(count)

    @property
    def total(self):
        count = self.leading_zeros()
        return str(count)