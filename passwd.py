import string,random
''.join([random.choice(string.letters+string.digits) for i in range(8)])




import random,string,os
class password(object):
    #任何含有大量单词的文件都可以：我们只想让self.data
    #成为一个大字符串，我们将模仿其中的文本
    print os.getcwd()
    data=open("/usr/share/dict/words").read().lower()
    def renew(self,n,maxmem=3):
        '''根据回溯的最大“历史”的maxmem个字符
             在self.data中累积n个随机字符'''
        self.chars=[]
        for i in range(n):
            #随机“旋转”self.data
            randspot=random.randrange(len(self.data))
            #print "randspot=",randspot
            self.data=self.data[randspot:]+self.data[:randspot]
            #print "self.data=",self.data
            #获得n-gram
            where=-1
            #试图定位self.data中最后maxmem个字符
            #如果i<maxmem,我们其实只获取最后i个
            #即使是所有self.chars也没问题：列表
            #切片的容忍度很高，仍然适合此算法
            locate=''.join(self.chars[-maxmem:])
            #print "locate=",locate
            while where<0 and locate:
                #定位data中的n-gram
                where=self.data.find(locate)
                #print "where=",where
                #如果必要的话后退到一个短一点的n-gram
                locate=locate[1:]
            #如果where=-1且locate='',选self.data[0]
            #那是self.data中随机的一项，因此旋转过
            c=self.data[where+len(locate)+1]
            #print "c=",c
            #我们只需要小写字母，所以，如果我们挑到了
            #大写字母，我们会再次随机选择一个字母
            if not c.islower():c=random.choice(string.lowercase)
            #最后我们将字母记录到self.chars
            self.chars.append(c)
    def __str__(self):
        return ''.join(self.chars)

if __name__=='__main__':
#for test
    #onepass=password()
    #onepass.renew(5,2)
    #print onepass.chars
    "使用方法：pastiche [passwords [length [memory]]]"
    import sys
    if len(sys.argv)>1: dopass=int(sys.argv[1])
    else:dopass=8
    if len(sys.argv)>2: length=int(sys.argv[2])
    else:length=10
    if len(sys.argv)>3: memory=int(sys.argv[3])
    else:memory=3
    onepass=password()
    for i in range(dopass):
        onepass.renew(length,memory)
        print onepass
