import pdfplumber
from tqdm import tqdm
import pandas as pd
import os
import re

file_path = "E:\\财务报告\\财务报告2020"#PDF文件文件夹地址，需要修改
file_lst = os.listdir(file_path)
print(len(file_lst))

data_source = pd.read_excel("E:\\几何画板\\数据2020.xlsx")
print(len(data_source))

#检查爬取是否有问题
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

new_path = "F:\\财务报告\\2020财务报告output"#TXT文件文件夹地址，需要修改
isExists=os.path.exists(new_path)
# 判断结果
if not isExists:
    os.makedirs(new_path) 
    print(new_path+'创建成功')
else:
# 如果目录存在则不创建，并提示目录已存在
    print(new_path+'目录已存在')
    
#PDF转换成txt函数
def pdf_to_txt(file_lst,new_path):
    error_lst=[]#转换失败的PDF放在这里
    for file in tqdm(file_lst):
        #设置路径
        temp_path = file_path + "\\" + file
        temp_save_path = new_path + "\\" + re.split("[\.]",file)[0]+".txt"
        #开始转换
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
        
    print(error_lst)###最后告诉转换失败的文件夹，记录一下
