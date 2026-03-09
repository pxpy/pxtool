import os
from http import HTTPStatus
from typing import Optional

import dashscope

def process_with_llm(prompt:str, content: Optional[str] = None, model: Optional[str] = "qwen3-max"):

    if content is None:
        messages = [
            {'role': 'system', 'content': prompt}
        ]
    else:
        messages = [
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': content}
        ]

    # 4. 调用 AI (DashScope Application)
    try:

        response = dashscope.Generation.call(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            # model="qwen3-max",
            model= model,
            # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=messages,
            result_format='message'
        )

        if response.status_code == HTTPStatus.OK:
            print(response.usage.input_tokens)
            analysis_text = response.output.choices[0].message.content
            return analysis_text
        else:
            return f"调用失败，状态码: {response.status_code}，消息: {response.message}"
    except Exception as e:
        return f"调用 AI 接口异常: {e}"
def long_text_analysis(txt):
    from openai import OpenAI

    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),  # 如果您没有配置环境变量，请在此处替换您的API-KEY
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务base_url
    )
    # 初始化messages列表
    completion = client.chat.completions.create(
        model="qwen-long",
        messages=[
            {'role': 'user', 'content': txt}
        ],
        # 所有代码示例均采用流式输出，以清晰和直观地展示模型输出过程。如果您希望查看非流式输出的案例，请参见https://help.aliyun.com/zh/model-studio/text-generation
        # stream=True,
        # stream_options={"include_usage": True}
    )
    return completion.choices[0].message.content