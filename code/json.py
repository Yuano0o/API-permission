#import sys
import os
import re
import json


"""
以requires_permission为例, 对每个.java文件进行处理, 返回一个method_dic, 格式为{method_name: {file_path:..., 'permission':{...}, 'return_value':..., 'method_arg':...}}

link: my_mapping.py
    NOTE/TODO: 删除@NonNull 
"""
def requires_permission(file_path):

    with open(file_path, 'r') as file:
        content = file.read()
     
        pattern = r'@RequiresPermission\(([^*]*?)\)\s*(?:@\w+(?:\([\w._]+\))?\s*)?\s*(?:public\s+|private\s+|protected\s+|default\s+)?(?:abstract\s+|static\s+|final\s+|synchronized\s+|native\s+|transient\s+)?(?:@NonNull\s+)?([^\;\*\=]*?\(.*?\))' #OK
        #pattern = r'@RequiresPermission\(([^*]*?)\)\s*(?:@\w+(?:\([\w._]+\))?\s*)?\s*(?:public\s+|private\s+|protected\s+|default\s+)?(?:abstract\s+|static\s+|final\s+|synchronized\s+|native\s+|transient\s+)?(?:@NonNull\s+)?([^\;\*\=]+\(.*?\))'
        # NOTE: 删除@NonNull
        # NOTE: 匹配函数名 *? > [^;*=]*+

        matches = re.findall(pattern, content, re.DOTALL) 

        if not matches: # 如果没有匹配到, 则返回
            return

        method_dic = {}

        for match in matches:

            """
            DONE: 处理permission
            NOTE: 以集合形式存储permission
            TODO: 取1,2的并集, 再用","分隔
            """
            permission_dic = set ()
            for permission in match[0].replace(" ", "").replace("\"", "").replace("\n","").split(","):  #match[0]是permission
                permission_string = "android.permission." + permission.split(".")[-1]
                permission_dic.add(permission_string)

            #print("permission_dic:", permission_dic, "\n")
            #for i in match[0].replace(" ", "").replace("\"", "").split(","):


            """DONE: 处理file_path, permission集合, 存储为method_dic_sub"""
            method_dic_sub = {}
            method_dic_sub["file_path"] = file_path[96:-5].replace("\\", ".") #分隔
            method_dic_sub["permission"] = permission_dic #分隔
            #print("method_dic_sub:", method_dic_sub, "\n")

            """
            TODO: 处理method_name, return_value, method_arg
            """

            method = match[1].replace("\n","") 
            #去除强制匹配
            if method.startswith("("):  
                continue
            print("method:", method)
            return_value = method.split(' ')[0] # OK
            print("return_value:", return_value)
            #print ("match:", match)


            #method_args = re.search(r'\(.*\)',method).group(1).split(",")
            method_arg = ""
            method_arg_per = []
            args = re.search(r'\((.*)\)',method).group(1)
            if args:
                for arg in args.split(","): 
                    #print("arg:", arg)
                    # TODO: 在append这里 匹配import的键值对
                    method_arg_per.append(re.search(r'(?:final\s*)?(?:@.*\s*)?([\w<>\[\]]+)\s', arg).group(1))
                    #method_arg += re.search(r'(?:final\s*)?(?:@.*\s*)?([\w<>]+)\s', arg).group(1) #匹配前面可能的final和@..
                method_arg = "(" + ",".join(method_arg_per) + ")"
            else:
                method_arg = "()"
            print("method_arg:", method_arg)  

            method_dic_sub["return_value"] = return_value
            method_dic_sub["method_arg"] = method_arg


            method_name = re.search(r'\s+(\w+)\(', method).group(1)
            
            # method = match[1].replace("\n","") #.replace(" ","")
            #method_name = method_name.replace("\n","") #.split(",")

            """存储为method_dic,格式为{method_name: {file_path:..., 'permission':{...}, 'return_value':..., 'method_arg':...}}"""
            method_dic[method_name] = method_dic_sub 

            #print(method_dic_sub, "\n")
        
            
            #将permission和method_name保存到text.txt中
            with open('require_json_2.txt', 'a') as file:
                file.write(f'match0: {match[0]}\nmatch1: {match[1]}\nmethod_dic: {method_dic_sub}\n\n')

        #print("method_dic",method_dic,"\n")
        return method_dic #permissions
    


def get_files(folder_path):
    """
    3.读取文件夹中的所有.java文件
    TODO: 保存对应的文件路径
    """
    files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                requires_permission(file_path)
                #link_permission(file_path) #NOTE check 6.4 in 

    return 0 #files # 返回文件路径列表


def save_to_file(permissions):
    """
    4.将提取的权限信息保存到test.txt文件中
    """
    with open('test.txt', 'w') as file:
        for method_name, permission in permissions:
            file.write(f'Method: {method_name}\tPermission: {permission}\n')

data = {}
json_data = json.dumps(data)

# 示例 
# or folder_path = sys.argv[1]
file_path = 'D:/CLASS/1 Now/texwork/shared/permission/sdk_source/android-sdk-sources-for-api-level-26-master/' #/android/service/oemlock/OemLockManager.java'
print(get_files(file_path))

# for api_level in range(26, 33):
#     folder_path = 'D:/CLASS/1 Now/texwork/shared/permission/sdk_source/android-sdk-sources-for-api-level-{level}-master/'.format(level=api_level) 
#     json_data["path"][api_level-26] = folder_path
#     permissions = get_files(folder_path)
    #save_to_file(permissions)


# path_name = []
# for api_level in range(26, 33):

#     folder_path = 'D:/CLASS/1 Now/texwork/shared/permission/sdk_source/android-sdk-sources-for-api-level-{level}-master/'.format(level=api_level) 
#     path_name.append(folder_path)


#     #permissions = get_files(folder_path)
#     #save_to_file(permissions)

# print(path_name)