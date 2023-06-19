import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import threading
import time
import datetime
import socket
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import requests
import tldextract
import re
import dns.resolver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
import csv
import os
import random
import json
import tkinter as tk
from tkinter import filedialog
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

LARGE_FONT = ("Verdana", 12)
BIG_FONT = ("Verdana", 15)


class MyGoogleBot(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "My Google Bot")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = StartPage(container, self)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # 输入框和搜索按钮布局
        input_frame = tk.Frame(self)
        input_frame.pack(side="top", fill="x", padx=10, pady=10)

        label = tk.Label(input_frame, text="1. 输入搜索内容：", font=LARGE_FONT)
        label.pack(side="left", padx=(0, 10))

        self.search_text_entry = tk.Entry(input_frame, font=BIG_FONT, width=30)
        self.search_text_entry.pack(side="left")

        new_search_button = tk.Button(input_frame, text="搜索", width=8, height=1,
                                      command=lambda: self.new_search(controller), font=("Verdana", 10))
        new_search_button.pack(side="left", padx=(10, 0), ipady=2)

        # 继续搜索和选择文件按钮布局
        continue_frame = tk.Frame(self)
        continue_frame.pack(side="top", fill="x", padx=10, pady=(0, 10))

        continue_label = tk.Label(continue_frame, text="2. 继续未完成的搜索：", font=LARGE_FONT)
        continue_label.pack(side="left", padx=(0, 10))

        choose_file_button = tk.Button(continue_frame, text="选择文件", width=8, height=1,
                                       command=lambda: self.choose_file(), font=("Verdana", 10))
        choose_file_button.pack(side="left", ipady=2)

        # 输出对话框布局
        self.output_text = tk.Text(self, font=LARGE_FONT, state="normal")
        self.output_text.pack(fill="both", expand=True, padx=10, pady=10)
    def new_search(self, controller, task=None):
        global filename, writer
        while True:
            # 获取要搜索的关键词
            search_text = self.search_text_entry.get()
            if search_text.strip() == '':
                print('没有输入搜索内容，请重新输入！')
                self.output_text.insert("end", "没有输入搜索内容，请重新输入！\n")
                quit()
            if not search_text.endswith('contact'):
                search_text += ''
            # 检查结果文件是否已存在
            filename = f'dic_{search_text}.csv'
            if os.path.isfile(filename):
                print(f'结果文件 {filename} 已存在，请重新选择操作！')
                self.output_text.insert("end", f"结果文件 {filename} 已存在，请重新选择操作！\n")
                continue
            # 新建结果文件并写入表头
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['href', 'domain', 'e-mail', 'country', 'lang', 'facebook', 'twitter', 'telegram'])
            print(f'已创建结果文件 {filename}')
            self.output_text.insert("end", f"已创建结果文件 {filename}\n")
            break
        start_options()
        browser.get('https://www.google.com/search?q=' + search_text + ' contact')
        time.sleep(4)
        main_process(self)
        ###########################
        t = threading.Thread(target=task)
        t.daemon = True
        t.start()

    def choose_file(self):
        global browser, filepath, current_url
        root = tk.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename(defaultextension='.csv', filetypes=[('CSV Files', '*.csv')])
        if not filepath:
            print('未选择文件，程序退出！')
            self.output_text.insert("end", "未选择文件，程序退出！\n")
            exit()

        # 尝试多种编码格式来读取文件
        encodings = ['utf-8', 'ISO-8859-1', 'GBK', 'Big5']
        for encoding in encodings:
            try:
                with open(filepath, mode='r', encoding=encoding, newline='') as f:
                    reader = csv.reader(f)
                    results = list(reader)
                if len(results) == 0:
                    print('结果文件中没有数据，请重新选择！')
                    self.output_text.insert("end", "结果文件中没有数据，请重新选择！\n")
                    exit()
                current_url = results[0][9]
                if not current_url:
                    print('结果文件第一行第十列为空，请重新选择！')
                    self.output_text.insert("end", "结果文件第一行第十列为空，请重新选择！\n")
                    exit()

                # 调用 main_process() 函数处理任务
                start_options()
                browser.get(current_url)
                time.sleep(2)
                main_process(filepath, current_url)

                return (filepath, current_url)
            except UnicodeDecodeError:
                pass

        print(f'无法读取文件{filename}，请检查文件路径和编码格式。')
        self.output_text.insert("end", f"无法读取文件{filename}，请检查文件路径和编码格式。\n")
        exit()

        t = threading.Thread(target=task)
        t.daemon = True
        t.start()

