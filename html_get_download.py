from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import threading

search_input = input("请输入要搜索的内容：").replace(" ", "+") # 将空格替换成+号

# 生成搜索链接
search_url = f"https://.../?story={search_input}&do=search&subaction=search"

edge_driver_path = "your_edge_driver_path" # 替换成您本地 Edge 驱动的路径
keyword = "https://.../" # 指定关键字

# 创建 EdgeDriver 对象
edge_service = EdgeService(executable_path=edge_driver_path)
driver = webdriver.Edge(service=edge_service)

# 打开浏览器并访问网页
def wait_and_get(search_url):
    driver.get(search_url)

t = threading.Thread(target=wait_and_get, args=(search_url,))
t.start()

# 模拟进度条
for i in range(1, 101):
    print("\rLoading... {}%".format(i), end="")
    time.sleep(0.2)
    if i == 50:
        time.sleep(0.3)
    if i == 99:
        t.join() # 等待 driver.get(url) 完成
    elif not t.is_alive():
        break

print("\n加载完成！")

# 等待页面完全加载
wait = WebDriverWait(driver, 10) # 等待时间为10秒
element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

# 查找包含指定关键字的链接并输出完整链接
link_elements = driver.find_elements(By.CSS_SELECTOR, f"a[href*='{search_input.replace('+','-')}']")
link_list = []

for link_element in link_elements:
    href = link_element.get_attribute("href")
    if href and keyword in href:
        processed_href = href.replace(keyword, '...')
        print(f"{len(link_list) + 1}. {processed_href}")
        link_list.append(href)

# 关闭浏览器 该语句保证浏览器一定会被关闭
try:
    driver.quit()
except:
    pass

if not link_list:
    print("未找到符合条件的链接！")
else:
    while True:
        choice = input("请输入链接序号以选择要打开的链接：\n")
        if not choice.isdigit() or int(choice) <= 0 or int(choice) > len(link_list):
            print("无效的选择，请重新输入！")
        else:
            break
    selected_link = link_list[int(choice) - 1]

    # 打开浏览器并访问选定的链接
    edge_service = EdgeService(executable_path=edge_driver_path)
    driver = webdriver.Edge(service=edge_service)

    def wait_and_open(selected_link):
        driver.get(selected_link)

    t = threading.Thread(target=wait_and_open, args=(selected_link,))
    t.start()

    # 模拟进度条
    for i in range(1, 101):
        print("\rLoading... {}%".format(i), end="")
        time.sleep(0.2)
        if i == 50:
            time.sleep(0.3)
        if i == 99:
            t.join() # 等待 driver.get(url) 完成
        elif not t.is_alive():
            break

    print("\n加载完成！")

    # 等待页面完全加载
    wait = WebDriverWait(driver, 10) # 等待时间为10秒
    element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # 查找包含指定关键字的链接并输出完整链接
    keyword = "https://vk.com/s/v1/doc/" # 指定关键字
    link_elements = driver.find_elements(By.TAG_NAME, "a")
    for link_element in link_elements:
        href = link_element.get_attribute("href")
        if href and keyword in href:
            print("\n包含关键字的链接：", href)

    # 关闭浏览器 该语句保证浏览器一定会被关闭
    try:
        driver.quit()
    except:
        pass

os.system("pause")
