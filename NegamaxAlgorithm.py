import copy
class State:
    def __init__(self, data=None, N=3):
        self.data = data
        self.N = N
    
    def close(self):
        sn = copy.deepcopy(self)
        return sn

    def Print(self):
        sz = self.N
        for i in range(sz):
            for j in range(sz):
                tmp = self.data[i * sz + j]
                if tmp == 0:
                    print('_', end='')
                elif tmp == 1:
                    print('o', end='')
                else:
                    print('x', end='')
            print()
        print("==============")

class Operator:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def Move(self, s):
        sz = s.N
        x = self.x
        y = self.y
        if x < 0 or x >= sz:
            return None
        
        