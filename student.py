class Student():

    def __init__(self, info):
        self.info = info


    def edit(self,info):
        if info == None:
            return
        self.info = info

    def __str__(self,):
        info = self.info
        s = ''
        for i in info:
            s += str(f'{info[i]}, ')
        s = s.strip(', ')
        s += '\n'
        return s
