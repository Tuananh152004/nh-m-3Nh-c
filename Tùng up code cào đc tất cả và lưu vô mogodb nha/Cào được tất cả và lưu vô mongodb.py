from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pymongo import MongoClient

# Đường dẫn tới geckodriver
gecko_path = r"C:\Users\HP\Downloads\geckodriver-v0.35.0-win64\geckodriver.exe"
service = Service(gecko_path)

# Kết nối tới MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["course_database"]
courses_collection = db["courses"]

# Hàm thu thập thông tin khóa học
def collect_course_info():
    driver = webdriver.Firefox(service=service)
    driver.get("https://titv.vn/")
    time.sleep(10)

    all_courses = {}

    for data_id in range(75, 82):
        li_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'span[data-id="{data_id}"]'))
        )
        li_name = li_element.text
        li_element.click()
        time.sleep(10)

        course_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.ms_lms_courses_card_item'))
        )

        for course in course_elements:
            try:
                course_name = WebDriverWait(course, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                        'div.ms_lms_courses_card_item_wrapper > div:nth-child(2) > a:nth-child(1) > h3'))
                ).text

                price_element = WebDriverWait(course, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                        'div.ms_lms_courses_card_item_info_price > div.ms_lms_courses_card_item_info_price_single > span'))
                ).text

                rating_element = WebDriverWait(course, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                        'div.ms_lms_courses_card_item_info_rating_quantity > span'))
                ).text

                members_count = WebDriverWait(course, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                        'div.ms_lms_courses_card_item_meta_block > i.stmlms-members + span'))
                ).text

                views_count = WebDriverWait(course, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                        'div.ms_lms_courses_card_item_meta_block > i.stmlms-views + span'))
                ).text

                # Chuyển đổi các trường sang dạng số
                rating_numeric = float(rating_element) if rating_element else 0.0
                price_numeric = float(price_element.replace(',', '').replace('đ', '').strip()) if price_element and price_element.lower() != "free" else 0.0
                members_count_numeric = int(members_count.replace(',', '').strip()) if members_count else 0
                views_count_numeric = int(views_count.replace(',', '').strip()) if views_count else 0

                course_info = {
                    "name": course_name,
                    "price": price_numeric,
                    "rating": rating_numeric,
                    "members_count": members_count_numeric,
                    "views_count": views_count_numeric,
                    "category": li_name,
                    "reviews": []
                }
                all_courses[course_name] = course_info

            except Exception as e:
                print(f"Error collecting course info: {e}")
                continue

        driver.back()
        time.sleep(10)

    driver.quit()

    for course_name, course_info in all_courses.items():
        try:
            courses_collection.update_one(
                {"name": course_name},
                {"$set": course_info},
                upsert=True
            )
        except Exception as e:
            print(f"Error saving course {course_name}: {e}")

    return all_courses

# Hàm thu thập bình luận từ tất cả các môn học
def collect_reviews_from_all(courses):
    driver = webdriver.Firefox(service=service)
    driver.get("https://titv.vn/")
    time.sleep(10)

    button_all = driver.find_element(By.CSS_SELECTOR, 'span[data-id="all"]')
    button_all.click()
    time.sleep(10)

    # Hàm cuộn xuống để tải thêm môn học
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

            # Cập nhật bình luận vào MongoDB
            courses_collection.update_one(
                {"name": course_name},
                {"$set": {"reviews": review_list}}
            )

            driver.back()
            time.sleep(10)

            scroll_down()
            course_elements = driver.find_elements(By.CSS_SELECTOR, 'div.ms_lms_courses_card_item_wrapper')

        except Exception as e:
            continue

    driver.quit()  # Đóng trình duyệt sau khi hoàn thành

# Chạy đoạn 1 để thu thập thông tin khóa học
courses_data = collect_course_info()

# Chạy đoạn 2 để thu thập bình luận và cập nhật vào khóa học
collect_reviews_from_all(courses_data)















