#import sys
import os
import re

import json


"""
以requires_permission为例, 对每个.java文件进行处理, 返回一个dict2, 格式为{method_name: {file_path:..., 'permission':...}}

link: my_mapping.py
    NOTE/TODO: 删除@NonNull 
"""
def requires_permission(file_path):

    with open(file_path, 'r') as file:
        content = file.read()
    
        pattern = r'@RequiresPermission\(([^*]*?)\)\s*(?:@\w+(?:\([\w._]+\))?\s*)?\s*(?:public\s+|private\s+|protected\s+|default\s+)?(?:abstract\s+|static\s+|final\s+|synchronized\s+|native\s+|transient\s+)?(?:@NonNull\s+)?([^;*=]*?\(.*?\))'  
        # NOTE: 删除@NonNull

        matches = re.findall(pattern, content, re.DOTALL) 

        if not matches: # 如果没有匹配到, 则返回
            return
        
        dict2 = {}
        """1.处理method"""
        # TODO: 处理java.lang.String
        for match in matches:
            permission_string = match[0]
            method = match[1].replace("\n","") #.replace(" ","") 
            #print("method:", method)
            return_value = method.split(' ')[0]
            #print("return_value:", return_value)
            method_match = re.search(r'\s+(\w+\(.*?\))', method)
            method_name = method_match.group(1)
            #print("method_name:", method_name)


            """2.处理permission"""
            pattern_of = r'\{(.*?)\}'
            match_of = re.search(pattern_of, permission_string.replace("\n", ""), re.DOTALL)
            if match_of:
                permission_string = match_of.group(1).replace(" ", "")


            dict = {}
            dict["file_path"] = file_path
            dict["permission"] = permission_string #分隔
            #dict["method_name"] = method_name #分隔
            dict2[method_name] = dict

            #print(dict, "\n")
        
            
            #将permission和method_name保存到text.txt中
            with open('require_test9_26.txt', 'a') as file:
                file.write(f'Path: {file_path}\nMethod: {method_name}\nPermission: {permission_string}\n\n')

        print("dict2",dict2)
        return dict2 #permissions
    


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


path_name = []
for api_level in range(26, 33):

    folder_path = 'D:/CLASS/1 Now/texwork/shared/permission/sdk_source/android-sdk-sources-for-api-level-{level}-master/'.format(level=api_level) 
    path_name.append(folder_path)


    #permissions = get_files(folder_path)
    #save_to_file(permissions)

print(path_name)