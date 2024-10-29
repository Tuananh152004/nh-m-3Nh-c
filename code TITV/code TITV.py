#from selenium import webdriver
#from selenium.webdriver.firefox.service import Service
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#import time
#from pymongo import MongoClient

# Đường dẫn tới geckodriver
#gecko_path = r"C:\Users\HP\Downloads\geckodriver-v0.35.0-win64\geckodriver.exe"
#service = Service(gecko_path)

# Kết nối tới MongoDB
#mongo_client = MongoClient("mongodb://localhost:27017/")
#db = mongo_client["course_database"]
#courses_collection = db["courses"]

# Hàm thu thập thông tin khóa học
#def collect_course_info():
#    driver = webdriver.Firefox(service=service)
#    driver.get("https://titv.vn/")
#    time.sleep(10)

#    all_courses = {}

#    # Vòng lặp để thu thập các khóa học
#    for data_id in range(75, 82):
#        li_element = WebDriverWait(driver, 20).until(
#            EC.element_to_be_clickable((By.CSS_SELECTOR, f'span[data-id="{data_id}"]'))
#        )
#        li_name = li_element.text
#        li_element.click()
#        time.sleep(10)

#        course_elements = WebDriverWait(driver, 20).until(
#            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.ms_lms_courses_card_item'))
#        )

#        # Lặp qua từng khóa học
#        for course in course_elements:
#            try:
#                course_name = WebDriverWait(course, 20).until(
#                    EC.presence_of_element_located((By.CSS_SELECTOR,
#                        'div.ms_lms_courses_card_item_wrapper > div:nth-child(2) > a:nth-child(1) > h3'))
#                ).text

#                price_element = WebDriverWait(course, 20).until(
#                    EC.presence_of_element_located((By.CSS_SELECTOR,
#                        'div.ms_lms_courses_card_item_info_price > div.ms_lms_courses_card_item_info_price_single > span'))
#                ).text

#                rating_element = WebDriverWait(course, 20).until(
#                    EC.presence_of_element_located((By.CSS_SELECTOR,
#                        'div.ms_lms_courses_card_item_info_rating_quantity > span'))
#                ).text

#                members_count = WebDriverWait(course, 20).until(
#                    EC.presence_of_element_located((By.CSS_SELECTOR,
#                        'div.ms_lms_courses_card_item_meta_block > i.stmlms-members + span'))
#                ).text

#                views_count = WebDriverWait(course, 20).until(
#                    EC.presence_of_element_located((By.CSS_SELECTOR,
#                        'div.ms_lms_courses_card_item_meta_block > i.stmlms-views + span'))
#                ).text

#                # Chuyển đổi các trường sang dạng số
#                rating_numeric = float(rating_element) if rating_element else 0.0
#                price_numeric = float(price_element.replace(',', '').replace('đ', '').strip()) if price_element and price_element.lower() != "free" else 0.0
#                members_count_numeric = int(members_count.replace(',', '').strip()) if members_count else 0
#                views_count_numeric = int(views_count.replace(',', '').strip()) if views_count else 0

#                course_info = {
#                    "name": course_name,
#                    "price": price_numeric,
#                    "rating": rating_numeric,
#                    "members_count": members_count_numeric,
#                    "views_count": views_count_numeric,
#                    "category": li_name,
#                }
#                all_courses[course_name] = course_info

#            except Exception as e:
#                print(f"Error collecting course info: {e}")
#                continue

#        driver.back()
#        time.sleep(10)

#    driver.quit()

#    # Lưu thông tin khóa học vào MongoDB
#    for course_name, course_info in all_courses.items():
#        try:
#            courses_collection.update_one(
#                {"name": course_name},
#                {"$set": course_info},
#                upsert=True
#            )
#        except Exception as e:
#            print(f"Error saving course {course_name}: {e}")

#    return all_courses

# Chạy đoạn 1 để thu thập thông tin khóa học
#collect_course_info()

from pymongo import MongoClient

# Kết nối tới MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["course_database"]
courses_collection = db["courses"]

# Nhóm 1: Tìm kiếm và liệt kê các khóa học
print("=== Tìm kiếm và liệt kê các khóa học ===")

# 1. Tìm tất cả các khóa học
all_courses = list(courses_collection.find())
print("Tất cả các khóa học:", all_courses)

# 2. Tìm khóa học theo tên
course_by_name = courses_collection.find_one({"name": "[Video] Microsoft Excel cơ bản"})
print("Khóa học theo tên:", course_by_name)

# 3. Tìm khóa học trong danh mục "Kiến thức nền tảng"
foundation_courses = list(courses_collection.find({"category": "Kiến thức nền tảng"}))
print("Khóa học Kiến thức nền tảng:", foundation_courses)

