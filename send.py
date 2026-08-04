import requests
import base64
import hashlib
import os
from datetime import datetime

# 从 GitHub Secrets 读取 webhook 地址
webhook_url = os.environ['WECHAT_WEBHOOK_URL']

# 要发送的图片链接
image_url = "https://picsum.photos/400/300"

# 下载图片
print("1/3 正在下载图片...")
image_data = requests.get(image_url, timeout=30).content
print(f"   图片大小: {len(image_data)} 字节")

# 转成企业微信要求的格式
print("2/3 正在处理图片...")
base64_str = base64.b64encode(image_data).decode('utf-8')
md5_hash = hashlib.md5(image_data).hexdigest()

# 先发一条文字消息
requests.post(webhook_url, json={
    "msgtype": "text",
    "text": {
        "content": f"🤖 自动推送测试\n时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    }
})

# 发送图片
print("3/3 正在发送图片...")
response = requests.post(
    webhook_url,
    json={
        "msgtype": "image",
        "image": {
            "base64": base64_str,
            "md5": md5_hash
        }
    }
)

# 显示结果
result = response.json()
if result['errcode'] == 0:
    print("✅ 发送成功！打开企业微信看看吧")
else:
    print(f"❌ 发送失败：{result['errmsg']}")
