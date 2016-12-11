#python网络数据采集
#使用现有文件内容，模拟文章生成（聊天）
"""
马尔可夫模型
马尔可夫文字生成器(markov text generator) - 基于一种常用于分析大量随机事件的马尔可夫模型. 随机事件的特点是一个离散事件发生之后, 另一个离散事件将在前一个事件的条件下以一定概率发生
在马尔可夫模型描述的天气系统中,如果今天是晴天,那么明天有70%的可能是晴天,20%的可能多云,10% 的可能下雨。如果今天是下雨天,那么明天有 50% 的可能也下雨,25% 的可能是晴天,25% 的可能是多云
马尔可夫模型需要注意的点:
任何一个节点引出的所有可能的总和必须等于 100%。无论是多么复杂的系统,必然会在下一步发生若干事件中的一个事件。
只有当前节点的状态会影响下一个状态。
有些节点可能比其他节点较难到达
google的pagerank算法也是基于马尔可夫模型的, 将网站看作节点, 入站/出站链接作为节点的连线. 连接某个节点的可能性(linklihood)表示一个网站的相对关注度
马尔可夫文字生成器的工作原理: 对文献中的每一个单词进行有效处理, 再建立一个二维字典, 用于统计二元词组的词频. 每次以当前单词所在节点为查询表, 选择下一个节点. 随机生成一个权重, 用词频减权重, 一旦权重减为非正数, 确定该单词为下一单词. 词频高的单词使权重减小得更厉害, 因此更容易获得
"""

from urllib.request import urlopen
from random import randint

def wordListSum(wordList):
    sum = 0
    for word, value in wordList.items():
        sum += value
    return sum

def retrieveRandomWord(wordList):

    randIndex = randint(1, wordListSum(wordList))
    for word, value in wordList.items():
        randIndex -= value
        if randIndex <= 0:
            return word

'''
{
  word_a:{word_b:2, word_c:1, word_d:1,},
  word_b:{word_b:5, word_d:2,},
  #......
}
'''
def buildWordDict(text):
    #Remove newlines and quotes
    text = text.replace("\n", " ")
    text = text.replace("\"", "")

    #Make sure puncuation are treated as their own "word," so they will be included
    #in the Markov chain
    punctuation = [',','.',';',':']
    for symbol in punctuation:
        text = text.replace(symbol, " "+symbol+" ")

    words = text.split(" ")
    #Filter out empty words
    words = [word for word in words if word != ""]

    wordDict = {}
    for i in range(1, len(words)):
        if words[i-1] not in wordDict:
            #Create a new dictionary for this word
            wordDict[words[i-1]] = {}
        if words[i] not in wordDict[words[i-1]]:
            wordDict[words[i-1]][words[i]] = 0
        wordDict[words[i-1]][words[i]] += 1

    return wordDict

text = str(urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read(), 'utf-8')
wordDict = buildWordDict(text)

#Generate a Markov chain of length 100
length = 100
chain = ""
currentWord = "I"
for i in range(0, length):
    chain += currentWord+" "
    #print(wordDict[currentWord])
    currentWord = retrieveRandomWord(wordDict[currentWord])

print(chain)
