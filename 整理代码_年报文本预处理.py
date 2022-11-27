import pandas as pd
import numpy as np
from tqdm import tqdm
import jieba
import  re
from datetime import datetime
import random

#����Ԥ����
def del_num_alpha(data):
	for i in tqdm(range(len(data))):
		#ɾ�������ַ�������
        data.loc[i,"��Ӫҵ��"] = re.sub("[^\u4e00-\u9fa5^a-z^A-Z^��^��^��^��^��^��^��^��^��^��^��^��^��^��^����^��^��^��^��^��^��]", "", str(data.loc[i,"��Ӫҵ��"]))
    
    
def stopwordslist():
    #Python strip() ���������Ƴ��ַ���ͷβָ�����ַ���Ĭ��Ϊ�ո���з������ַ�����
    
    stopwords_1 = [str(line).strip() for line in open('E:\\stopwords-master\\stopwords-master\\baidu_stopwords.txt',encoding='UTF-8').readlines()]
    stopwords_2 = [str(line).strip() for line in open('E:\\stopwords-master\\stopwords-master\\cn_stopwords.txt',encoding='UTF-8').readlines()]
    stopwords_3 = [str(line).strip() for line in open('E:\\stopwords-master\\stopwords-master\\hit_stopwords.txt',encoding='UTF-8').readlines()]
    stopwords_4 = [str(line).strip() for line in open('E:\\stopwords-master\\stopwords-master\\scu_stopwords.txt',encoding='UTF-8').readlines()]
    
    stopwords_lst = set(stopwords_1 + stopwords_2 + stopwords_3 + stopwords_4)
    stopwords = list(stopwords_lst)
    
    return stopwords

def seg_depart(sentence):
     #sentence��Ҫ�ִʵľ���
     # ���ĵ��е�ÿһ�н������ķִ�
        #print("���ڷִ�")
        sentence_depart = jieba.cut(str(sentence).strip())
     # ����һ��ͣ�ô��б�
        stopwords = stopwordslist()
     # ������Ϊoutstr
        outstr = ''
     # ȥͣ�ô�
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
    line_seg = seg_depart(data.loc[i,"��Ӫҵ��"])
    data.loc[i,'textnew']=line_seg
print("ɾ��ͣ�ôʺͷִʳɹ�������")
del data["��Ӫҵ��"]
