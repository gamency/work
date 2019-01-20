#!/usr/bin/env
# encoding: utf-8

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageDraw
import numpy as np
import math
import time
import random
import json

x=320
y=180
slide_x=42
slide_y=42

# 截图拿到图片位置，pox,poy是相对位移
def get_snap(driver, pox, poy):
    driver.save_screenshot('snap.png')
    page_snap_obj=Image.open('snap.png')
    res = page_snap_obj.crop((pox, poy, pox+x, poy+y))
    return res

# 灰度图
def convertToL(image):
	image = image.convert('L')
	image = ImageEnhance.Brightness(image).enhance(1.5) #提高亮度
	image = ImageEnhance.Contrast(image).enhance(2.0)
	image = ImageEnhance.Brightness(image).enhance(1.5) #提高亮度
	image = ImageEnhance.Contrast(image).enhance(1.0)
	image = ImageEnhance.Sharpness(image).enhance(1.0)
	# image.show()
	return image

# 牛逼的算法
def getOriginVector(width, height):
	v = np.zeros(width * height)
	for i in range(width * height):
		v[i] = 1
	return v/255

def transvector(image, start_x, start_y, width, height):
    w, h = image.size
    v = np.zeros(width * height)
    idx = 0
    for i in range(height):
        if start_y + i >= h:
            break
        for j in range(width):
            idx = i * width + j
            if start_x + j >= w:
                break
            a = image.getpixel((start_x + j, start_y + i))
            v[idx] = a
    return v/255

def vecsim(v1, v2):
    s1 = v1.dot(v1)
    s2 = v2.dot(v2)
    s = math.sqrt(s1 * s2)
    if s == 0:
        return 0
    # s1 = math.sqrt(s1)
    # s2 = math.sqrt(s2)
    if s1 > s2:
        return (v1.dot(v2) / s) * s2 / s1
    return (v1.dot(v2) / s) * s1 / s2

def vecsim1(v1, v2):
    v = v2-v1
    return -1*v.dot(v)

# fix_y是y轴高度
def calsim(image, width, height, fix_y ):
    maxsim = -100000
    x, y = (0,0)
    w, h = image.size
    v = getOriginVector(width, height)
    # image_c = image.crop((1, fix_y, 1+width, fix_y + height))
    # image_c.show()
    # v = getOriginVector(image_c, width, height) # 计算彩色图片的时候用
    for i in range(h - height):
        # 因为y是固定的，所以不用遍历，只允许一遍即可
        if i > 0:
            break
        for j in range(w - width):
            vm = transvector(image, j, fix_y, width, height)
            sv = vecsim1(vm, v)
            if sv > maxsim:
                maxsim = sv
                x = j
                y = fix_y
    print(maxsim)
    dr = ImageDraw.Draw(image)
    dr.rectangle((x, y, x + width, y + height), outline = "white")
    del dr
    image.show()
    return x

# 模拟滑动
def getCaptchaAndDrag(browser, target):
	time.sleep(2) # 等待2s等图片切换
	# 找到滑块位置，获取高度
	slide = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/img')
	size = slide.size
	pos = slide.get_attribute('style')
	print(slide.get_attribute('src').replace('https://statictest.fraudmetrix.cn/sphinx/slide/',''))
	pos = int(pos.replace(' transform: translate(0px, 0px);','').replace('top: ','').replace('px;', '').replace(' opacity: 1;', ''))
	print("y轴高度为%d" % pos)
	# 获取滑块底图
	resImg = get_snap(browser, 440, 244)
	resImg = convertToL(resImg)
	distance = calsim(resImg, size.get('width'), size.get('height'), pos)
	# = random.randint(20, 200)
	print("滑动距离为%d" % distance)
	time.sleep(3)
	# 模拟滑动行为
	actions = ActionChains(browser)
	actions.click_and_hold(target)
	time.sleep(0.1)
	# actions.drag_and_drop_by_offset(target, distance, 0).perform() # 精确滑动
	dis = 0
	reveal = 0 # 滑过头了
	for x in range(200):
		s = random.randint(1, 5)
		dis = dis + s
		actions.move_by_offset(s, 1)
		time.sleep(0.1)
		if dis >= distance:
			# 如果滑过头了，就要回走
			if dis - distance > 0:
				reveal = distance - dis
				actions.move_by_offset(reveal, 1)
			print("目标距离%d, 实际%d, 回滑%d" % (distance, dis, reveal))
			break
	actions.release().perform()
	time.sleep(1) # 这里等待1s看结果
	text = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div')
	print(text.text)
	print("................................")
	return text.text

def refresh(browser):
	ActionChains(browser).move_by_offset(20, 20).click().perform();
	time.sleep(1)
	ActionChains(browser).move_by_offset(30, 30).click().perform();
	time.sleep(1)
	browser.find_element_by_xpath('//*[@id="loginBtn"]/button').click()
	time.sleep(1)

if __name__ == '__main__':
	url = "https://www.tongdun.cn/online/smartVerify"
	browser = webdriver.Chrome()
	browser.get(url)
	success = 0
	i = 0
	try:
		time.sleep(3)
		browser.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[3]/div/span[2]').click()
		time.sleep(2)
		browser.find_element_by_xpath('//*[@id="loginBtn"]/button').click()
		time.sleep(1)
		target = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[2]')
		time.sleep(2)
		while i < 50:
			print("第%d次" % i)
			resp = getCaptchaAndDrag(browser, target)
			while resp.startswith(u'验证失败'):
				i = i + 1
				resp = getCaptchaAndDrag(browser, target)
			if resp.startswith(u'验证通过'):
				success = success + 1
			# 点击一下空白区域，再去点击登录button
			i = i + 1
			try:
				refresh(browser)
			except Exception:
				refresh(browser)
	except Exception:
		raise
		browser.close()
	finally:
		time.sleep(5)
		print("验证完成成功%d次" % success)
		browser.close()

