#!/usr/bin/env python
# -*- coding: utf-8 -*-
# * filename   : back_ani.py
# * created at : 2023-04-04 14:48:13
# * Author     : xiliuya <xiliuya@aliyun.com>
import sys
import os


def find_dir_file(root):
    file_name_list = []
    for item in os.listdir(root):
        if os.path.isfile(os.path.join(root, item)) and ".plist" in item:
            file_name_list.append(root + "/" + item)
    return file_name_list


def find_json_file(root):
    file_name_list = []
    for item in os.listdir(root):
        if os.path.isfile(os.path.join(root, item)) and ".ExportJson" in item:
            file_name_list.append(root + "/" + item)
    return file_name_list


if __name__ == '__main__':
    dirname = sys.argv[1]
    proj_name = os.path.basename(dirname) if os.path.basename(
        dirname) else os.path.basename(os.path.dirname(dirname))
    out_dir = "out/" + proj_name

    if not os.path.exists('out/'):
        os.system('mkdir out/')

    if os.path.exists(out_dir):
        print("文件已存在, 请清理 out/ 目录.")
        sys.exit()

    os.system('cp -r NewAnimation/ ' + out_dir)

    # 重命名项目文件内容
    os.system('mv ' + out_dir + "/NewAnimation.xml.animation " + out_dir +
              "/" + proj_name + ".xml.animation")
    os.system('mv ' + out_dir + "/Ruler/NewAnimation.xml " + out_dir +
              "/Ruler/" + proj_name + ".xml")

    # 替换项目文件内容
    os.system('grep -rl NewAnimation ' + out_dir +
              ' | xargs sed -i "s/NewAnimation/' + proj_name + '/g"')

    # 复制资源到 out_dir/Resources/
    file_list = find_dir_file(dirname)
    for file in file_list:
        if os.path.isfile(file.replace('.plist', '.png')):
            os.system("python texture_unpacker/unpack_plist.py " +
                      file.replace('.plist', ''))
            os.system('mv ' + file.replace('.plist', '') + "/* " + out_dir +
                      '/Resources/')

    # 复制资源到out_dir/Resources
    os.system('cp ' + dirname + "/* " + out_dir + '/Resources/')

    # 复制jons到out_dir/Json
    json_list = find_json_file(dirname)
    for json_file in json_list:
        os.system('cp ' + json_file + " " + out_dir + '/Json/' +
                  os.path.basename(json_file.replace(".ExportJson", ".json")))
