from pymongo import MongoClient
from datetime import datetime

# Kết nối tới MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["course_database"]
courses_collection = db["courses"]

# 1. Tìm tất cả các khóa học trong một danh mục cụ thể
print("Tất cả các khóa học trong danh mục 'Data Science':")
courses_in_category = courses_collection.find({"category": "Data Science"})
for course in courses_in_category:
    print(course)

# 2. Lấy các khóa học có rating trên 4.5
print("\nCác khóa học có rating trên 4.5:")
high_rating_courses = courses_collection.find({"rating": {"$gt": 4.5}})
for course in high_rating_courses:
    print(course)

# 3. Tìm khóa học có tên cụ thể
print("\nKhóa học có tên 'Python for Beginners':")
course_name = courses_collection.find_one({"name": "Python for Beginners"})
print(course_name)

# 4. Tìm khóa học với giá từ 100 đến 200
print("\nCác khóa học với giá từ 100 đến 200:")
mid_price_courses = courses_collection.find({"price": {"$gte": 100, "$lte": 200}})
for course in mid_price_courses:
    print(course)

# 5. Lấy danh sách các khóa học có từ 100 thành viên trở lên
print("\nCác khóa học có từ 100 thành viên trở lên:")
high_member_courses = courses_collection.find({"members_count": {"$gte": 100}})
for course in high_member_courses:
    print(course)

# 6. Đếm số khóa học trong một danh mục
category_count = courses_collection.count_documents({"category": "Machine Learning"})
print("\nSố khóa học trong danh mục 'Machine Learning':", category_count)

# 7. Sắp xếp khóa học theo số lượt xem giảm dần
print("\nCác khóa học sắp xếp theo số lượt xem giảm dần:")
sorted_courses = courses_collection.find().sort("views_count", -1)
for course in sorted_courses:
    print(course)

# 8. Lấy 5 khóa học đầu tiên trong danh mục "Programming"
print("\n5 khóa học đầu tiên trong danh mục 'Mới học lập trình':")
first_5_programming_courses = courses_collection.find({"category": "Mới học lập trình"}).limit(5)
for course in first_5_programming_courses:
    print(course)

# 9. Tìm khóa học không có bình luận nào
print("\nCác khóa học không có bình luận nào:")
no_review_courses = courses_collection.find({"reviews": {"$size": 0}})
for course in no_review_courses:
    print(course)

# 10. Cập nhật rating cho một khóa học cụ thể
print("\nCập nhật rating cho khóa học 'Data Science 101':")
courses_collection.update_one({"name": "Data Science 101"}, {"$set": {"rating": 4.8}})
for course in courses_collection.find({"name": "Data Science 101"}):
    print(course)

# 11. Tăng số lượng thành viên cho khóa học "Python for Beginners"
print("\nTăng số lượng thành viên cho khóa học 'Python for Beginners':")
courses_collection.update_one({"name": "Python for Beginners"}, {"$inc": {"members_count": 10}})
for course in courses_collection.find({"name": "Python for Beginners"}):
    print(course)

# 12. Xóa các khóa học có rating dưới 2
print("\nXóa các khóa học có rating dưới 2:")
courses_collection.delete_many({"rating": {"$lt": 2}})
for course in courses_collection.find():
    print(course)

# 13. Tìm khóa học có ít nhất một bình luận chứa từ "excellent"
print("\nCác khóa học có bình luận chứa từ 'excellent':")
excellent_review_courses = courses_collection.find({"reviews": {"$elemMatch": {"$regex": "excellent", "$options": "i"}}})
for course in excellent_review_courses:
    print(course)

# 14. Lấy các khóa học có giá trị rating hoặc số thành viên nhất định
print("\nCác khóa học có rating là 5 hoặc có trên 500 thành viên:")
rating_or_member_courses = courses_collection.find({"$or": [{"rating": 5}, {"members_count": {"$gt": 500}}]})
for course in rating_or_member_courses:
    print(course)

# 15. Cập nhật giá cho tất cả khóa học trong một danh mục
print("\nCập nhật giá cho tất cả khóa học trong danh mục 'Web Development':")
courses_collection.update_many({"category": "Web Development"}, {"$set": {"price": "150"}})
for course in courses_collection.find({"category": "Web Development"}):
    print(course)

# 16. Tìm khóa học có tên chứa "JavaScript"
print("\nCác khóa học có tên chứa 'JavaScript':")
javascript_courses = courses_collection.find({"name": {"$regex": "JavaScript", "$options": "i"}})
for course in javascript_courses:
    print(course)

# 17. Lấy danh sách tất cả danh mục khóa học
print("\nDanh sách tất cả các danh mục khóa học:")
categories = courses_collection.distinct("category")
print(categories)

# 18. Thêm đánh giá vào một khóa học cụ thể
print("\nThêm đánh giá vào khóa học 'Machine Learning Basics':")
courses_collection.update_one({"name": "Machine Learning Basics"}, {"$push": {"reviews": "Great course!"}})
for course in courses_collection.find({"name": "Machine Learning Basics"}):
    print(course)

# 19. Tìm tất cả khóa học có số lượt xem cao nhất trong từng danh mục
print("\nKhóa học có số lượt xem cao nhất trong từng danh mục:")
max_view_courses = courses_collection.aggregate([
    {"$group": {"_id": "$category", "max_views": {"$max": "$views_count"}}}
])
for course in max_view_courses:
    print(course)
#20 Các khóa học có nhiều hơn 3 đánh giá
print("\nCác khóa học có nhiều hơn 3 đánh giá:")
many_review_courses = courses_collection.find({"$expr": {"$gt": [{"$size": "$reviews"}, 3]}})
for course in many_review_courses:
    print(course)

