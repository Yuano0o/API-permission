#import sys
import os
import re
import json


"""
TODO: debug final
"""


def link_permission(file_path):
    """
    2.匹配{@link android.Manifest.permission#}

    DONE: debug

    DONE: 匹配多种模式 如 require the {@link android.Manifest.permission#NFC} permission.
    DONE: 匹配方法名 ok
    DONE: 匹配完 删除"*"
    DONE: public 前面如果有注解?

    NOTE: valid 6.10: link_string_1=2=3  , link_json_2
    """
    with open(file_path, 'r') as file:
        content = file.read()

        # TODO: permission换成set, 与1保持一致, 并取并集

        # NOTE link_test7_26 (the methods matched are the same as test7)   
        # 匹配/** */后的第一个method
        # pattern = r'/\*\*(.*?)\*/\s*(?:@\w+(?:\([\w.={}]+\))?\s*)?(?:public|private|protected|default)\s+(?:abstract\s+|static\s+|final\s+|synchronized\s+|native\s+|transient\s+)?([^;*=]*?\(.*?\))' 
        # NOTE: 匹配/** */ + 可能的注解@xxx()/@xxx + java修饰符若干(防止强制匹配) + 关建字若干/无 + 返回值,方法名,参数(并去除;*=的强制匹配)

        # NOTE link_test10_26 移除返回值类型的修饰 
        pattern = r'/\*\*(.*?)\*/\s*(?:@(?:[\w.]+)(?:\([\w.={}]+\))?\s*)*(?:public\s+|private\s+|protected\s+|default\s+)*(?:abstract\s+|static\s+|final\s+|synchronized\s+|native\s+|transient\s+)*(?:@(?:[\w.]+)\s+)*([^;*=/]*?\(.*?\))' 
      

        matches = re.findall(pattern, content, re.DOTALL) 


        for match in matches:
            comment = match[0].strip().replace('*', '') # 去除首尾空格, 去除注释中的"*"
            permission_pattern = r'Requires\s+(?:the\s+)?Permission:\s*{@link\s+(.*?)}'
            permission_match = re.search(permission_pattern, comment, re.IGNORECASE) # DONE: 忽略大小写

            if permission_match:
                permission = permission_match.group(1)
                method = match[1].replace("\n","")
                #print("method:", method, "\n")

                if method.startswith("("):  #NOTE: 去除强制匹配
                    continue

                # 1.处理permission
                # 1.2.以集合形式存储permission
                #permission_dic = set ()
                # 4. 存储格式化结果
                method_dic = {}

                method_dic["permission"] = "android.permission." + re.search(r'android.Manifest.permission#(\w+)\s*', permission).group(1)
                print("permission:",method_dic["permission"])
                #permission_dic.add(permission_string)

                method_dic["file_path"] = file_path[96:-5].replace("\\", ".") #分隔
                print("file_path_:",method_dic["file_path"])

                method_name = re.search(r'\s+(\w+)\(', method).group(1)
                method_dic["method_name"] = method_name
 
                # 3.1 return_value

                print("method:", method)
                #print ("match:", match)


                # 3.2 method_args 
                method_arg = ""
                method_arg_per = []
                args = re.search(r'\((.*)\)',method).group(1)
                if args:
                    for arg in args.split(","): 
                        print("arg:", arg,"\n")

                        # TODO: 在append这里 匹配import的键值对
                        # DONE: DEBUG 
                        #匹配前面可能的final和@..
                        #NOTE: link_string_2, 把?改成*, 结果与1一致, 再加上. 作为3, 一致
                        find = re.search(r'(?:(?:final\s*)|(?:@(?:[\w.]+)\s+))*([\w.<>\[\]]+)\s', arg).group(1) 
                        print("find:",find,"\n")
                        method_arg_per.append(find)

                        
                    method_arg = "(" + ",".join(method_arg_per) + ")"
                else:
                    method_arg = "()"
                print("method_arg:", method_arg)  

                # 4.1b 把返回值和参数类型 存储到method_dic中
                method_dic["method_arg"] = method_arg

                return_value = method.split(' ')[0] # OK
                method_dic["return_value"] = return_value



                #将permission和method_name保存到text.txt中
                # with open('link_json_3.txt', 'a') as file:
                #     file.write(f'Path: {file_path}\nMethod: {method_name}\nPermission: {permission}\nmethod_dic: {method_dic}\n\n') #NOTE: 用f-string格式化输出

                with open('link_string_6.txt', 'a') as file:
                    file.write(f'{method_dic["file_path"]}.{method_dic["method_name"]}{method_dic["method_arg"]}{method_dic["return_value"]}  ::  {method_dic["permission"]}\n')
                



def get_files(folder_path):
    """
    3.读取文件夹中的所有.java文件
    DONE: 保存对应的文件路径
    """
    files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                #requires_permission(file_path)
                link_permission(file_path) #NOTE check 6.4 in 

    return 0 #files # 返回文件路径列表



# 示例 
# or folder_path = sys.argv[1]
file_path = 'D:/CLASS/1 Now/texwork/shared/permission/sdk_source/android-sdk-sources-for-api-level-26-master/' #/android/service/oemlock/OemLockManager.java'
print(get_files(file_path))


# data = {}
# json_data = json.dumps(data)

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