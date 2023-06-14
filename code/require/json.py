#import sys
import os
import re
import json


"""
TODO: 取两种注解的并集, 再用","分隔. +考虑explorer的结果
"""

def requires_permission(file_path):

    """
    扩展requires_permission(link: my_mapping.py),对匹配结果格式化 
    返回一个method_dic
        格式为{
                method_name: 
                {
                    'file_path':..., 
                    'permission':{...}, 
                    'return_value':..., 
                    'method_arg':...
                }
                method_name:...
            }
    
    DONE: method_arg final bug
    """

    with open(file_path, 'r') as file:
        content = file.read()
 
        pattern = r'@RequiresPermission\(([^*]*?)\)\s*(?:@(?:[\w._={}]+)(?:\([\w._]+\))?\s*)*\s*(?:public\s+|private\s+|protected\s+|default\s+)*(?:abstract\s+|static\s+|final\s+|synchronized\s+|native\s+|transient\s+)*(?:@(?:[\w.]+)\s+)*([^;*=/]*?\(.*?\))' #OK
        # DONE: 删除@...
        # DONE: 匹配函数名 *? > [^;*=]*+


        matches = re.findall(pattern, content, re.DOTALL) 
        if not matches: # 如果没有匹配到, 则返回
            return

        # 4. 存储格式化结果
        #   4.1 method_dic_sub {file_path:..., 'permission':{...}, 'return_value':..., 'method_arg':...}
        #   4.2 method_dic {method_name: method_dic_sub}
        method_dic = {}

        for match in matches:

            # 1.处理permission
            permission_string = match[0]

            # 1.1: 处理anyof/allof, 统一用,分隔
            pattern_of = r'\{(.*?)\}'  
            match_of = re.search(pattern_of, permission_string.replace("\n", ""), re.DOTALL)
            if match_of:
                permission_string = match_of.group(1).replace(" ", "").replace("\"", "")

            # 1.2.以集合形式存储permission
            permission_dic = set ()
            for permission in permission_string.split(","):  #match[0]是permission
                permission_dic.add("android.permission." + permission.split(".")[-1])


            # 2.处理file_path
            # 4.1a 把file_path和permission 存储到method_dic_sub
            method_dic_sub = {}
            method_dic_sub["file_path"] = file_path[96:-5].replace("\\", ".") #分隔
            method_dic_sub["permission"] = permission_dic #分隔
            print("permission:",method_dic_sub["permission"],"\n")
            #print("method_dic_sub:", method_dic_sub, "\n")


            # 3.处理return_value,method_arg,method_name
            method = match[1].replace("\n","") 

            # 3.1 return_value
            if method.startswith("("):  #NOTE: 去除强制匹配
                continue
            print("method:", method)
            return_value = method.split(' ')[0] # OK
            print("return_value:", return_value)
            #print ("match:", match)


            # 3.2 method_args 
            method_arg = ""
            method_arg_per = []
            args = re.search(r'\((.*)\)',method).group(1)
            if args:
                for arg in args.split(","): 
                    print("arg:", arg,"\n")

                    # DONE: DEBUG 
                    # NOTE: 匹配前面可能的final和@.. (不计顺序)
                    find = re.search(r'(?:(?:final\s*)|(?:@(?:[\w.]+)\s+))*([\w.<>\[\]]+)\s', arg).group(1) 
                    print("find:",find,"\n")
                    method_arg_per.append(find)

                    
                method_arg = "(" + ",".join(method_arg_per) + ")"
            else:
                method_arg = "()"
            print("method_arg:", method_arg)  

            # 4.1b 把返回值和参数类型 存储到method_dic_sub中
            method_dic_sub["return_value"] = return_value
            method_dic_sub["method_arg"] = method_arg


            # 3.3 method_name
            method_name = re.search(r'\s+(\w+)\(', method).group(1)
            print("method_name:", method_name, "\n")
            method_dic_sub["method_name"] = method_name

            # 4.2 存储为method_dic, 格式为{method_name: method_dic_sub}
            # method_dic[method_name] = method_dic_sub 
            #print(method_dic_sub, "\n")

            # 5. 保留测试结果
            # NOTE: method_dic in require_json_4.txt. DONE: DEBUG 
            with open('require_json_6.txt', 'a') as file:
                file.write(f'match0: {match[0]}\nmatch1: {match[1]}\nmethod_dic: {method_dic_sub}\n\n')

            # with open('require_string_2.txt', 'a') as file:
            #     file.write(f'{method_dic_sub["file_path"]}.{method_dic_sub["method_name"]}{method_dic_sub["method_arg"]}{method_dic_sub["return_value"]}  ::  {",".join(method_dic_sub["permission"])}\n')
                

        #print("method_dic",method_dic,"\n")
        return method_dic 
    



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
                requires_permission(file_path)
                #link_permission(file_path) #NOTE check 6.4 in 

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