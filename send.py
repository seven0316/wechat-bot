import requests
import base64
import hashlib
import os
import random
import sys

webhook_url = os.environ['WECHAT_WEBHOOK_URL']

# 随机选图
images_dir = "images"

# 1. 检查目录是否存在
if not os.path.exists(images_dir):
    print(f"❌ 目录 '{images_dir}' 不存在！")
    print(f"当前目录内容: {os.listdir('.')}")
    sys.exit(1)

# 2. 检查目录是否为空
dir_contents = os.listdir(images_dir)
print(f"📂 images 目录内容: {dir_contents}")

# 3. 过滤图片文件
all_images = [f for f in dir_contents if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]

if not all_images:
    print(f"❌ 在 '{images_dir}' 中没有找到图片文件！")
    print(f"支持格式: .jpg, .jpeg, .png, .gif")
    sys.exit(1)

# 4. 随机选一张
chosen = random.choice(all_images)
image_path = os.path.join(images_dir, chosen)
print(f"🖼️ 选中图片: {chosen}")

# 处理图片
with open(image_path, 'rb') as f:
    image_data = f.read()

base64_str = base64.b64encode(image_data).decode('utf-8')
md5_hash = hashlib.md5(image_data).hexdigest()

# 发图片
print(f"📤 发送图片: {chosen} (大小: {len(image_data)} 字节)")
resp1 = requests.post(webhook_url, json={
    "msgtype": "image",
    "image": {"base64": base64_str, "md5": md5_hash}
})
print(f"图片发送响应: {resp1.status_code}")

# 发文字
resp2 = requests.post(webhook_url, json={
    "msgtype": "text",
    "text": {"content": "日报日报~随机福利"}
})
print(f"文字发送响应: {resp2.status_code}")

print("✅ 发送完成！")
