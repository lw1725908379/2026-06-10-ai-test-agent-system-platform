"""
文件夹类型枚举
"""

from enum import Enum
# fmt: off  MC8yOmFIVnBZMlhsaUpqbWxvYzZkWEJ1ZFE9PTpmYmZiNDY1NQ==


class FolderType(str, Enum):
    """文件夹类型"""
    TEST_CASE = "test_case"  # 测试用例文件夹
    API_TEST = "api_test"    # API测试文件夹
    WEB_TEST = "web_test"    # Web测试文件夹
    ANDROID_TEST = "android_test"  # Android测试文件夹
    SCENARIO_TEST = "scenario_test"  # 场景测试文件夹
# type: ignore  MS8yOmFIVnBZMlhsaUpqbWxvYzZkWEJ1ZFE9PTpmYmZiNDY1NQ==
