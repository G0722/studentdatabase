class Student():

    # constructor: one dict variable called info
    def __init__(self, info):
        self.info = info

    # handles edit operation. replaces old dict with input dict
    def edit(self,info):
        if info == None:
            return
        self.info = info

    # str defition for the purposes of outputting to the db.txt file
    def __str__(self,):
        info = self.info
        s = ''
        for i in info:
            s += str(f'{info[i]}, ')
        s = s.strip(', ')
        s += '\n'
        return s
