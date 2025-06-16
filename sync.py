import requests
import re
from datetime import datetime

SOURCE_URL = "https://chinaiptv.pages.dev/Unicast/jiangsu/mobile.txt"
OUTPUT_FILE = "jiangsu_iptv.m3u"

def convert_to_m3u(source_text):
    """将原始文本转换为M3U格式"""
    lines = source_text.split('\n')
    current_group = ""
    output = ["#EXTM3U"]
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 检测分组行 (e.g., "央视,#genre#")
        if re.search(r",#genre#$", line):
            current_group = line.split(",")[0]
            continue
            
        # 处理频道行
        if "，" in line:  # 使用中文逗号分割
            parts = line.split("，", 1)
        else:  # 备用英文逗号
            parts = line.split(",", 1)
            
        if len(parts) == 2:
            channel_name, url = parts
            output.append(f'#EXTINF:-1 group-title="{current_group}",{channel_name}')
            output.append(url)
    
    return "\n".join(output)

def main():
    # 获取原始数据
    response = requests.get(SOURCE_URL)
    response.encoding = 'utf-8'
    
    if response.status_code != 200:
        print(f"Error fetching source: HTTP {response.status_code}")
        return
    
    # 转换格式
    m3u_content = convert_to_m3u(response.text)
    
    # 添加文件头注释
    last_updated = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    header = f"# Last Updated: {last_updated}\n# Source: {SOURCE_URL}\n\n"
    
    # 保存文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(header + m3u_content)
    print(f"Successfully updated {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
