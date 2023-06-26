import os
import re

def match_import(code):
    """
    匹配import 存储为键值表
    """
    pattern = r'import\s+(\S+)\s*;' #\S+表示匹配任意非空白字符
    matches = re.findall(pattern, code)

    paths = {}

    for match in matches:
        element = match.split('.')[-1] # 取最后一个元素
        paths[element] = match

    return paths

def requires_permission(file_path, content):

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

    # NOTE: 匹配@RequiresPermission(...^*) + 可能的注解@xxx()/@xxx + java修饰符若干/无修饰符 + 关建字若干/无 + 返回值,方法名,参数(并去除;*=的强制匹配) 
    # NOTE: 去除强制匹配的例子: [^;*=]*?(除去变量,注释等)   [^*](除去注释) 

    pattern = r'@RequiresPermission\(([^*]*?)\)\s*(?:@(?:[\w._={}]+)(?:\([\w._]+\))?\s*)*(?:public\s+|private\s+|protected\s+|default\s+)*(?:abstract\s+|static\s+|final\s+|synchronized\s+|native\s+|transient\s+)*(?:@(?:[\w.]+)\s+)*([^;*=/]*?\([^;]*?\))' 

    matches = re.findall(pattern, content, re.DOTALL) 
    if not matches: 
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
            if "conditional" not in permission: #NOTE: 去除强制匹配
                permission_dic.add("android.permission." + permission.split(".")[-1])


        # 2.处理file_path
        # 4.1a 把file_path和permission 存储到method_dic
        method_dic = {}
        method_dic["file_path"] = file_path[96:-5].replace("\\", ".") #分隔
        method_dic["permission"] = permission_dic #分隔

        # 3.处理return_value,method_arg,method_name
        method = match[1].replace("\n","") 

        # 3.1 return_value
        if method.startswith("("):  #NOTE: 去除强制匹配
            continue
        return_value = method.split(' ')[0] # OK

        # 3.2 method_args 
        #add: 匹配import
        import_dict = match_import(content)

        method_arg = ""
        method_arg_per = []
        args = re.search(r'\((.*)\)',method).group(1)
        if args:
            
            for arg in args.split(","):  
                #更好的解决方案: 按","分隔, 但不匹配()内的","
                if re.search(r'[\(\)\<\>]',arg): #如果是匹配了(),<>内的",", 则跳过
                    continue 
                if len(arg.split(' ')) >1 : 
                    find = arg.split(' ')[-2]
                else:
                    continue 
 
                if find in import_dict: #如果是import的类, 则替换
                    find = import_dict[find]
                
                match_array = re.search(r'(.*)?\[\]', find) #匹配数组
                if match_array:
                    find = "[" + match_array.group(1)

                find = find.replace("String", "java.lang.String")

                method_arg_per.append(find) 

                
            method_arg = "(" + ",".join(method_arg_per) + ")"
        else:
            method_arg = "()"

        # 4.1b 把返回值和参数类型 存储到method_dic中
        method_dic["return_value"] = return_value
        method_dic["method_arg"] = method_arg


        # 3.3 method_name
        #method_name = re.search(r'\s+(\w+)\(', method).group(1)
        method_name = re.search(r'\s?([\w.]+)\s*\(', method).group(1)   # DEBUG 28: 加上了\s*, 29: 加上了[.]
        method_dic["method_name"] = method_name

        # 5 写入最终的dict
        
        method_string = method_dic["file_path"] + "." + method_dic["method_name"] + method_dic["method_arg"] + method_dic["return_value"]
        string_dict[method_string] = method_dic["permission"]



    return string_dict 


