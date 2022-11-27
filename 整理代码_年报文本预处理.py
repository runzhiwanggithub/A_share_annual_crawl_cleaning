import pandas as pd
import numpy as np
from tqdm import tqdm
import jieba
import  re
from datetime import datetime
import random

#数据预处理
def del_num_alpha(data):
	for i in tqdm(range(len(data))):
		#删除特殊字符和数字
        data.loc[i,"主营业务"] = re.sub("[^\u4e00-\u9fa5^a-z^A-Z^，^。^；^：^、^？^！^—^《^》^〈^〉^·^—^……^“^”^‘^’^（^）]", "", str(data.loc[i,"主营业务"]))
    
    
def stopwordslist():
    #Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
    
    stopwords_1 = [str(line).strip() for line in open('E:\\stopwords-master\\stopwords-master\\baidu_stopwords.txt',encoding='UTF-8').readlines()]
    stopwords_2 = [str(line).strip() for line in open('E:\\stopwords-master\\stopwords-master\\cn_stopwords.txt',encoding='UTF-8').readlines()]
    stopwords_3 = [str(line).strip() for line in open('E:\\stopwords-master\\stopwords-master\\hit_stopwords.txt',encoding='UTF-8').readlines()]
    stopwords_4 = [str(line).strip() for line in open('E:\\stopwords-master\\stopwords-master\\scu_stopwords.txt',encoding='UTF-8').readlines()]
    
    stopwords_lst = set(stopwords_1 + stopwords_2 + stopwords_3 + stopwords_4)
    stopwords = list(stopwords_lst)
    
    return stopwords

def seg_depart(sentence):
     #sentence是要分词的句子
     # 对文档中的每一行进行中文分词
        #print("正在分词")
        sentence_depart = jieba.cut(str(sentence).strip())
     # 创建一个停用词列表
        stopwords = stopwordslist()
     # 输出结果为outstr
        outstr = ''
     # 去停用词
        for word in sentence_depart:
            if word not in stopwords:
                if word != '\t' and len(word)>1:
                    outstr += word
                    outstr += " "
        return outstr
        
data = pd.read_excel("F:\\LDA_ROBUST.xlsx")
data = del_num_alpha(data)

data["textnew"] = np.nan
for i in tqdm(range(len(data))):
    line_seg = seg_depart(data.loc[i,"主营业务"])
    data.loc[i,'textnew']=line_seg
print("删除停用词和分词成功！！！")
del data["主营业务"]
