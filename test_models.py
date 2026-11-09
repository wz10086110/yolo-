#!/usr/bin/env python3
"""
项目结构生成器
使用说明：
1. 运行脚本
2. 输入要分析的目录路径
3. 查看生成的树状结构
"""

import os
import sys
from pathlib import Path
root_path=r'E:\earthquake_damage_yolo\earthquake_backend'

def generate_project_structure(root_path, indent=0, last_item=False, prefix="", ignore_dirs=None, ignore_files=None):
    """
    递归生成目录结构树

    Args:
        root_path (str): 根目录路径
        indent (int): 缩进级别
        last_item (bool): 是否是最后一个项目
        prefix (str): 前缀字符串
        ignore_dirs (list): 要忽略的目录列表
        ignore_files (list): 要忽略的文件列表
    """
    if ignore_dirs is None:
        ignore_dirs = ['.git', '__pycache__', '.venv', 'venv', '.idea', '.vscode', 'node_modules', '.mypy_cache',
                       '.pytest_cache']
    if ignore_files is None:
        ignore_files = ['.gitignore', '.DS_Store', '__init__.py', 'Thumbs.db']

    try:
        # 获取当前目录下的所有项目
        items = sorted(os.listdir(root_path))

        # 过滤掉要忽略的项目
        filtered_items = []
        for item in items:
            item_path = os.path.join(root_path, item)
            if os.path.isdir(item_path):
                if item not in ignore_dirs:
                    filtered_items.append((item, 'dir'))
            else:
                if item not in ignore_files:
                    filtered_items.append((item, 'file'))

        total_items = len(filtered_items)

        for i, (item, item_type) in enumerate(filtered_items):
            is_last = (i == total_items - 1)
            item_path = os.path.join(root_path, item)

            # 确定连接符
            if indent == 0:
                connector = "└── " if is_last else "├── "
            else:
                connector = "└── " if is_last else "├── "

            # 确定前缀
            if indent > 0:
                new_prefix = prefix + ("    " if last_item else "│   ")
            else:
                new_prefix = ""

            # 打印当前项目
            if item_type == 'dir':
                print(f"{prefix}{connector}{item}/")
                # 递归处理子目录
                generate_project_structure(
                    item_path,
                    indent + 1,
                    is_last,
                    new_prefix,
                    ignore_dirs,
                    ignore_files
                )
            else:
                print(f"{prefix}{connector}{item}")

    except PermissionError:
        print(f"{prefix}{'└── ' if last_item else '├── '}[权限拒绝]")
    except Exception as e:
        print(f"{prefix}{'└── ' if last_item else '├── '}[错误: {str(e)}]")


def main():
    """主函数"""
    print("=" * 60)
    print("项目结构生成器")
    print("=" * 60)
    print("提示：")
    print("1. 输入目录路径（可以是相对路径或绝对路径）")
    print("2. 输入 'exit' 退出程序")
    print("3. 默认忽略: .git, __pycache__, venv 等目录和 .gitignore 等文件")
    print("-" * 60)

    while True:
        # 获取用户输入
        user_input = input("\n请输入目录路径 (或输入 'exit' 退出): ").strip()

        if user_input.lower() == 'exit':
            print("程序退出。")
            break

        if not user_input:
            print("错误：路径不能为空！")
            continue

        # 转换为绝对路径
        target_path = os.path.abspath(user_input)

        # 验证路径是否存在
        if not os.path.exists(target_path):
            print(f"错误：路径 '{target_path}' 不存在！")
            continue

        if not os.path.isdir(target_path):
            print(f"错误：'{target_path}' 不是一个目录！")
            continue

        print(f"\n{'=' * 60}")
        print(f"项目结构: {target_path}")
        print(f"{'=' * 60}")

        try:
            # 打印根目录
            root_name = os.path.basename(target_path) or os.path.basename(os.path.dirname(target_path))
            print(f"{root_name}/")

            # 生成项目结构
            generate_project_structure(
                target_path,
                indent=0,
                last_item=True,
                prefix=""
            )

            print(f"\n{'=' * 60}")
            print("生成完成！")
            print(f"{'=' * 60}")

        except Exception as e:
            print(f"生成过程中出错: {str(e)}")
            print("请检查路径权限或尝试其他目录。")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断。")
    except Exception as e:
        print(f"发生未预期错误: {str(e)}")
    finally:
        sys.exit(0)