def process_task(href):
    global current_url
    global ext
    global subdomain
    global domain
    page_source = get_page_source(browser, href)
    domain = extract_domain(browser)
    email_str = extract_emails(page_source)
    country_code = get_country_code(browser)
    lang = get_page_language(browser)
    # 提取社交链接
    links_tuple = extract_social_links(page_source)
    facebook_links = links_tuple[0]
    twitter_links = links_tuple[1]
    telegram_links = links_tuple[2]
    print(f"{domain}, {email_str}, {country_code}, {lang}, {facebook_links}, {twitter_links}, {telegram_links}")
    # self.output_text.insert("end", f"{domain}, {email_str}, {country_code}, {lang}, {facebook_links}, {twitter_links}, {telegram_links}\n")

    # 直接将新的一行写入结果文件中
    row = [href, domain, email_str, country_code, lang, facebook_links, twitter_links, telegram_links]
    writer.writerow(row)
    existing_domains.append(domain)
    # 将新域名写入表中
    with open('domain.json', 'w') as f2:
        json.dump(existing_domains, f2)
    browser.close()

    # 切换回第一个标签页
    browser.switch_to.window(browser.window_handles[0])

def get_page_source(browser, href):
    """
    使用 Selenium 打开链接并获取页面源代码。

    Args:
        browser: Selenium WebDriver 浏览器实例。
        href (str): 要打开的链接地址。

    Returns:
        str: 页面的 HTML 源代码。
    """
    # 记录页面源代码
    page_source = ""

    try:
        browser.set_page_load_timeout(40)
        browser.execute_script(f"window.open('{href}', '_blank');")
    except TimeoutException:
        print("Load page timed out.")
        # self.output_text.insert("end", "Load page timed out.\n")
        browser.execute_script("window.stop();")

    # 等待页面加载完成
    time.sleep(4)
    # 获取当前所有窗口的句柄
    window_handles = browser.window_handles
    # 切换到新打开的标签页
    new_window_handles = browser.window_handles
    browser.switch_to.window(new_window_handles[-1])

    try:
        wait = WebDriverWait(browser, 10)  # 等待时间设置为 10 秒
        table = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "table")))  # 等待表格元素出现
    except TimeoutException:
        time.sleep(5)
        browser.execute_script("window.stop();")
        pass
    # 获取页面的源代码
    try:
        browser.set_page_load_timeout(40)
        page_source = browser.page_source
    except TimeoutException:
        print("Get page source timed out.")
        browser.execute_script("window.stop();")
        page_source = browser.page_source

    return page_source

def extract_domain(browser):
    """
    从当前页面 URL 中提取出域名。

    Args:
        browser: Selenium WebDriver 浏览器实例。

    Returns:
        str: 域名字符串，格式为“二级域名.顶级域名”。
    """

    current_url = browser.current_url
    ext = tldextract.extract(current_url)
    domain = f"{ext.domain}.{ext.suffix}"
    return domain

def extract_emails(page_source):
    soup = BeautifulSoup(page_source, 'lxml')
    email_set = set()
    # 通过正则表达式提取所有的邮箱地址
    for string in soup.find_all(string=True):
        match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", string)
        if match:
            email_set.add(match.group(0))

    email_list = list(email_set)
    email_str = ';'.join(email_list)

    return email_str

def get_country_code(browser):
    """
    获取当前页面所属的国家或地区信息。

    Args:
        browser: Selenium WebDriver 浏览器实例。

    Returns:
        str: 当前页面所属的国家或地区代号。如果查询失败，则返回空字符串。
    """

    country_code = ""

    try:
        domain = extract_domain(browser)
        # 尝试获取页面 IP 地址
        socket.setdefaulttimeout(10)
        url = domain if domain.startswith('www.') else 'www.' + domain
        ip = socket.gethostbyname(url)

        # 查询 IP 地址所属的国家或地区
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            country_code = data.get('countryCode', '')
    except Exception as e:
        print(f"Error occurred when getting country code: {e}")
        pass

    return country_code

def get_page_language(browser):
    """
    获取当前页面的主语言。

    Args:
        browser: Selenium WebDriver 浏览器实例。

    Returns:
        str: 当前页面的主语言。
    """

    lang = None
    try:
        lang = browser.execute_script("return document.querySelector('html').getAttribute('lang')")
    except Exception as e:
        print(f"Error occurred when getting page language: {e}")
        pass

    return lang

def extract_social_links(page_source):
    """
    从网页源代码中提取出所有的 Facebook 和 Twitter 链接。

    Args:
        page_source: 网页的源代码。

    Returns:
        tuple: 一个元组，包含两个列表，分别表示找到的 Facebook 和 Twitter 链接。
    """

    # 匹配 Facebook 和 Twitter 链接
    soup = BeautifulSoup(page_source, 'lxml')
    facebook_links = set()
    twitter_links = set()
    telegram_links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        if 'facebook.com' in href:
            facebook_links.add(href)
        elif 'twitter.com' in href:
            twitter_links.add(href)
        elif 't.me' in href or 'telegram.me' in href:
            telegram_links.add(href)

    return list(facebook_links), list(twitter_links), list(telegram_links)

