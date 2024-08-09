import logging
import random
import sys

import websocket
import websockets
import requests
from flask import Flask, jsonify,request
import json
from flask_cors import CORS

import uuid

app = Flask(__name__)
CORS(app)

client_id = str(uuid.uuid4())
comfyui_host = os.getenv("comfyui_host")
comfyui_port = os.getenv("comfyui_port")
host = comfyui_host
port = comfyui_port

logging.basicConfig(level=logging.INFO,stream=sys.stdout,format='%(asctime)s - %(levelname)s - %(message)s')


# 生成提交任务的请求体，前端传参主要修改函数
def task_body(positive_prompt:str,negative_prompt:str,width:int,height:int,batch_size:int):
    with open("workflow_json\\txt2img.json","r",encoding="utf-8") as file:
        data =json.load(file)

        # 随机种子
        random.seed()
        data["3"]["inputs"]["seed"] = random.randint(1234,999999)
        print(random.randint(1234,999999))
        # 正向提示词替换
        data["15"]["inputs"]["text"] = positive_prompt
        # 反向提示词替换
        data["61"]["inputs"]["text"] = negative_prompt
        # 生成图片宽度
        data["5"]["inputs"]["width"] = width
        # 生成图片高度
        data["5"]["inputs"]["height"] = height
        # 生成图片数量
        data["5"]["inputs"]["batch_size"] = batch_size

        bodydata ={"client_id":client_id,"prompt":data}
        logging.info(f"请求的body: {json.dumps(bodydata)}")
        return json.dumps(bodydata)

# 提交任务（得到prompt_id）
def task_prompt(bodydata):
    img_data = requests.post(f"http://{host}:{port}/prompt",data=bodydata,headers={"Content-Type": "application/json"})
    if img_data.status_code ==200:

        resp_data = json.loads(img_data.text)
        prompt_id = resp_data.get("prompt_id")
        # print(prompt_id)
        return prompt_id
    else:
        logging.error(f"下发任务失败: {img_data.status_code}")
        logging.WARN(f"返回值为: {img_data.text}")

# 通过prompt_id获取任务数据
def task_data(prompt_id):
   ws_uri = f"ws://{host}:{port}/ws?clientId={client_id}"
   ws = websocket.create_connection(ws_uri)
   while True:
        msg = ws.recv()
        logging.info(f"WebSocket返回消息: {msg}")
        if isinstance(msg,str):
            ws_msg = json.loads(msg)
            # 判断状态
            if ws_msg.get("type") == "executing" and ws_msg.get("data",{}).get("node") is None:
                data = ws_msg["data"]
                print(f"data为:{data}")
                data = requests.get(f"http://{host}:{port}/history/{prompt_id}")
                if data.status_code == 200:
                    his_data = json.loads(data.text)
                    logging.info(f"返回的json为: {his_data}")
                else:
                    logging.error(f"获取output失败: {data.status_code}")
                output = his_data.get(prompt_id, {}).get("outputs", {}).get("9", {})
                filenames_lst = [image['filename'] for image in output['images']]
                return filenames_lst
            else:
                continue
   ws.close()
# 获取图片链接
def get_image_urls(filenames_lst):
   image_urls = [f"http://{host}:{port}/view?filename={filename}&type=output" for filename in filenames_lst]
   return image_urls

# def main():
#     positive_prompt = "一个漂亮的女孩,长腿,黑色丝袜,全身图,清晰,4k,成熟,简单背景,腿部均匀"
#     negative_prompt = "多人,多腿,多脚,丑陋,多手指，畸形,半身"
#     width = 1920
#     height = 1080
#     batch_size = 2
#     bodydata = task_body(positive_prompt,negative_prompt,width,height,batch_size)
#     prompt_id = task_prompt(bodydata)
#     filname = task_data(prompt_id)
#     img_lst = get_image_urls(filname)
#     print(f"图片链接为: {img_lst}")

@app.route('/txt2img', methods=['POST'])
def txt2img():
    data = request.json
    positive_prompt = data.get('positive_prompt', '')
    negative_prompt = data.get('negative_prompt', '')
    width = data.get('width', 512)
    height = data.get('height', 512)
    batch_size = data.get('batch_size', 2)
    bodydata = task_body(positive_prompt, negative_prompt, width, height, batch_size)
    prompt_id = task_prompt(bodydata)
    filname = task_data(prompt_id)
    img_lst = get_image_urls(filname)

    return img_lst
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5001,debug=True)