import os
import re


'''
from: my_mapping_2.py

string_dict = {

    "method_string": {permissions} (set)
    //"method_string" = method_dic["file_path"] + "." + method_dic["method_name"] + method_dic["method_arg"] + method_dic["return_value"]
}
'''


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
 
        #pattern = r'@RequiresPermission\(([^*]*?)\)\s*(?:@(?:[\w._={}]+)(?:\([\w._]+\))?\s*)*\s*(?:public\s+|private\s+|protected\s+|default\s+)*(?:abstract\s+|static\s+|final\s+|synchronized\s+|native\s+|transient\s+)*(?:@(?:[\w.]+)\s+)*([^;*=/]*?\(.*?\))' #OK
        # DEBUG 29: 除去括号中的=
        pattern = r'@RequiresPermission\(([^*]*?)\)\s*(?:@(?:[\w._={}]+)(?:\([\w._]+\))?\s*)*\s*(?:public\s+|private\s+|protected\s+|default\s+)*(?:abstract\s+|static\s+|final\s+|synchronized\s+|native\s+|transient\s+)*(?:@(?:[\w.]+)\s+)*([^;*=/]*?\([^=]*?\))' 
        
        # DONE: 删除@...
        # DONE: 匹配函数名 *? > [^;*=]*+


        matches = re.findall(pattern, content, re.DOTALL) 
        if not matches: # 如果没有匹配到, 则返回
            return

        # 4. 存储格式化结果
        #   4.1 method_dic {file_path:..., 'permission':{...}, 'return_value':..., 'method_arg':...}
        #   4.2 method_dic {method_name: method_dic}
        string_dict = {} # per file

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
            # 4.1a 把file_path和permission 存储到method_dic
            method_dic = {}
            method_dic["file_path"] = file_path[96:-5].replace("\\", ".") #分隔
            method_dic["permission"] = permission_dic #分隔
            #print("permission:",method_dic["permission"],"\n")
            #print("method_dic:", method_dic, "\n")


            # 3.处理return_value,method_arg,method_name
            method = match[1].replace("\n","") 

            # 3.1 return_value
            if method.startswith("("):  #NOTE: 去除强制匹配
                continue
            #print("method:", method)
            return_value = method.split(' ')[0] # OK
            #print("return_value:", return_value)


            # 3.2 method_args 
            method_arg = ""
            method_arg_per = []
            args = re.search(r'\((.*)\)',method).group(1)
            if args:
                for arg in args.split(","): 

                    # DONE: DEBUG 
                    # NOTE: 匹配前面可能的final和@.. (不计顺序)
                    #find = re.search(r'(?:(?:final\s*)|(?:@(?:[\w.]+)\s+))*([\w.<>\[\]]+)\s', arg).group(1)
                    find = re.search(r'\s*(?:(?:final\s*)|(?:@(?:[\w.]+)\s+))*([\w.<>\[\]]+)\s?', arg).group(1)  # DEBUG: 28 加上了<>

                    method_arg_per.append(find) 

                    
                method_arg = "(" + ",".join(method_arg_per) + ")"
            else:
                method_arg = "()"
            #print("method_arg:", method_arg)  

            # 4.1b 把返回值和参数类型 存储到method_dic中
            method_dic["return_value"] = return_value
            method_dic["method_arg"] = method_arg


            # 3.3 method_name
            #method_name = re.search(r'\s+(\w+)\(', method).group(1)
            method_name = re.search(r'\s?([\w.]+)\s*\(', method).group(1)   # DEBUG 28: 加上了\s*, 29: 加上了[.]
            #print("method_name:", method_name, "\n")
            method_dic["method_name"] = method_name

            # 5 写入最终的dict
            
            method_string = method_dic["file_path"] + "." + method_dic["method_name"] + method_dic["method_arg"] + method_dic["return_value"]
            string_dict[method_string] = method_dic["permission"]


        #print("method_dic",method_dic,"\n")
    return string_dict 
    

def get_files(folder_path):
    """
    3.读取文件夹中的所有.java文件
    DONE: 保存对应的文件路径
    """
    files = []
    string_dict_1 = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)

                requires_dict = requires_permission(file_path)
                if requires_dict:
                        string_dict_1.update(requires_dict)


    return string_dict_1 


 
# 示例 
# or folder_path = sys.argv[1]

for api_level in range(26, 34):
    file_path = 'D:/CLASS/1 Now/texwork/shared/permission/sdk_source/android-sdk-sources-for-api-level-{level}-master/'.format(level=api_level) 
    #file_path = 'D:/CLASS/1 Now/texwork/shared/permission/sdk_source/android-sdk-sources-for-api-level-26-master/' 

    string_dict = get_files(file_path)

    with open('string_dict_{level}.txt'.format(level=api_level), 'a') as file:
        for key,value in string_dict.items():
            file.write(f'{key} :: {",".join(value)}\n')