def start_options():
    global browser, now, default_domains
    # 创建 WebDriver 实例
    # driver = webdriver.Chrome()
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.page_load_strategy = "none"  # 设置 PageLoadStrategy

    # 指定 Chrome WebDriver 文件路径
    driver_path = r'C:\Users\jason\PycharmProjects\pythonProject\Orders\dist\chromedriver.exe'

    # 创建浏览器对象，这里使用Chrome浏览器
    service = Service(driver_path)
    browser = webdriver.Chrome(service=service)
    # 创建chrome driver实例
    # driver = webdriver.Chrome(service=service, options=options)
    # 获取当前日期时间并格式化为字符串
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    # 设置默认的域名列表
    default_domains = ['google.com']
def main_process(filepath, current_url):
    global existing_domains
    # 初始序列号为 0
    seq_no = 0
    count = 1

    limit = 3
    page_count = 0

    browser.implicitly_wait(1)  # 隐式等待 2 秒
    # 循环搜索所有结果
    while True:
        # 查找所有搜索结果的标题元素列表，并逐个输出结果
        divs = browser.find_elements(By.XPATH, '//div[@class="yuRUbf"]')
        # 遍历每个 div 元素，并输出其后面的链接地址
        links = []
        for div in divs:
            link1 = div.find_element(By.TAG_NAME, 'a')
            links.append(link1)
        # 先列出所有搜索结果
        results2 = []
        for i, link in enumerate(links):
            href = link.get_attribute("href")
            # 打印序号和链接
            print(f"{i + 1}. {href}")
            results2.append((i + 1, href, '', '', '', ''))

        # 检查 domain.json 文件是否存在，如果不存在则创建一个包含默认域名列表的文件
        if not os.path.exists('domain.json'):
            with open('domain.json', 'w') as f:
                json.dump(default_domains, f)

        # 读取已有域名列表
        with open('domain.json', 'r') as f:
            existing_domains = json.load(f)

        # 遍历搜索结果并写入结果文件（追加模式）
        with open(filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # 初始化 hlinks 列表
            hlinks = []
            # 切换回主标签页
            browser.switch_to.window(browser.window_handles[0])
            for i, link in enumerate(links):
                # time.sleep(1)
                href = link.get_attribute('href')
                # 获取二级域名和顶级域名
                ext = tldextract.extract(href)
                subdomain = ext.subdomain
                domain = f'{ext.domain}.{ext.suffix}'

                # 如果域名已存在，则跳过
                if domain in existing_domains:
                    continue

                # 将新的域名添加到域名列表中
                # existing_domains.append(domain)

                hlinks.append([href])
            # 转换为任务列表
            tasks = [{"href": link[0]} for link in hlinks]
            # 处理任务列表中的每个任务
            results = [process_task(task["href"]) for task in tasks]

        # 将当前页面的完整链接写入结果文件的第一行第十列
        browser.switch_to.window(browser.window_handles[0])
        time.sleep(1)
        current_url = browser.current_url

        encodings = ['utf-8', 'ISO-8859-1', 'GBK', 'Big5']
        for encoding in encodings:
            try:
                with open(filename, mode='r', encoding=encoding) as file:
                    reader = csv.reader(file)
                    results = list(reader)
                print(f'Read {filename} successfully with {encoding} encoding.')
                break  # 如果成功读取文件，则直接退出循环。
            except UnicodeDecodeError:
                print(f'Failed to read {filename} with {encoding} encoding.')

        if not results:
            print(f'Failed to read {filename} using all tried encodings.')
        # 检查results列表是否为空
        if not results:
            results.append([''] * 10)  # 如果为空则添加一行空白数据

        # 检查第一行是否包含足够的列数
        if len(results[0]) < 10:
            results[0].extend([''] * (10 - len(results[0])))  # 如果列数不足则添加空白单元格

        # 检查当前链接是否以 "http://" 或 "https://" 开头
        if not current_url.startswith('http://') and not current_url.startswith('https://'):
            print('加载失败，请重新开始！')
            exit()
        # 在第一行第十列位置添加当前链接
        results[0][9] = current_url
        # 使用csv模块保存修改后的数据
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(results)

        page_count += 1
        if page_count >= limit:  # 达到翻页次数限制，跳出循环
            print('演示结束')
            break
        # 找到"下一页"按钮并获取其链接
        try:
            browser.switch_to.window(browser.window_handles[0])
            time.sleep(1)
            next_page_link = browser.find_element(By.XPATH, '//a[@id="pnnext"]')
            next_page_href = next_page_link.get_attribute("href")
            # 跳转到下一页
            browser.get(next_page_href)
            time.sleep(3)
        except NoSuchElementException:
            try:
                # 如果找不到下一页链接，则查找"重新搜索以显示省略的结果"链接并点击
                browser.switch_to.window(browser.window_handles[0])
                time.sleep(1)
                retry_link_xpath = '//a[contains(@href,"search?q") and contains(@href,"filter=0") and contains(text(),"重新搜索以显示省略的结果")]'
                retry_link = browser.find_element(By.XPATH, retry_link_xpath)
                retry_link.click()
                time.sleep(3)
            except NoSuchElementException:
                break

    print(f'结果已保存到 {filename} 文件中')


if __name__ == "__main__":
    app = MyGoogleBot()
    app.geometry("800x600")
    app.mainloop()

