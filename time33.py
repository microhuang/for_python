#time33算法和它的变种，提供良好的碰撞，并具有速度优势
def time33(str):
    hash=0
    for c in str:
        hash=hash*33+int(c)
    return hash

#print(time33('ab中文'))
