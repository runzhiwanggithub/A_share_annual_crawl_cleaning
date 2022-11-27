import pdfplumber
from tqdm import tqdm
import pandas as pd
import os
import re

file_path = "E:\\���񱨸�\\���񱨸�2020"#PDF�ļ��ļ��е�ַ����Ҫ�޸�
file_lst = os.listdir(file_path)
print(len(file_lst))

data_source = pd.read_excel("E:\\���λ���\\����2020.xlsx")
print(len(data_source))

#�����ȡ�Ƿ�������
data_source_lst = list(data_source["security_name"])
data_source_lst = [name.replace("*","") for name in data_source_lst]
security_name_lst = []
for file in file_lst:
    security_name = file.split("-")[1]
    security_name_lst.append(security_name)
print(len(security_name_lst))
print(len(data_source_lst))#.replace("*","")
test_lst = [name for name in data_source_lst if not name in security_name_lst] 
print(test_lst)

new_path = "F:\\���񱨸�\\2020���񱨸�output"#TXT�ļ��ļ��е�ַ����Ҫ�޸�
isExists=os.path.exists(new_path)
# �жϽ��
if not isExists:
    os.makedirs(new_path) 
    print(new_path+'�����ɹ�')
else:
# ���Ŀ¼�����򲻴���������ʾĿ¼�Ѵ���
    print(new_path+'Ŀ¼�Ѵ���')
    
#PDFת����txt����
def pdf_to_txt(file_lst,new_path):
    error_lst=[]#ת��ʧ�ܵ�PDF��������
    for file in tqdm(file_lst):
        #����·��
        temp_path = file_path + "\\" + file
        temp_save_path = new_path + "\\" + re.split("[\.]",file)[0]+".txt"
        #��ʼת��
        try:
            with pdfplumber.open(temp_path) as p:
                temp_string=""
                for i in range(len(p.pages)):
                    page = p.pages[i]
                    temp_textdata = page.extract_text()
                    temp_string=temp_string+temp_textdata
            temp_text_file = open(temp_save_path, "w",encoding="utf-8")
            n = temp_text_file.write(temp_string)
            temp_text_file.close()
        except :
            print("Error")
            error_lst.append(file)
            pass
        
    print(error_lst)###������ת��ʧ�ܵ��ļ��У���¼һ��
