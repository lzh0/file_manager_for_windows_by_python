# -*- coding: UTF-8 -*-
"""
#简介：一个只需要标准库的文件管理器。
#功能：扫描输入的某个或多个路径下的所有文件，汇总记录文件信息并保存为csv表单文件，并提供疑似重复文件的csv文件表单。（并删除重复文件？）
#第三方库依赖：无
#
#适用平台：windows
"""

#默认保存文件到当前路径下
#from datetime import datetime
import datetime
#sudo python3 ./data_collection_main.py


import platform
import threading    #通过多线程，解决控制台输入堵塞问题（？？？写的时候忘记有非堵塞的用户输入检测方法了...
import subprocess   #使用subprocess.run代替os.popen以获取命令行返回数据   #https://docs.python.org/3/library/subprocess.html

import os   
    #使用os.path.splitext()和os.path.split()函数，从全局路径中裁剪出含拓展名的文件名和文件名
    #使用os.walk()遍历路径下的所有文件

import time #用于计算程序耗时

def generate_filename():
    file_name=str(datetime.datetime.now())
    file_name=file_name[0:file_name.find(".")]  #去除秒以下的部分
    file_name=file_name.replace("-","")     #合并年月日
    file_name=file_name.replace(":","")    #windows中文件名禁止使用':'
    file_name=file_name.replace(" ","_")
    file_name=file_name.replace("-","_")
    file_name="files_path_"+("data_file_")+file_name+(".csv")   #简化版：file_name+(".csv")
    print("data file name is: "+file_name)
    return file_name

class NewFile():    #简单封装一下文件操作（意义不明的文件操作封装
    file_object=None
    file_state=""
    #构造
    def __init__(self,file_path=".\\",file_name=generate_filename(),open_file_mode="a+",file_encode_format= "utf-8" ):    #默认创建在当前路径下，默认文件名为时间戳，默认打开文件方式为创建追加(a+)，默认保存的文件编码格式为utf-8
         #windwos下路径符为"\"，但由于python转义字符冲突，故需要输入为"\\"
        if(file_path[-1] != "\\"):  #检测路径是否完整，末尾是否为"\"
                file_path=file_path+"\\"    #路径尾端不完整得手动添加"\"
        else:pass
        #路径检测完成，则创建文件：
        #return open("file_path"+file_name, mode=open_file_mode)
        self.file_object = open(file_name, mode=open_file_mode, encoding=file_encode_format)
        self.file_state="open"

    def write(self, write_in_str):
         self.file_object.write(write_in_str)
         self.file_object.flush()   #刷新缓冲区立即写入 #【性能优化项，待优化】
         
    def write_append(self, write_in_str):
         self.file_object.write(write_in_str)
         self.file_object.flush()   #刷新缓冲区立即写入 #【性能优化项，待优化】

    def write_in_new_line(self, write_in_str):
         self.file_object.write("\n" + write_in_str)
         self.file_object.flush()   #刷新缓冲区立即写入 #【性能优化项，待优化】

    def __del__(self,): #析构   #免去在主程序中结束后再添加close语句
    #def close(self,):
         if(self.file_state == "open"):
              self.file_object.close()
         else:
            print("file handle had closed")

def capture_terminal_exec(command_str): #功能：执行指定命令行
    return_str = subprocess.run(["dir"], capture_output=True ,check=True, shell=True)   #, stdout=subprocess.PIPE
    #subprocess.run(["dir"], , stdout=subprocess.PIPE ,check=True, shell=True)   #
    #subprocess.run("dir -l",  stdout=subprocess.PIPE , shell=True).stdout.decode("GBK")    #解码成功   #命令终端的编码格式可以在打开命令终端——属性——当前代码页中看到，为GBK
    #windows cmd命令示例：显示当前路径(pwd)：echo %cd% ；显示当前路径下所有文件(ls)：dir
    subprocess.run("dir",  stdout=subprocess.PIPE , shell=True).stdout.decode("GBK")    #解码成功   #命令终端的编码格式可以在打开命令终端——属性——当前代码页中看到，为GBK
    #subprocess模块详解说明：https://docs.python.org/3.5/library/subprocess.html #https://docs.python.org/zh-cn/3.5/library/subprocess.html
    #中文编码：GB2312、GBK（GBK 向下与 GB 2312 编码兼容，向上支持 ISO 10646.1国际标准。）、GB18030 （对GB 2312-1980完全向后兼容，与GBK基本向后兼容，并支持Unicode）
    #编码猜测破解：https://www.haomeili.net/Code/DeCoding
    return return_str

def subprocess_popen(command_str):    #功能：执行指定命令行,并且既可以判断执行是否成功，还可以获取执行结果#来源https://blog.csdn.net/baidu_36943075/article/details/105681683
    p = subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE)  # 执行shell语句并定义输出格式
    while p.poll() is None:  # 判断进程是否结束（Popen.poll()用于检查子进程（命令）是否已经执行结束，没结束返回None，结束后返回状态码）
        if p.wait() != 0:  # 判断是否执行成功（Popen.wait()等待子进程结束，并返回状态码；如果设置并且在timeout指定的秒数之后进程还没有结束，将会抛出一个TimeoutExpired异常。）
            print("exec cmd fail! cmd: ",command_str)
            return ["subprocess_popen func exec fail!"]    #返回内容格式为字符串列表
        else:
            re = p.stdout.readlines()  # 获取原始执行结果
            result = []
            for i in range(len(re)):  # 由于原始结果需要转换编码，所以循环转为utf8编码并且去除\n换行
                res = re[i].decode('GBK').strip('\r\n') #由于操作系统为中文，故命令行使用的是GBK编码 #res = re[i].decode('utf-8').strip('\r\n')
                result.append(res)
            return result

def generate_cmd_str_of_hashing_file(global_file_path:str, hash_algorithm_name:str):   #生成终端命令：通过调用winodws系统API，计算文件hash值
    global_file_path.replace("'", '"')  #hash命令中字符串必须用双引号"包裹，而不能用单引号' 
    global_file_path='"'+global_file_path+'"'   #cmd的hash命令必须用双引号""（单引号'不行）包裹文件路径，否则若路径中有空格会导致命令传输参数数量出错
    
    if (global_file_path[-1] == "\\"):  #检测路径尾端是否正确（是文件名而不是路径符\\）
        raise Exception("file_path error!!! your input global_file_path is: ", global_file_path)
    else:pass
    
    #计算文件hash的cmd命令：certutil -hashfile "C:\Users\Public\spars.txt" MD5 #其中双引号！不能使用！单引号，必须双引号，所以字符串只能用单引号
    cmd_header='certutil -hashfile '
    hash_algorithm_name = hash_algorithm_name.replace('"',"'")    #由于hash命令中路径字符串用了双引号，故附加参数等其他部分字符串只能用单引号表示
    if(hash_algorithm_name[0] != ' '):  #名称字符串格式检测，检测是否有空格（例：' MD5'、' SHA256'...） （哈希算法名称检测/匹配
        hash_algorithm_name=' ' + hash_algorithm_name 
    hash_cmd_str = 'certutil -hashfile '+ global_file_path + hash_algorithm_name
    return hash_cmd_str
