import base64
from openai import OpenAI
import httpx
import os

# 将本地图片转换为Base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image

# 创建OpenAI客户端
client = OpenAI(
    base_url="https://api.xty.app/v1", 
    api_key="sk-vQIOfXZ8olru1QPIDe068f3fE637418a9aDf4a495147E9Af",  # 使用您自己的API密钥
    http_client=httpx.Client(
        base_url="https://api.xty.app/v1",
        follow_redirects=True,
    ),
)

# 图片的本地路径
image_path_nominal = "/mnt/VisDiff/data/mvtec_anomaly_detection/bottle/train/good/000.png"
image_base64_nominal = image_to_base64(image_path_nominal)



def add_user_message(msg, text, image_base64):
    msg.append({
        "role": "user",
        "content": [
            {"type": "text", "text": text},
            {"type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_base64}",
                },
            },
            ],
    },)
    return msg

def add_system_response(msg):
    response = client.chat.completions.create(
    model="gpt-4-vision-preview",  # 或者使用你需要的模型，如"gpt-4"如果可用
    messages=msg,
    max_tokens=1024
    )
    msg.append({"role": "system", "content": response.choices[0].message.content})
    print(response.choices[0].message.content)
    return msg, response.choices[0].message.content
    
ori_messages = []    
ori_messages = add_user_message(ori_messages, "Below are the standard samples. \
                Please take note of them as references.", image_base64_nominal)
ori_messages, response = add_system_response(ori_messages)  # 系统根据用户的消息生成回复

# 指定包含图片的目录
object_type = "bottle"
object_class = "contamination"
directory_path = f"/mnt/VisDiff/data/mvtec_anomaly_detection/{object_type}/test/{object_class}"
# 结果文件夹
results_dir = "results/gpt4v/"
# 确保结果目录存在
os.makedirs(results_dir, exist_ok=True)
# 结果文件名
results_file = f"{results_dir}zs_1_NS_{object_type}_test_{object_class}.txt"

# 准备写入结果
with open(results_file, 'w') as file:
    # 遍历目录中的每个文件
    for filename in os.listdir(directory_path):
        if filename.endswith(".png"):  # 确保只处理PNG图片
            image_path = os.path.join(directory_path, filename)
            image_base64_test = image_to_base64(image_path)
            
            # 对图片进行分类
            # classification_result = classify_image(image_path)
            local_ori_messages = ori_messages.copy()
            msg = add_user_message(local_ori_messages, "Based on the reference. Classify it as \
                nominal or anomalous. Just reply 0 if it’s nominal or 1 if it’s anomalous.", image_base64_test)
            # print(msg)
            new_msg, classification_result = add_system_response(msg)
            # print(classification_result)
            # 将结果写入文件
            file.write(f"Image: {filename} is {'nominal' if classification_result == '0' else 'anomalous'}\n")

print(f"Classification results saved to {results_file}")

# image_path_test = "/mnt/VisDiff/data/mvtec_anomaly_detection/bottle/test/good/000.png"
# image_base64_test = image_to_base64(image_path_test)

# add_user_message("Based on the reference. Classify it as nominal or anomalous. Just reply 0 if it’s nominal or 1 if it’s anomalous.", image_base64_test)
# add_system_response()  # 系统再次根据用户的新消息和之前的对话历史生成回复

