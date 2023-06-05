#import sys
import os
import re
import json

"""
TODO: 分别提取 1.@RequiresPermission 和 2.{@link} 两种注解的权限, 保存为JSON格式 (同一个JSON)
TODO: 保留匹配的完整/原始match字符串 以便检查匹配是否正确 
TODO: 最后处理成explorer的格式
"""

def requires_permission(file_path):
    """
    1. 匹配@RequiresPermission注解

    TODO: anyof 和 allof 的处理, 统一用,分隔

    DONE: debug, require_test6_26.txt
    
    link DONE 1.2: 匹配import 存储为键值表 
    """
    with open(file_path, 'r') as file:
        content = file.read()

        # NOTE: require_test3_26.txt
        #pattern = r'@RequiresPermission\(([\w.={}]+)\)\s*(?:@\w+(?:\([\w.={}]+\))?\s*)?\s*(?:public|private|protected|default)\s+(?:final\s+)?(?:synchronized\s+)?(?:native\s+)?([^;*=]*?\(.*?\))'  

        # NOTE: require_test4_26.txt
        # pattern = r'@RequiresPermission\(([^*]*?)\)\s*(?:@\w+(?:\([\w.]+\))?\s*)?\s*(?:public|private|protected|default)\s+(?:final\s+)?(?:synchronized\s+)?(?:native\s+)?([^;*=]*?\(.*?\))'  

        # NOTE: require_test5_26.txt
        #pattern = r'@RequiresPermission\(([^*]*?)\)\s*(?:@\w+(?:\([\w._]+\))?\s*)?\s*(?:public|private|protected|default)\s+(?:final\s+)?(?:synchronized\s+)?(?:native\s+)?([^;*=]*?\(.*?\))'  

        # NOTE: require_test1_26.txt
        #pattern = r'@RequiresPermission\((.*?)\)\s*(?:@\w+(?:\(.*?\))?\s*)?\s*(?:public|private|protected|default)?\s+(?:final\s+)?(?:synchronized\s+)?(?:native\s+)?([^;*=]*?\(.*?\))'  

        # NOTE: require_test6_26.txt, 去除强制匹配, 匹配anyof和allof, default
        pattern = r'@RequiresPermission\(([^*]*?)\)\s*(?:@\w+(?:\([\w._]+\))?\s*)?\s*(?:public|private|protected|default)?\s+(?:final\s+)?(?:synchronized\s+)?(?:native\s+)?([^;*=]*?\(.*?\))'  
        # NOTE: 匹配@RequiresPermission(...^*) + 可能的注解@xxx()/@xxx + java修饰符若干/无修饰符 + 返回值,方法名,参数(并去除;*=的强制匹配)
        # NOTE: 去除强制匹配: [^;*=]*?(匹配方法,除去变量,注释)   [^*](除去注释)
        matches = re.findall(pattern, content, re.DOTALL) 

        if not matches: # 如果没有匹配到, 则返回
            return
        
        permissions = []
        for match in matches:
            permission_string = match[0]
            method_name = match[1] # match[1]?
            print("file_path:",file_path)
            print("Permission:", permission_string)
            print("Method Name:", method_name)
            permissions.append((method_name, permission_string))
            
            #将permission和method_name保存到text.txt中
            with open('require_test6_26.txt', 'a') as file:
                file.write(f'Path: {file_path}\nMethod: {method_name}\nPermission: {permission_string}\n\n')


        return permissions


def link_permission(file_path):
    """
    2.匹配{@link android.Manifest.permission#}

    TODO: debug

    DONE: 匹配多种模式 如 require the {@link android.Manifest.permission#NFC} permission.
    DONE: 匹配方法名 ok
    DONE: 匹配完 删除"*"
    DONE: public 前面如果有注解?
    """
    with open(file_path, 'r') as file:
        content = file.read()

        # NOTE link_test1_26.txt
        # 匹配/** */后的第一个method
        # pattern = r'/\*\*(.*?)\*/\s*(?:@\w+(?:\([\w.]+\))?\s*)?(?:public|private|protected|default)\s+(?:final\s+)?(?:synchronized\s+)?(?:native\s+)?([^;*=]*?\(.*?\))' 
        # NOTE: 匹配/** */ + 可能的注解@xxx()/@xxx + java修饰符若干(防止强制匹配) + 返回值,方法名,参数(并去除;*=的强制匹配)

        #pattern = r'/\*\*(.*?)\*/\s*(?:@\w+(?:\([\w.]+\))?\s*)?(?:public|private|protected|default)\s+(?:final\s+)?(?:synchronized\s+)?(?:native\s+)?([^;*=]*?\(.*?\))\s*\{' 
        # NOTE link_test2_26

        pattern = r'/\*\*(.*?)\*/\s*(?:@\w+(?:\([\w._={}]+\))?\s*)?(?:public|private|protected|default)?\s+(?:final\s+)?(?:synchronized\s+)?(?:native\s+)?([^;*=]*?\(.*?\))\s*' 
        # NOTE link_test3_26

        matches = re.findall(pattern, content, re.DOTALL) 

        for match in matches:
            comment = match[0].strip().replace('*', '') # 去除首尾空格, 去除注释中的"*"
            permission_pattern = r'Requires\s+(?:the\s+)?Permission:\s*{@link\s+(.*?)}'
            permission_match = re.search(permission_pattern, comment, re.IGNORECASE) # DONE: 忽略大小写

            if permission_match:
                permission = permission_match.group(1)
                method_name = match[1] 
                print('file_path:',file_path)
                print("Permission:", permission)
                print("Method Name:", method_name)

                #将permission和method_name保存到text.txt中
                with open('link_test3_26.txt', 'a') as file:
                    file.write(f'Path: {file_path}\nMethod: {method_name}\nPermission: {permission}\n\n')

            

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



def match_import(code):
    """
    DNOE 1.2: 匹配import 存储为键值表
    """
    pattern = r'import\s+(\S+)\s*;' #\S+表示匹配任意非空白字符
    matches = re.findall(pattern, code)

    paths = {}

    for match in matches:
        element = match.split('.')[-1] # 取最后一个元素
        paths[element] = match

    print(paths)


