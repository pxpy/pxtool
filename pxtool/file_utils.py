from docx import Document
import pdfplumber
import subprocess

def extract_content_and_count(file_path: str) -> tuple[int, str]:
    """提取单个 doc, docx 或 pdf 文件的文本并返回字数和内容"""
    try:
        file_content = ""

        # 处理 doc 文件 (Mac 下调用 antiword)
        if file_path.endswith('.doc'):
            # 使用 subprocess 直接调用刚才 brew 安装的 antiword
            result = subprocess.run(['antiword', file_path], capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0:
                file_content = result.stdout
            else:
                # 如果 antiword 报错，尝试处理编码问题
                result = subprocess.run(['antiword', file_path], capture_output=True)
                file_content = result.stdout.decode('utf-8', errors='ignore')

        # 处理 docx 文件
        elif file_path.endswith('.docx'):
            doc = Document(file_path)
            paragraphs_text = [para.text for para in doc.paragraphs if para.text.strip()]
            file_content = "\n".join(paragraphs_text)

        # 处理 pdf 文件
        elif file_path.endswith('.pdf'):
            with pdfplumber.open(file_path) as pdf:
                # 提取所有页面的文字并合并
                pages_text = [page.extract_text() for page in pdf.pages if page.extract_text()]
                file_content = "\n".join(pages_text)
        elif file_path.endswith('.txt'):
            file_content = open(file_path).read()
        # 统计字数（不含空格和换行）
        word_count = len(file_content.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", ""))

        return word_count, file_content
    except Exception as e:
        print(f"无法读取文件 {file_path}: {e}")
        return 0, ""