#'certutil -hashfile C:\\Users\\lzh_company\\Desktop\\remote_vscode\\my_file_manager\\data_structure.py MD5'
def get_file_hash_vale_by_cmd_str(hash_command_str:str):  #功能：通过命令行计算并返回文件哈希值，同时检测执行是否成功； 简述：基于subprocess_popen的简单封装，特化用于执行hash命令计算及执行状态返回检测
    cmd_path_part_str = hash_command_str[hash_command_str.find("-hashfile ")+10:hash_command_str.find(" MD5")]   #截取命令行中的文件路径部分
    result_str_list=subprocess_popen(hash_command_str)  #结果示例：['MD5 的 C:\\Users\\lzh_company\\Desktop\\remote_vscode\\my_file_manager\\temp.py 哈希:', '9bdf1403166a4fdf4d4d3c9f903779ea', 'CertUtil: -hashfile 命令成功完成。']
    if(len(result_str_list) != 3):   #返回字符串数组元素检测
        #raise Exception( "EXEC CMD FAIL: " + hash_command_str + "    cmd should return 3 members of list, but actually return:", len(result_str_list) )
        return  [cmd_path_part_str,"cmd should return 3 members of list, but actually return:"+str((result_str_list))]#若命令执行失败触发异常抛出，会影响到导致中断表格写入，并且由于没有进度保存，从而导致需要重来
    else:   #正常情况下返回数量为3个，见结果示例
        if(result_str_list[2].find("命令成功完成") ==-1 ):  #检测hash命令调用状态
            #raise Exception( "EXEC CMD FAIL: "+hash_command_str+"    cmd retval:", result_str_list[2]) #执行未成功
            return [cmd_path_part_str, "EXEC CMD FAIL: "+hash_command_str+"    cmd retval:", result_str_list[2]+str((result_str_list))]   #若命令执行失败触发异常抛出，会影响到导致中断表格写入，并且由于没有进度保存，从而导致需要重来
        
        else:
            file_path_str=result_str_list[0] #例：'MD5 的 C:\\xxx\\temp.py 哈希:'
            file_hash_str=result_str_list[1] #例：'9bdf1403166a4fdf4d4d3c9f903779ea'
    return [file_path_str[6:-4],file_hash_str] #返回列表(被hash的文件路径，文件hash值)

def write_in_csv_by_design_format(csv_file_object:object, global_file_path:str,hash_algorithm_name:str,hash_value_str:str, ):    #以设计格式写入csv文件
    file_name_str= ((global_file_path.split("\\")[-1]).split("."))[0]  #获取文件名 #注：此处定义的文件名是指最后一个路径符到第一个.字符之前的所有字符
    filename_extension_str= ( os.path.splitext(global_file_path) )[1]#获取文件拓展名    #注：此处定义的文件拓展名指的是从左到右最后一个.字符与字符串末端之间的所有字符
    full_filename_str = ( os.path.split(global_file_path) )[1]  #完整文件名（含拓展名filename_and_extension_str） #注：此处定义的完整文件名是指最后一个路径符到文件路径末端的所有字符
    file_size_int = os.path.getsize(global_file_path) #获取文件大小,单位字节Bytes，1024 Bytes = 1kb
    file_hash_value_str = hash_value_str
    
    #文件时间信息
    file_creation_time = os.path.getctime(global_file_path)  #文件创建时间
    last_time_of_file_modified = os.path.getmtime(global_file_path) #最后一次文件修改时间
    #os.path.getatime(global_file_path) #文件访问时间
    #注：由于返回的都为纪元时间/Unix 纪元/Unix 时间，所以需要转换为可读的时间格式(若不需要秒以下的小数部分，去掉.%f即可)
    file_creation_time = datetime.datetime.fromtimestamp(file_creation_time).strftime('%Y-%m-%d %H:%M:%S.%f')   #例结果'2023-04-26 09:11:08.781599'
    last_time_of_file_modified = datetime.datetime.fromtimestamp(last_time_of_file_modified).strftime('%Y-%m-%d %H:%M:%S.%f')   #例结果'2023-04-26 09:11:08.781599'
    
    #按CSV及设计格式写入CSV文件
    csv_file_object.write_in_new_line(
        file_name_str
        +","+
        filename_extension_str
        +","+
        full_filename_str
        +","+
        global_file_path
        +","+
        str(file_size_int)
        +","+
        hash_algorithm_name
        +","+
        file_hash_value_str
        +","+
        file_creation_time
        +","+
        last_time_of_file_modified
    )
    # "filename", #文件名
    # "extension name",   #文件拓展名
    # "full filename",    #完整文件名（）
    # "global file path",    #全局文件路径
    # "file size",    #文件大小
    # "hash algorithm name", #哈希算法名称
    # "hash value",   #文件哈希值
    # "creation date",    #文件创建时间
    # "last time of file modified"    #最后一次修改时间
    
    pass
    
