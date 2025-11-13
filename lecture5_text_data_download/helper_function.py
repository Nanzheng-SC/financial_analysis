from bs4 import BeautifulSoup
import requests
import time
import random
import re
import json

def download_page(url, max_retries=3):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                response.encoding = response.apparent_encoding
                return response.text
            else:
                print(f"请求失败，状态码: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"请求异常 (尝试 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(random.uniform(2, 5))  # 等待时间稍长一些
                continue
        return ""

        
def parse_eastmoney_guba(html_content):
    # 使用正则表达式提取 article_list 变量中的JSON数据
    pattern = r'var article_list=(\{.*?\});'
    match = re.search(pattern, html_content, re.DOTALL)
    
    if match:
        json_str = match.group(1)
        try:
            # 移除可能的前导空格或换行符
            json_str = json_str.strip()
            # 使用json.loads解析JSON字符串，转换为Python字典
            data = json.loads(json_str)
            return data
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            return None
    else:
        print("未找到article_list数据")
        return None


def parse_swufe_news_list(html: str):
    """
    从西南财经大学新闻列表 HTML 中解析新闻数据
    
    参数:
        html (str): HTML 文本字符串
    
    返回:
        list[dict]: 新闻信息列表，每条包含 title, link, text, date
    """
    soup = BeautifulSoup(html, "html.parser")
    news_items = []
    # 在爬虫开发中，我们通常优先使用那些 语义化、具有唯一性 的class作为选择器，
    # 而忽略那些通用的、功能性的class（如clearfix）
    # 定位新闻 li
    ul = soup.find_all("ul",{"class":"whitenewslist"})
    for li in ul[0].find_all("li"):
        a_tag = li.find("a")
        date_tag = li.find("i",{"class":"thunews-clock-o"})

        if a_tag:
            news_items.append({
                "title": a_tag.get("title", "").strip(),
                "link": a_tag.get("href", "").strip(),
                "text": a_tag.get_text(strip=True),
                "date": date_tag.get_text(strip=True) if date_tag else ""
            })
    
    return news_items



# def parse_swufe_news_list(html: str):
#     """
#     从西南财经大学新闻列表 HTML 中解析新闻数据
    
#     参数:
#         html (str): HTML 文本字符串
    
#     返回:
#         list[dict]: 新闻信息列表，每条包含 title, link, text, date
#     """
#     soup = BeautifulSoup(html, "html.parser")
#     news_items = []
#     # 定位新闻 li
#     for li in soup.select("ul.whitenewslist li"):
#         a_tag = li.find("a")
#         date_tag = li.select_one("span.time i.thunews-clock-o")

#         if a_tag:
#             news_items.append({
#                 "title": a_tag.get("title", "").strip(),
#                 "link": a_tag.get("href", "").strip(),
#                 "text": a_tag.get_text(strip=True),
#                 "date": date_tag.get_text(strip=True) if date_tag else ""
#             })
    
#     return news_items