# 4. Tìm khóa học có số lượng thành viên lớn hơn 20,000
popular_courses = list(courses_collection.find({"members_count": {"$gt": 20000}}))
print("Khóa học có số lượng thành viên lớn hơn 20,000:", popular_courses)

# 5. Tìm khóa học có giá là 0
free_courses = list(courses_collection.find({"price": 0}))
print("Khóa học miễn phí:", free_courses)

# Nhóm 2: Đếm và cập nhật dữ liệu
print("\n=== Đếm và cập nhật dữ liệu ===")

# 6. Đếm số lượng khóa học trong danh mục "Data Science"
data_science_count = courses_collection.count_documents({"category": "Data Science"})
print("Số lượng khóa học Data Science:", data_science_count)

# 7. Tìm khóa học có rating cao nhất
highest_rated_course = courses_collection.find_one(sort=[("rating", -1)])
print("Khóa học có rating cao nhất:", highest_rated_course)

# 8. Tìm khóa học có số lượt xem lớn hơn 10,000
popular_viewed_courses = list(courses_collection.find({"views_count": {"$gt": 10000}}))
print("Khóa học có lượt xem lớn hơn 10,000:", popular_viewed_courses)

# 9. Cập nhật số lượng thành viên cho khóa học "Git và GitHub toàn tập"
courses_collection.update_one(
    {"name": "[Video] Git và GitHub toàn tập"},
    {"$set": {"members_count": 16000}}
)
updated_course = courses_collection.find_one({"name": "[Video] Git và GitHub toàn tập"})
print("Khóa học sau khi cập nhật số lượng thành viên:", updated_course)

# 10. Xóa khóa học có tên "[Video] Nguyên lý Hệ điều hành"
courses_collection.delete_one({"name": "[Video] Nguyên lý Hệ điều hành"})
print("Đã xóa khóa học '[Video] Nguyên lý Hệ điều hành'.")

# Nhóm 3: Tìm khóa học theo điều kiện khác
print("\n=== Tìm khóa học theo điều kiện khác ===")

# 11. Tìm tất cả khóa học có rating = 0
zero_rating_courses = list(courses_collection.find({"rating": 0}))
print("Khóa học có rating bằng 0:", zero_rating_courses)

# 12. Tìm khóa học theo ID
course_by_id = courses_collection.find_one({"_id": "6720b69a572a75111ce409bb"})
print("Khóa học theo ID:", course_by_id)

# 13. Tìm tất cả khóa học có số lượt xem từ 5,000 đến 10,000
views_range_courses = list(courses_collection.find({"views_count": {"$gte": 5000, "$lte": 10000}}))
print("Khóa học có số lượt xem từ 5,000 đến 10,000:", views_range_courses)

# Nhóm 4: Cập nhật và nhóm khóa học
print("\n=== Cập nhật và nhóm khóa học ===")

# 14. Cập nhật rating cho tất cả khóa học có rating = 0 thành 1
courses_collection.update_many(
    {"rating": 0},
    {"$set": {"rating": 1}}
)
print("Đã cập nhật rating cho tất cả khóa học có rating bằng 0.")

# 15. Tìm khóa học có số lượng thành viên lớn hơn 5,000 và thuộc danh mục "Data Science"
data_science_popular = list(courses_collection.find({"members_count": {"$gt": 5000}, "category": "Data Science"}))
print("Khóa học Data Science có số lượng thành viên lớn hơn 5,000:", data_science_popular)

# 16. Tìm khóa học có giá khác 0
paid_courses = list(courses_collection.find({"price": {"$ne": 0}}))
print("Khóa học có giá khác 0:", paid_courses)

# Nhóm 5: Tóm tắt dữ liệu
print("\n=== Tóm tắt dữ liệu ===")

# 17. Đếm số lượng khóa học trong từng danh mục
category_count = courses_collection.aggregate([
    {"$group": {"_id": "$category", "count": {"$sum": 1}}}
])
print("Số lượng khóa học trong từng danh mục:")
for category in category_count:
    print(category)

# 18. Tìm khóa học có số lượng thành viên tối thiểu
min_members_course = courses_collection.find_one(sort=[("members_count", 1)])
print("Khóa học có số lượng thành viên tối thiểu:", min_members_course)

# 19. Tìm khóa học có số lượt xem nhiều nhất
most_viewed_course = courses_collection.find_one(sort=[("views_count", -1)])
print("Khóa học có số lượt xem nhiều nhất:", most_viewed_course)

# 20. Lấy danh sách tên khóa học
course_names = [course["name"] for course in courses_collection.find()]
print("Danh sách tên khóa học:", course_names)

# Đóng kết nối
mongo_client.close()