def get_all_files_path_str_list_in(dir_path):   #功能：遍历获取指定路径下的所有文件
    # https://zhuanlan.zhihu.com/p/149824829
    files_path_str_list = [] #文件列表，用于存储
    # [print([print(home,"\\",filename) for filename in files]) for home,dirs,files in os.walk("C:\\Users\\me\\Desktop\\出BUG乱码的路径")]
    for home, dirs, files in os.walk(dir_path): #遍历输入输入路径下的所有文件
        for filename in files:
            # 文件名列表，包含完整路径
            files_path_str_list.append(os.path.join(home, filename))
            # 文件名列表，只包含文件名
            # Filelist.append( filename)
    return files_path_str_list


#测试路径： C:\Users\lzh_company\Desktop\remote_vscode\my_file_manager\temp.py
    #"C:\\Users\\lzh_company\\Desktop\\remote_vscode\\my_file_manager"
    #"C:\\Users\\lzh_company\\Desktop\\remote_vscode\\my_file_manager\\temp.py"
if __name__ == "__main__":
    program_start_time=time.time()


    hash_algorithm_name="MD5"
    print("start!")
    my_csv_file=NewFile(file_encode_format="GBK")   #若文件以utf-8编码，在excel中打开会乱码（需修改默认设置）；若以GBK编码，在vscode中打开会乱码（需要更改文件编码，以UTF-8打开）
    #microsoft excel 支持unicode 但不支持UTF-8, 并且在winodws中文系统中默认使用GBK格式打开文件
    #csv路径数据文件格式：
    #第一行：用户输入路径（指定遍历的路径）
    #第二行：表头写入
    #第三、四、...：数据
    user_input_path = 'C:\\Users\\me\\Desktop\\出BUG乱码的路径\\U64G\\手机\\Apk'
    user_input_path = 'C:\\Users\\me\\Desktop\\出BUG乱码的路径'
    #user_input_path = input("file_path: ").replace(" ","")  #获取指定的遍历路径 #健壮性有待提升，建议形成路径规则自动滤除
    sheet_header_str=(  #表头构成
        "filename,"+ #文件名
        "extension name,"+   #文件拓展名
        "full filename,"+    #完整文件名（）
        "global file path,"+    #全局文件路径
        "file size,"+    #文件大小
        "hash algorithm name,"+ #哈希算法名称
        "hash value,"+   #文件哈希值
        "creation date,"+    #文件创建时间
        "last time of file modified,"    #最后一次修改时间
        )
    
    my_csv_file.write_append(user_input_path)  #第一行：用户输入路径（指定遍历的路径）
    my_csv_file.write_in_new_line(sheet_header_str) #第二行：表头写入

    files_path_str_list = get_all_files_path_str_list_in(user_input_path)
    print("总计发现在路径下：",user_input_path," 有：",len(files_path_str_list)," 个文件")
    for file_path_str in files_path_str_list:

        hashing_file_cmd_str=generate_cmd_str_of_hashing_file(file_path_str,"MD5")
        __file_path_str,hash_value_str=get_file_hash_vale_by_cmd_str(hashing_file_cmd_str)
        #my_csv_file.write_in_new_line(hash_value_str)
        write_in_csv_by_design_format(my_csv_file, file_path_str, hash_algorithm_name, hash_value_str)
    #print(hash_value_str)



    print("program spend time:", time.time()-program_start_time, " sec")
    exit(0)

    while(1):
        user_terminal_input=input("input q to exit: \n")
        my_csv_file.write(user_terminal_input)
        if(user_terminal_input[0] == "q"):
            break

    print("program end")