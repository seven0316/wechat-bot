import requests
import base64
import hashlib
import os
from datetime import datetime, timedelta

# 从 GitHub Secrets 读取 webhook 地址
webhook_url = os.environ['WECHAT_WEBHOOK_URL']

# 要发送的图片链接
image_url = "https://picsum.photos/400/300"

# 获取北京时间
beijing_time = datetime.utcnow() + timedelta(hours=8)
date_str = beijing_time.strftime('%Y-%m-%d')

# 检查是否为工作日（使用免费 API）
try:
    # 使用中国节假日 API（免费）
    api_url = f"https://timor.tech/api/holiday/info/{date_str}"
    response = requests.get(api_url, timeout=5)
    data = response.json()
    
    if data.get('code') == 0:
        holiday_type = data['data']['type']
        # type: 0=工作日, 1=休息日, 2=节假日
        if holiday_type in [1, 2]:
            print(f"⏸️ 今天是{data['data'].get('name', '休息日')}，跳过发送")
            exit(0)
        else:
            print(f"ℹ️ 今天是工作日，正常发送")
    else:
        # API 调用失败，降级为检查周末
        print("⚠️ 节假日API调用失败，使用周末检查")
        if beijing_time.weekday() >= 5:
            print("⏸️ 今天是周末，跳过发送")
            exit(0)
except Exception as e:
    print(f"⚠️ 节假日检查异常：{e}，使用周末检查")
    if beijing_time.weekday() >= 5:
        print("⏸️ 今天是周末，跳过发送")
        exit(0)

# 下载图片
print("1/3 正在下载图片...")
image_data = requests.get(image_url, timeout=30).content
print(f"   图片大小: {len(image_data)} 字节")

# 转成企业微信要求的格式
print("2/3 正在处理图片...")
base64_str = base64.b64encode(image_data).decode('utf-8')
md5_hash = hashlib.md5(image_data).hexdigest()

# 获取时间字符串
time_str = beijing_time.strftime('%Y-%m-%d %H:%M:%S')
weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
weekday_name = weekday_names[beijing_time.weekday()]

# 先发一条文字消息
requests.post(webhook_url, json={
    "msgtype": "text",
    "text": {
        "content": f"🤖 自动推送测试\n时间：{time_str} (北京时间)\n{weekday_name} 工作日推送"
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
