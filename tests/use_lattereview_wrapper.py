#!/usr/bin/env python3
"""
在AutoSurvey根目录使用LatteReview Wrapper包的示例
"""

import sys
from pathlib import Path

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

def import_and_use_wrapper():
    """导入并使用LatteReview Wrapper包"""
    print("=== 导入LatteReview Wrapper包 ===")
    
    try:
        # 方法1: 从包导入
        from lattereview_wrapper import run_lattereview_evaluation_sync
        print("✅ 成功从包导入主要函数")
        
        # 显示可用函数
        from lattereview_wrapper import __all__
        print(f"可用函数: {__all__}")
        
        return True
        
    except ImportError as e:
        print(f"❌ 从包导入失败: {e}")
        
        try:
            # 方法2: 直接导入
            from lattereview_wrapper.lattereview_wrapper import run_lattereview_evaluation_sync
            print("✅ 成功直接导入函数")
            return True
            
        except ImportError as e2:
            print(f"❌ 直接导入也失败: {e2}")
            return False


def show_package_structure():
    """显示包结构"""
    print("\n=== 包结构 ===")
    
    wrapper_dir = Path(__file__).parent / "lattereview_wrapper"
    if wrapper_dir.exists():
        print(f"包目录: {wrapper_dir}")
        print("包含文件:")
        for file in wrapper_dir.iterdir():
            if file.is_file():
                print(f"  📄 {file.name}")
            else:
                print(f"  📁 {file.name}")
    else:
        print("❌ 包目录不存在")


def show_usage_examples():
    """显示使用示例"""
    print("\n=== 使用示例 ===")
    
    print("1. 基本导入:")
    print("   from lattereview_wrapper import run_lattereview_evaluation_sync")
    
    print("\n2. 基本使用:")
    print("   result = run_lattereview_evaluation_sync(")
    print("       topic='AI Research',")
    print("       reviewer_models=['gpt-4o-mini', 'gpt-4.1-mini', 'gpt-5-mini'],")
    print("       papers=[...]")
    print("   )")
    
    print("\n3. 查看详细文档:")
    print("   cd lattereview_wrapper")
    print("   cat README.md")
    print("   cat QUICKSTART_LatteReview.md")


def main():
    """主函数"""
    print("LatteReview Wrapper 包使用示例")
    print("=" * 50)
    
    # 显示包结构
    show_package_structure()
    
    # 尝试导入包
    if import_and_use_wrapper():
        print("\n✅ 包导入成功!")
        show_usage_examples()
        
        print("\n📚 下一步:")
        print("1. 查看详细文档: cd lattereview_wrapper && cat README.md")
        print("2. 运行快速开始: cd lattereview_wrapper && cat QUICKSTART_LatteReview.md")
        print("3. 运行示例: cd lattereview_wrapper && python simple_example.py")
        print("4. 运行测试: cd lattereview_wrapper && python test_lattereview_wrapper.py")
        
    else:
        print("\n❌ 包导入失败!")
        print("\n🔧 解决方案:")
        print("1. 检查包目录是否存在")
        print("2. 安装依赖: cd lattereview_wrapper && pip install -r requirements_lattereview.txt")
        print("3. 检查Python路径设置")
        print("4. 查看错误信息进行调试")


if __name__ == "__main__":
    main()