def link_permission(file_path, content):
    """
    2.匹配{@link android.Manifest.permission#}
    """


    # NOTE link_test7_26 (the methods matched are the same as test7)   
    # 匹配/** */后的第一个method
    # pattern = r'/\*\*(.*?)\*/\s*(?:@\w+(?:\([\w.={}]+\))?\s*)?(?:public|private|protected|default)\s+(?:abstract\s+|static\s+|final\s+|synchronized\s+|native\s+|transient\s+)?([^;*=]*?\(.*?\))' 
    # NOTE: 匹配/** */ + 可能的注解@xxx()/@xxx + java修饰符若干(防止强制匹配) + 关建字若干/无 + 返回值,方法名,参数(并去除;*=的强制匹配)

    # NOTE link_test10_26 移除返回值类型的修饰 
    pattern = r'/\*\*(.*?)\*/\s*(?:@(?:[\w.]+)(?:\([\w.={}]+\))?\s*)*\s*(?:public\s+|private\s+|protected\s+|default\s+)(?:abstract\s+|static\s+|final\s+|synchronized\s+|native\s+|transient\s+)*(?:@(?:[\w.]+)\s+)*([^;*=/]*?\([^=]*?\))'
    

    matches = re.findall(pattern, content, re.DOTALL) 

    # 4. 存储格式化结果
    
    string_dict = {}  # per file

    for match in matches:
        comment = match[0].strip().replace('*', '') # 去除首尾空格, 去除注释中的"*"
        
        
        #      NOTE: 匹配
        #      * Requires Permission: {@link android.Manifest.permission#READ_PRECISE_PHONE_STATE
        #      * READ_PRECISE_PHONE_STATE}
        #      或
        #      * Requires Permission: {@link android.Manifest.permission#READ_PRECISE_PHONE_STATE}
        permission_pattern = r'{@link android.Manifest.permission#(\w+)(\s+|\})' 
        permission_match = re.findall(permission_pattern, comment, re.IGNORECASE) # DONE: 忽略大小写
        
        if permission_match:
            #print("permission_match:", permission_match, "\n")

            permission = set()
            for permissions in permission_match:
                permission.add("android.permission." + permissions[0])

            method = match[1].replace("\n","")
            #print("method:", method, "\n")

            if method.startswith("("):  #NOTE: 去除强制匹配
                continue

            # 1.处理permission
            # 1.2.以集合形式存储permission
            #permission_dic = set ()
            method_dic = {}

            method_dic["permission"] = permission
            method_dic["file_path"] = file_path[96:-5].replace("\\", ".") #分隔
            method_name = re.search(r'\s?([\w.]+)\s*\(', method).group(1)
            method_dic["method_name"] = method_name


            # 3.2 method_args 
            #add: 匹配import
            import_dict = match_import(content)
            
            method_arg = ""
            method_arg_per = []
            args = re.search(r'\((.*)\)',method).group(1)
            if args:

                for arg in args.split(","):  
                    #更好的解决方案: 按","分隔, 但不匹配()内的","
                    if re.search(r'[\(\)\<\>]',arg): #如果是匹配了(),<>内的",", 则跳过
                        continue 
                    if len(arg.split(' ')) >1 : 
                        find = arg.split(' ')[-2]
                    else:
                        continue 


                    if find in import_dict: #如果是import的类, 则替换
                        find = import_dict[find]
                    
                    match_array = re.search(r'(.*)?\[\]', find) #匹配数组
                    if match_array:
                        find = "[" + match_array.group(1)
                    
                    find = find.replace("String", "java.lang.String") #单独处理String

                    method_arg_per.append(find)

                    
                method_arg = "(" + ",".join(method_arg_per) + ")"
            else:
                method_arg = "()"


            # 4.1b 把返回值和参数类型 存储到method_dic中
            method_dic["method_arg"] = method_arg

            return_value = method.split(' ')[0] # OK
            method_dic["return_value"] = return_value

            # 5 写入最终的dict
            
            method_string = method_dic["file_path"] + "." + method_dic["method_name"] + method_dic["method_arg"] + method_dic["return_value"]
            string_dict[method_string] = method_dic["permission"]



    return string_dict



def get_files(folder_path):
    """
    3.读取文件夹中的所有.java文件
    DONE: 保存对应的文件路径
    """
    files = []
    string_dict_1 = {}
    string_dict_2 = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)

                with open(file_path, 'r') as file:
                    content = file.read()

                    pattern = r"//.*"  # 匹配以双斜杠 "//" 开始的注释
                    content = re.sub(pattern, '', content)  # 将匹配到的注释替换为空字符串

                    requires_dict = requires_permission(file_path,content)
                    if requires_dict:
                            string_dict_1.update(requires_dict)

                    link_dict = link_permission(file_path,content)
                    if link_dict:
                            string_dict_2.update(link_dict)


    # 用@link的结果 与 requires的结果合并
    for key,value in string_dict_2.items():
        if key in string_dict_1:
            string_dict_1[key] = string_dict_1[key].union(value)
        else:
            string_dict_1[key] = value


    return string_dict_1 


'''
NOTE:
string_dict = {

    "method_string": {permissions} (set)
    //"method_string" = method_dic["file_path"] + "." + method_dic["method_name"] + method_dic["method_arg"] + method_dic["return_value"]
}
'''
for api_level in range(26, 34):
    file_path = 'D:/CLASS/1 Now/texwork/shared/permission/sdk_source/android-sdk-sources-for-api-level-{level}-master/'.format(level=api_level) 

    string_dict = get_files(file_path)

    with open('string_dict_{level}.txt'.format(level=api_level), 'a') as file:
        for key,value in string_dict.items():
            permission = ",".join(value)
            file.write(f'{key} :: {permission}\n')