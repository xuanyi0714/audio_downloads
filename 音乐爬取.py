import sys
import requests
from pathlib import Path
from playwright.sync_api import sync_playwright
from lxml import etree
import jsonpath
import json
import time
print("程序启动中🚀🚀🚀")
time.sleep(1.5)
print("欢迎使用音频下载工具，请勿用于商业用途，请勿用于非法用途，请勿用于非法用途……(此处省略重复一万次)😱🙏🙏🙏")
print("本程序为个人学习小项目，不可用于商业😡")
time.sleep(1.5)
print("本程序需要在联网的情况下使用，请确保当前网络环境优良🔍（不优良也不要紧，不过有点卡罢了😁😁）")
time.sleep(1.5)
print("搜索结果均来自哔哩哔哩，感谢哔哩哔哩平台🙏🙏🙏🙏")
time.sleep(0.5)
print("🔴🔴🔴再次强调，本程序为免费产品，禁止用于商业盈利，禁止用于非法用途！！！🔴🔴🔴")
time.sleep(1.5)
print("使用时会弹出要输入的内容，记得留意如果在使用过程中出现一堆看不懂的英文报错不用理会，只需检查自己输入的内容是否正确即可")


def get_app_dir() -> Path:
    # 返回当前文件所在的目录
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent


APP_DIR = get_app_dir()
BROWSER_EXE = APP_DIR / "ms-playwright" / "chromium-1208" / "chrome-win" / "chrome.exe"
USER_DATA_DIR = APP_DIR / "ms-playwright" / "aa"
RESULTS_DIR = APP_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)
header = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0',
          "Referer": 'https://www.bilibili.com/'}
with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        headless=True,
        user_data_dir=str(USER_DATA_DIR),
        executable_path=str(BROWSER_EXE),
    )
    page = browser.pages[0]
    page.goto('https://www.bilibili.com/')
    page.wait_for_timeout(2000)
    key_word = input("请输入要下载的音频（输入完成后请按回车）：")
    if key_word:
        print('正在快马加鞭搜索您需要的音频🔍...', end='')
        print('...', end='')
        print('...', end='')
        page.fill('//input[@class="nav-search-input"]', key_word)
        page.click('//div[@class="nav-search-btn"]')
        page.wait_for_timeout(5000)
        page1 = browser.pages[1]
        locators = page1.locator('//a[@data-mod="search-card"]')
        locators_list = locators.all()
        print("已成功搜索到您想要的音频😆😆😆，当前搜索到n个结果🌸🌸🌸")
        print("现在请选择您要下载第几个结果的音频（默认下载第一个），备注：正常情况下保持默认就好，只有当下载的音频不符合预期时再考虑更换")
        str_ = input("请在这里输入整数，例如：1（输入完成后请按回车），现在开始输入吧：")
        try:
            num = int(str_)
        except Exception as e:
            print("错误的输入（需要输入正整数）😭😭😭，默认下载第一个结果🥲")
            locators_list[0].click()
        else:
            if num > len(locators_list):
                print("抱歉，我没搜到这么多内容😭😭😭，默认下载第一个结果🥲")
                locators_list[0].click()
            elif num <= 0:
                print('为什么不输入正整数😭，那我只能默认下载第一个结果了😢')
                locators_list[0].click()
            else:
                print(f"好的，正在下载第{num}个结果😆😆😆")
                locators_list[num-1].click()
        page1.wait_for_timeout(2000)
        page2 = browser.pages[2]
        url = page2.url
        response = requests.get(url, headers=header)
        data = response.content.decode('utf-8')
        html_obj = etree.HTML(data)
        response_data = html_obj.xpath('//script[contains(text(), "window.__playinfo__")]/text()')[0]
        json_data = response_data.split('__=')[1]
        py_data = json.loads(json_data)
        audio_url = jsonpath.jsonpath(py_data, "$..audio[?(@.id==30216)].baseUrl")[0]
        page2.wait_for_timeout(1000)
        response2 = requests.get(audio_url, headers=header)
        audio_path = RESULTS_DIR / f"{key_word}.wav"
        with open(audio_path, 'wb') as f:
            f.write(response2.content)
        print('下载成功！😆')
        print("祝您生活愉快~🌸🌸🌸")
        print("下次再见吧~😆😆😆🌹")
        input("回车结束")
    else:
        print("你竟然什么都不输入！太让我伤心了~💔💔💔😭😭😭")
        time.sleep(2)
        input("回车结束")




























