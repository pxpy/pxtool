# pxtool

pxtool 是一个Python工具集合，提供了日志处理和JSON文本处理等实用功能。

## 安装

```bash
pip install pxtool
```

## 功能特性

### 1. 日志处理 (set_log)
- 支持彩色控制台输出
- 自动创建日志文件并按日期命名
- 支持自定义日志级别（包括TRACE级别）
- 同时输出到文件和控制台

示例：
```python
from pxtool import setup_logger
import logging

# 初始化日志配置
setup_logger(log_filename_prefix='myapp', level=logging.INFO)

# 使用日志
logging.debug("调试信息")
logging.info("普通信息")
logging.warning("警告信息")
logging.error("错误信息")
```

### 2. JSON处理 (json_deal)
- 移除JSON文本中的Markdown代码块包装
- 支持多种格式的JSON文本清理

示例：
```python
from pxtool import remove_json_wrapper

json_text = '''```json
{
    "name": "pxtool",
    "version": "0.1.0"
}
```'''

cleaned_json = remove_json_wrapper(json_text)
print(cleaned_json)
```

## 要求
- Python >= 3.6
- termcolor (用于彩色日志输出)

## 许可证
MIT License

## 作者
- 作者：px
- 邮箱：panxin@panxin.me
- 项目地址：https://github.com/pxpy/pxtool