import os

import subprocess, configparser, yaml;


# 初始化
version = "1.0"
cf = configparser.ConfigParser()

print("Multilingual Blog Manager",
    "By StonePick",
    f"版本：{version}",
    sep="\n")

# 读取 langconfig.ini ，获取语言列表
cf.read("./langconfig.ini")
main_lang = cf["LANGS"]["main_lang"]
other_lang_raw = cf["LANGS"]["other_lang"]
other_lang = other_lang_raw.split(", ")

print("博客支持的语言列表：",
    main_lang + "（主语言）",
    sep="\n")

for i in other_lang:
    print(i)

lang_list = [main_lang]
lang_list.extend(other_lang)


# 定义功能模块
def cmd_byline(*cmd):
    """在壳层执行 cmd 命令，并实时逐行打印输出。"""

    # 实时读取命令输出
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)

    # 实时打印输出
    for line in process.stdout:
        print(line.strip())

    # 等待进程结束
    process.wait()

def chk_cache(lang_list):
    """检查并处理各语言缓存文件。"""

    i = 0

    for subdir in lang_list:
        # 检查是否存在缓存文件夹
        dir_public = f"./{subdir}/public"
        dir_deploy = f"./{subdir}/.deploy_git"
        if os.path.isdir(dir_public) or os.path.isdir(dir_deploy):
            do_del = input(f"检测到网站（ {subdir} 语言）预发布文件夹。是否删除？（Y/N）")
            if do_del[0].lower() == "y":
                cmd_byline("rmdir", "/s", "/q", ".deploy_git")
                os.chdir(f"./{subdir}")
                cmd_byline("hexo", "clean")
                os.chdir("..")
            elif do_del[0].lower() == "n":
                print(f"已拒绝清理 {subdir} 缓存。")
            elif len(do_del) == 0:
                print("已忽略。")
            else:
                i += 1
                chk_cache(lang_list[i])
        else:
            print(f"语言 {subdir} 无缓存。")

def menu_modes():
    """模式选择菜单。"""

    print("1：写作",
        "2：配置",
        "3：预发布",
        "4：发布",
        "0：退出")

    # 监控输入
    switch = 1
    while switch:
        mode = input("请选择：")
        match mode:
            case "1": switch -= 1; writing()
            case "2": switch -= 1; config()
            case "3": switch -= 1; predeploy()
            case "4": switch -= 1; deploy()
            case "0": exit()
            case _:
                print("无效输入，请重试")

def writing():
    """写作模块。"""

    print("写作模式")

    # 写作菜单
    print("1：新建草稿",
          "2：新建文章",
          "3：跨语言文章管理",
          "0：返回")
    
    switch = 1
    while switch:
        mode = input("请选择：")
        match mode:
            case "1":
                switch -= 1

                # 打印语言列表
                for i in lang_list:
                    print(i)

                switch_2 = 1
                while switch_2:
                    arg_lang = input("语言：（键入0将退出）")
                    if (arg_lang not in [lang_list]) and (arg_lang != "0"):
                        print("非法输入或该语言不受支持。")
                    elif arg_lang == "0":
                        writing()
                    else:
                        if len(arg_lang) == 0:
                            # 缺省值为主语言
                            print(f"缺省值将使用主语言，{lang_list[0]}。")
                            os.chdir(f"./{lang_list[0]}")
                        else:
                            arg_title = input("标题：")
                            os.chdir(f"./{arg_lang}")
                            cmd_byline("hexo", "new", "draft", f"{arg_title}")

            case "2":
                switch -= 1
                
                # 打印语言列表
                for i in lang_list:
                    print(i)

                switch_2 = 1
                while switch_2:
                    arg_lang = input("语言：")
                    if (arg_lang not in [lang_list]) and (arg_lang != "0"):
                        print("非法输入或该语言不受支持。")
                    elif arg_lang == "0":
                        writing()
                    else:
                        if len(arg_lang) == 0:
                            # 缺省值为主语言
                            print(f"缺省值将使用主语言，{lang_list[0]}。")
                            os.chdir(f"./{lang_list[0]}")
                        else:
                            arg_title = input("标题：")
                            os.chdir(f"./{arg_lang}")
                            cmd_byline("hexo", "new", "post", f"{arg_title}")

            case "3": switch -= 1
            case "0": menu_modes()
            case _:
                print("无效输入，请重试")

def config():
    """配置模块。"""

    print("配置模式\n",
    "1：修改语言列表",
    "2：跨语言同步配置",
    "0：返回")

    switch = 1
    while switch:
        mode = input("请选择：")
        match mode:
            case "1":
                switch -= 1
                
            case "0": switch -= 1; menu_modes()
            case _:
                print("无效输入，请重试")


def predeploy():
    """预发布模块。"""

def deploy():
    """发布模块。"""

    print("1：发布",
    "0：返回")

    switch = 1
    while switch:
        mode = input("请选择：")
        match mode:
            case "1":
                switch -= 1

                if os.path.isdir(f"./{lang_list[0]}/public") == False:
                    switch_2 = 1
                    
                    while switch_2:
                        do_pred = input("未进行预发布准备，是否开始执行？（Y/N）")
                        if do_pred[0].lower() == "y":
                            switch_2 -= 1
                            predeploy()
                        elif do_pred[0].lower() == "n":
                            switch_2 -= 1
                            print(f"已拒绝执行。发布终止。")
                            deploy()
                        else:
                            continue
                else:
                    os.chdir(f"./{lang_list[0]}")
                    cmd_byline("hexo", "deploy")
            case "0":
                switch -= 1
                menu_modes()
            case _:
                print("无效输入，请重试")

# 主进程
def main():
    # 检查缓存
    chk_cache(lang_list)

    # 模式选单
    menu_modes()



if __name__ == "__main__":
    main()