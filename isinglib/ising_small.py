import typing as tp


def user_while(msg: str, df: str) -> bool:
    '''Asks msg until (y/n) and sets a bool value'''
    (yes, no) = df == 'y' and (['y',''],['n']) or (['y'],['n',''])
    while True:
        temp = input(msg).lower().strip()
        if temp in yes:
            bool_stored = True
            break
        elif temp in no:
            bool_stored = False
            break
        else:
            print('Not understood, try again.')
    return bool_stored


def gread(file_data: tp.TextIO) -> tp.TextIO:
    '''Read lines, skipping the empty ones'''
    line = file_data.readline()
    while not line:
        line = file_data.readline()
    return line

def find_matter(oss: str) -> str:
    '''Finds if ene or mag is required to calculate the observable oss'''
    if oss in {'amag','chi','mag','binder'} :
        return 'magn'
    return 'ene'

if __name__ == '__main__':
    bool1=user_while('try 1:\n','y')
    print(bool1)
    bool2=user_while('try 2:\n','n')
    print(bool2)