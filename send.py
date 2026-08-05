import requests
import base64
import hashlib
import os
import random

webhook_url = os.environ['WECHAT_WEBHOOK_URL']

# 随机选图
images_dir = "images"
all_images = [f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
chosen = random.choice(all_images)
image_path = os.path.join(images_dir, chosen)

# 处理图片
with open(image_path, 'rb') as f:
    image_data = f.read()
base64_str = base64.b64encode(image_data).decode('utf-8')
md5_hash = hashlib.md5(image_data).hexdigest()

# 发图片
print(f"发送图片: {chosen}")
requests.post(webhook_url, json={
    "msgtype": "image",
    "image": {"base64": base64_str, "md5": md5_hash}
})

# 发文字
requests.post(webhook_url, json={
    "msgtype": "text",
    "text": {"content": "日报日报~随机福利"}
})

print("✅ 发送完成！")
