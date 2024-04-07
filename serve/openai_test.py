import base64
from openai import OpenAI
import httpx

# 将本地图片转换为Base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# 图片的本地路径
# image_path = "/mnt/VisDiff/data/teaser.png"
image_path = "/mnt/VisDiff/data/mvtec_examples/set_a/001.png" 
image_base64 = image_to_base64(image_path)

# 创建OpenAI客户端
client = OpenAI(
    base_url="https://api.xty.app/v1", 
    api_key="sk-vQIOfXZ8olru1QPIDe068f3fE637418a9aDf4a495147E9Af",  # 使用您自己的API密钥
    http_client=httpx.Client(
        base_url="https://api.xty.app/v1",
        follow_redirects=True,
    ),
)

# 使用Base64编码的图片构建请求
response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image in detail."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}",
                        },
                },
            ],
        }
    ],
    max_tokens=1024
)

# print(response)
content = response.choices[0].message.content
print(content)