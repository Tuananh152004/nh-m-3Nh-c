from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Đường dẫn tới geckodriver
gecko_path = r"C:\Users\HP\Downloads\geckodriver-v0.35.0-win64\geckodriver.exe"
service = Service(gecko_path)

# Hàm để thu thập thông tin môn học
def collect_course_info():
    driver = webdriver.Firefox(service=service)
    driver.get("https://titv.vn/")
    time.sleep(10)  # Tăng thời gian chờ tải trang

    all_courses = {}  # Tạo từ điển để chứa thông tin

    for data_id in range(75, 82):
        li_element = driver.find_element(By.CSS_SELECTOR, f'span[data-id="{data_id}"]')
        li_name = li_element.text  # Lấy tên thẻ li
        driver.execute_script("arguments[0].scrollIntoView();", li_element)
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable(li_element))
        li_element.click()
        time.sleep(10)  # Tăng thời gian chờ để đảm bảo nội dung tải xong

        # Khởi tạo danh sách cho các môn học thuộc thẻ li này
        all_courses[li_name] = []

        # Thu thập các môn học
        course_elements = driver.find_elements(By.CSS_SELECTOR, 'div.ms_lms_courses_card_item')

        for course in course_elements:
            try:
                course_name = course.find_element(By.CSS_SELECTOR, 'div.ms_lms_courses_card_item_wrapper > div:nth-child(2) > a:nth-child(1) > h3').text
                price_element = course.find_element(By.CSS_SELECTOR, 'div.ms_lms_courses_card_item_info_price > div.ms_lms_courses_card_item_info_price_single > span').text
                rating_element = course.find_element(By.CSS_SELECTOR, 'div.ms_lms_courses_card_item_info_rating_quantity > span').text
                members_count = course.find_element(By.CSS_SELECTOR, 'div.ms_lms_courses_card_item_meta_block > i.stmlms-members + span').text
                views_count = course.find_element(By.CSS_SELECTOR, 'div.ms_lms_courses_card_item_meta_block > i.stmlms-views + span').text

                # Thêm thông tin môn học vào danh sách
                course_info = {
                    "name": course_name,
                    "price": price_element,
                    "rating": rating_element,
                    "members_count": members_count,
                    "views_count": views_count
                }
                all_courses[li_name].append(course_info)

            except Exception as e:
                # Bỏ qua lỗi và không in ra
                continue

        driver.back()
        time.sleep(10)  # Tăng thời gian chờ trước khi quay lại

    driver.quit()  # Đóng trình duyệt sau khi hoàn thành đoạn 1

    # In ra thông tin ở định dạng JSON
    print(json.dumps(all_courses, ensure_ascii=False, indent=4))

# Hàm thu thập bình luận từ tất cả các môn học
def collect_reviews_from_all():
    driver = webdriver.Firefox(service=service)  # Mở lại trình duyệt
    driver.get("https://titv.vn/")
    time.sleep(10)  # Tăng thời gian chờ tải trang

    # Click vào thẻ "All"
    button_all = driver.find_element(By.CSS_SELECTOR, 'span[data-id="all"]')
    button_all.click()
    time.sleep(10)  # Tăng thời gian chờ để đảm bảo nội dung tải xong

    # Hàm cuộn xuống để tải thêm môn học
    def scroll_down():
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Tăng thời gian chờ giữa các lần cuộn
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    scroll_down()  # Cuộn xuống để tải hết nội dung

    course_elements = driver.find_elements(By.CSS_SELECTOR, 'div.ms_lms_courses_card_item_wrapper')
    if not course_elements:
        print("Không còn môn học nào trong thẻ All để thu thập.")
        return

    all_reviews = {}  # Tạo từ điển để chứa bình luận

    for i in range(len(course_elements)):
        try:
            course_link = course_elements[i].find_element(By.CSS_SELECTOR, 'a')
            course_link.click()
            time.sleep(10)  # Tăng thời gian chờ để đảm bảo nội dung tải xong

            course_name_element = driver.find_element(By.CSS_SELECTOR, 'h1')
            course_name = course_name_element.text

            reviews = driver.find_elements(By.CSS_SELECTOR, '.masterstudy-single-course-reviews__item-content p')
            if reviews:
                review_list = [review.text for review in reviews]
                all_reviews[course_name] = review_list
            else:
                all_reviews[course_name] = []

            driver.back()
            time.sleep(10)  # Tăng thời gian chờ trước khi quay lại

            # Cuộn xuống để đảm bảo có đầy đủ môn học
            scroll_down()
            course_elements = driver.find_elements(By.CSS_SELECTOR, 'div.ms_lms_courses_card_item_wrapper')

        except Exception as e:
            # Bỏ qua lỗi và không in ra
            continue

    driver.quit()  # Đóng trình duyệt sau khi hoàn thành đoạn 2

    # In ra bình luận ở định dạng JSON
    print(json.dumps(all_reviews, ensure_ascii=False, indent=4))

# Chạy đoạn 1
collect_course_info()

# Chạy đoạn 2
collect_reviews_from_all()


