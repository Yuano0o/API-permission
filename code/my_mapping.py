import sys
import os
import re

# TODO for 1,2: 保留匹配的完整/原始match字符串 以便检查匹配是否正确 
# TODO 分别提取 @RequiresPermission 和 {@link} 两种注解的权限, 保存为JSON格式 (同一个JSON)

# 1.扫描每个 .java文件, 用正则表达式匹配@RequiresPermission字符串
# link DONE 1.2: 匹配import 存储为键值表 
# TODO: anyof 和 allof 的处理, 统一用,分隔
# TODO: 最后处理成explorer的格式
# DONE: 匹配java修饰符 
def extract_permissions(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

        # 查找带有权限注解的方法
        #pattern = r'@RequiresPermission\((.*?)\)\s*public\s+(?:final\s+)?(?:synchronized\s+)?(?:native\s+)?(.*?)\(' # NOTE 标准匹配 
        #pattern = r'@RequiresPermission\((.*?)\)\s*public\s+(?:final\s+)?(?:synchronized\s+)?(?:native\s+)?([^;*=]*?\(.*?\))' # NOTE 去除强制匹配
        pattern = r'@RequiresPermission\((.*?)\)\s*(?:@\w+\([\w.]+\)\s*)?\s*(?:public|private|protected|default)\s+(?:final\s+)?(?:synchronized\s+)?(?:native\s+)?([^;*=]*?\(.*?\))'  ## NOTE 匹配中间可能的注解
        #(?:@\w+\([\w.]+\)\s*)? 
        matches = re.findall(pattern, content, re.DOTALL) 
        if not matches: # 如果没有匹配到, 则返回
            return
        #print(matches)
        permissions = []
        for match in matches:
            permission_string = match[0]
            method_name = match[1] # match[1]?
            print("Permission:", permission_string)
            print("Method Name:", method_name)
            permissions.append((method_name, permission_string))
    
        return permissions
#1.


# 2.匹配{@link android.Manifest.permission#}
#DONE: 匹配方法名 ok
#DONE: 匹配完 删除"*"
#DONE: public 前面如果有注解?
def link_permission(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

        # DONE: 匹配每个/** */后的第一个method
        pattern = r'/\*\*(.*?)\*/\s*.*?(?:public|private|protected|default)\s+(?:final\s+)?(?:synchronized\s+)?(?:native\s+)?(.*?\(.*?\))' 
        # NOTE link [2.1]
        
        matches = re.findall(pattern, content, re.DOTALL) 

        for match in matches:
            comment = match[0].strip().replace('*', '') # 去除首尾空格, 去除注释中的"*"

            permission_pattern = r'Requires\s+(?:the\s+)?Permission:\s*{@link\s+(.*?)}'
            # DONE: 匹配多种模式 如 require the {@link android.Manifest.permission#NFC} permission.
            #permission_pattern = r'{@link\s+(.*?)}\s+permission' # DONE 需要更精准的匹配
            permission_match = re.search(permission_pattern, comment, re.IGNORECASE) # DONE: 忽略大小写

            if permission_match:
                permission = permission_match.group(1)
                method_name = match[1] 
                
                print("Permission:", permission)
                print("Method Name:", method_name)

#2.

# 3.读取文件夹中的所有.java文件
# TODO: 保存对应的文件路径
def get_files(folder_path):
    files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                #extract_permissions(file_path)
                link_permission(file_path)

                #files.append(file_path)
                #print(file_path)
                #print(extract_permissions)
    return 0 #files # 返回文件路径列表
# 3.


# 4.将提取的权限信息保存到test.txt文件中
def save_to_file(permissions):
    with open('test.txt', 'w') as file:
        for method_name, permission in permissions:
            file.write(f'Method: {method_name}\tPermission: {permission}\n')
#4.


# 示例 
# or folder_path = sys.argv[1]
file_path = 'D:/CLASS/1 Now/texwork/shared/permission/android-sdk-sources-for-api-level-26-master/' #/android/service/oemlock/OemLockManager.java'
print(get_files(file_path))

# DNOE 1.2.匹配import 存储为键值表
def match_import(code):
    pattern = r'import\s+(\S+)\s*;' #\S+表示匹配任意非空白字符
    matches = re.findall(pattern, code)

    paths = {}

    for match in matches:
        element = match.split('.')[-1] # 取最后一个元素
        paths[element] = match

    print(paths)


