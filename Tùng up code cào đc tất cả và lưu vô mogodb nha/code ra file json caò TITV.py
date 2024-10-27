from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from pymongo import MongoClient

# Đường dẫn tới geckodriver
gecko_path = r"C:\Users\HP\Downloads\geckodriver-v0.35.0-win64\geckodriver.exe"
service = Service(gecko_path)

# Kết nối tới MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["course_database"]  # Tạo hoặc kết nối đến database
courses_collection = db["courses"]  # Tạo hoặc kết nối đến collection cho các môn học
reviews_collection = db["reviews"]  # Tạo hoặc kết nối đến collection cho bình luận

# Hàm để thu thập thông tin môn học
def collect_course_info():
    driver = webdriver.Firefox(service=service)
    driver.get("https://titv.vn/")
    time.sleep(10)  # Tăng thời gian chờ tải trang

    all_courses = {}

    for data_id in range(75, 82):
        li_element = driver.find_element(By.CSS_SELECTOR, f'span[data-id="{data_id}"]')
        li_name = li_element.text
        driver.execute_script("arguments[0].scrollIntoView();", li_element)
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable(li_element))
        li_element.click()
        time.sleep(10)

        all_courses[li_name] = []

        course_elements = driver.find_elements(By.CSS_SELECTOR, 'div.ms_lms_courses_card_item')

        for course in course_elements:
            try:
                course_name = course.find_element(By.CSS_SELECTOR, 'div.ms_lms_courses_card_item_wrapper > div:nth-child(2) > a:nth-child(1) > h3').text
                price_element = course.find_element(By.CSS_SELECTOR, 'div.ms_lms_courses_card_item_info_price > div.ms_lms_courses_card_item_info_price_single > span').text
                rating_element = course.find_element(By.CSS_SELECTOR, 'div.ms_lms_courses_card_item_info_rating_quantity > span').text
                members_count = course.find_element(By.CSS_SELECTOR, 'div.ms_lms_courses_card_item_meta_block > i.stmlms-members + span').text
                views_count = course.find_element(By.CSS_SELECTOR, 'div.ms_lms_courses_card_item_meta_block > i.stmlms-views + span').text

                course_info = {
                    "name": course_name,
                    "price": price_element,
                    "rating": rating_element,
                    "members_count": members_count,
                    "views_count": views_count,
                    "category": li_name
                }
                all_courses[li_name].append(course_info)

                # Lưu vào MongoDB
                courses_collection.insert_one(course_info)

            except Exception as e:
                continue

        driver.back()
        time.sleep(10)

    driver.quit()

# Hàm thu thập bình luận từ tất cả các môn học
def collect_reviews_from_all():
    driver = webdriver.Firefox(service=service)
    driver.get("https://titv.vn/")
    time.sleep(10)

    button_all = driver.find_element(By.CSS_SELECTOR, 'span[data-id="all"]')
    button_all.click()
    time.sleep(10)

    def scroll_down():
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    scroll_down()

    course_elements = driver.find_elements(By.CSS_SELECTOR, 'div.ms_lms_courses_card_item_wrapper')
    if not course_elements:
        print("Không còn môn học nào trong thẻ All để thu thập.")
        return

    for i in range(len(course_elements)):
        try:
            course_link = course_elements[i].find_element(By.CSS_SELECTOR, 'a')
            course_link.click()
            time.sleep(10)

            course_name_element = driver.find_element(By.CSS_SELECTOR, 'h1')
            course_name = course_name_element.text

            reviews = driver.find_elements(By.CSS_SELECTOR, '.masterstudy-single-course-reviews__item-content p')
            review_list = [review.text for review in reviews] if reviews else []

            # Lưu vào MongoDB
            reviews_collection.insert_one({"course_name": course_name, "reviews": review_list})

            driver.back()
            time.sleep(10)

            scroll_down()
            course_elements = driver.find_elements(By.CSS_SELECTOR, 'div.ms_lms_courses_card_item_wrapper')

        except Exception as e:
            continue

    driver.quit()

# Chạy đoạn 1
collect_course_info()

# Chạy đoạn 2
collect_reviews_from_all()










