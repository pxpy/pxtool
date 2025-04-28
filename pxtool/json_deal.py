import re


def remove_json_wrapper(text):
    # 匹配以```开头，可能带json标识的代码块，兼容各种换行符和空格
    pattern = r'^```(?:json\s*)?([\s\S]*?)```$'

    match = re.search(pattern, text.strip())
    if match:
        return match.group(1).strip()
    return text.strip()  # 如果没有匹配则返回原文本，去除首尾空白

if  __name__ == '__main__':
    # 测试多种情况
    test_cases = [
        # 标准带json标识
        """```json
    {
      "线索有效性分值": 20
    }
    ```""",

        # 无json标识
        """
    {
      "线索优先级": "B"
    }
    """,

        # 带换行符变种
        """
    
    {
      "推荐下次拨打时间": "2025年2月17日"
    }
     """,

        # 混合换行符
        """```json\n{  "关注的车型": ["EQM5"]}\n```"""
    ]

    for i, case in enumerate(test_cases, 1):
        print(f"Case {i} Result:")
        print(remove_json_wrapper(case))
        print("-" * 30)
