from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import base64

def generate_image(path, output_file, height=1500, width=1500):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--force-device-scale-factor=1')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    # 加载本地HTML文件
    driver.get(path)
    
    # 等待内容加载
    time.sleep(2)
    
    # # 获取内容区域的实际尺寸
    if(height == 0 and width == 0):
        dimensions = driver.execute_script("""
            var content = document.querySelector('.content-wrapper') || document.body;
            var rect = content.getBoundingClientRect();
            return {
                width: Math.ceil(rect.width),
                height: Math.ceil(rect.height)
            };
        """)
        height = dimensions['height']
        width = dimensions['width']
        print("Content dimensions:", dimensions)
    
    # 设置视口大小为内容区域大小
    driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {
        'mobile': False,
        'width': width,
        'height': height,
        'deviceScaleFactor': 1,
    })
    
    # 获取完整页面截图
    screenshot = driver.execute_cdp_cmd('Page.captureScreenshot', {
        'format': 'png',
        'fromSurface': True,
        'captureBeyondViewport': True
    })
    
    # 保存截图
    with open(output_file, 'wb') as f:
        f.write(base64.b64decode(screenshot['data']))
    
    driver.quit()

if __name__ == '__main__':
    #generate_image('P01.html', 'P01.png', height=1500, width=1500)
    #localfile = 'file://' + os.path.abspath('main.html')
    localfile = 'https://www.deepseek.com/'
    generate_image(localfile, 'deepseek.png', height=0, width=0)
