import pandas
 
import os




def find_csv_file_in_current_path():    #功能：返回当前路径下所有csv文件路径列表
    csv_files_name_list=[]
    current_path_str = os.path.abspath('.') + '\\' #获取程序当前路径
    file_name_str_list = os.listdir(os.getcwd())
    for file_name_str in file_name_str_list:
        if(file_name_str[-4:] == ".csv"):
            csv_files_name_list.append( (current_path_str + file_name_str) )  #将文件完整路径添加到列表中
        else:
            pass
    if(csv_files_name_list==[]):    #如果文件列表为空，则抛出异常
        raise Exception("don't find any csv file in path: ", current_path_str)
    
    return csv_files_name_list
    pass

 
if __name__ =="__main__":
    csv_files_data_list=[]  #用来存储所有
    #
    csv_files_name_list=find_csv_file_in_current_path()
    for csv_file_path in csv_files_name_list:
        csv_file_data = pandas.read_csv(csv_file_path)
        print("pandas.read_csv file path:", csv_file_path)
        
        csv_files_data_list.append(csv_file_data)
        
    all_csv_files_data = pandas.concat(csv_files_data_list)

    sheet_header=[  #表头构成
        "filename", #文件名
        "extension name",   #文件拓展名
        "full filename",    #完整文件名（）
        "global file path",    #全局文件路径
        "file size",    #文件大小
        "hash algorithm name", #哈希算法名称
        "hash value",   #文件哈希值
        "creation date",    #文件创建时间
        "last time of file modified"    #最后一次修改时间
        ]
    
    
    
    
    print("hi3!")

    
    