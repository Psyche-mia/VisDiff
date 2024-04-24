from modelscope import (
    snapshot_download, AutoModelForCausalLM, AutoTokenizer, GenerationConfig
)
import torch
import base64
import httpx
import os
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Run anomaly detection on images.")
parser.add_argument("--object_type", type=str, required=True, help="Type of object to analyze")
parser.add_argument("--object_class", type=str, required=True, help="Class of the anomaly")
args = parser.parse_args()

model_id = 'Qwen/Qwen-VL-Chat-Int4'
revision = 'v1.0.0'

model_dir = snapshot_download(model_id, revision=revision)
torch.manual_seed(1234)

tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
if not hasattr(tokenizer, 'model_dir'):
    tokenizer.model_dir = model_dir

model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", trust_remote_code=True).eval()
 
# 图片的本地路径
image_path_nominal = f"/mnt/VisDiff/data/mvtec_anomaly_detection/{args.object_type}/train/good/000.png"

# 1st dialogue turn
first_query = tokenizer.from_list_format([
    {'image': image_path_nominal}, # Either a local path or an url
    {'text': 'Below are the standard samples. Please take note of them as references. Your task is to identify any samples that deviate from these norms.\
        (No need to reply image.)'},
])
response, history = model.chat(tokenizer, query=first_query, history=None)
print(response)

test_path = f"/mnt/VisDiff/data/mvtec_anomaly_detection/{args.object_type}/test/{args.object_class}/000.png"

# 指定包含图片的目录
directory_path = f"/mnt/VisDiff/data/mvtec_anomaly_detection/{args.object_type}/test/{args.object_class}"
# 结果文件夹
results_dir = "results/qwen-vl/"
# 结果文件名
results_file = f"{results_dir}SLC/zs_1_NS_{args.object_type}_test_{args.object_class}.txt"

# 2nd dialogue turn
second_query = tokenizer.from_list_format([
    {'image': image_path_nominal}, # Either a local path or an url
    {'text': 'Based on the reference. Classify it as nominal or anomalous. If it’s nominal, reply 0. (No need to reply image.)'},
])
response, history_new = model.chat(tokenizer, query=second_query, history=history)
print(response)
# print(response)
# <ref>"击掌"</ref><box>(211,412),(577,891)</box>
# image = tokenizer.draw_bbox_on_latest_picture(response, history)
# if image:
#   image.save('output_chat.jpg')
# else:
#   print("no box")