import mysql.connector
from faker import Faker
from datetime import datetime
from werkzeug.security import generate_password_hash
import random
# MySQLに接続
conn = mysql.connector.connect(
    host='db',
    user='ope1',
    password='ope1',
    database='shiftOptimization'
)
cursor = conn.cursor()

# Fakerインスタンスを作成
fake = Faker('jp-JP')

# ランダムなデータを生成して挿入
for _ in range(10):
    name = fake.name()
    facility = fake.company()
    job = fake.job()
    password = generate_password_hash('password')
    facility_id = random.randint(33, 37)    
    is_admin = random.randint(0, 1)
    employee_type_id = random.randint(23, 30)
    qualification = fake.word() + "資格"
    constraint = fake.word() + "制約"
    qualification_id = random.randint(89, 98)
    constraint_id = random.randint(11, 52)
    if 21 <= constraint_id <= 32:
        constraint_id = 33
    
    # cursor.execute(
    #     "INSERT INTO facilities (name,created_at, updated_at) VALUES (%s, %s, %s)",
    #     (facility, datetime.now(), datetime.now())
    # # )
    # cursor.execute(
    #     "INSERT INTO users (facility_id, username, password_hash,is_admin,created_at,updated_at) VALUES (%s, %s, %s,%s, %s, %s)",
    #     (facility_id, name,password, is_admin,datetime.now(), datetime.now())
    # )
    
    # cursor.execute(
    #     "INSERT INTO employee_types (type_name, created_at, updated_at) VALUES (%s, %s, %s)",
    #     (job, datetime.now(), datetime.now())
    # )

    # employeesテーブルへのデータ挿入
    # cursor.execute(
    #     "INSERT INTO employees (facility_id, first_name, last_name, employee_type_id, is_delete, created_at, updated_at) VALUES (%s, %s, %s, %s, %s,%s, %s)",
    #     (facility_id, fake.first_name(), fake.last_name(), employee_type_id, 0,datetime.now(), datetime.now())  # employee_type_idやis_deleteもランダムで設定
    # )

    # qualificationsテーブルへのデータ挿入
    # cursor.execute(
    #     "INSERT INTO qualifications (name, created_at, updated_at) VALUES (%s, %s, %s)",
    #     (qualification, datetime.now(), datetime.now())
    # )

    # constraintsテーブルへのデータ挿入
    # cursor.execute(
    #     "INSERT INTO constraints (name, created_at, updated_at) VALUES (%s, %s, %s)",
    #     (constraint, datetime.now(), datetime.now())
    # )

    # facility_qualificationsテーブルへのデータ挿入
    # cursor.execute(
    #     "INSERT INTO facility_qualifications (facility_id, qualification_id) VALUES (%s, %s)",
    #     (facility_id, qualification_id)
    # )

    # facility_constraintsテーブルへのデータ挿入
    # cursor.execute(
    #     "INSERT INTO facility_constraints (facility_id, constraint_id) VALUES (%s, %s)",
    #     (facility_id, constraint_id)
    # )

    # # employee_qualificationsテーブルへのデータ挿入
    # employee_ids = [13,15,20,26,31]
    # qualification_ids = [89,90,92,93,95,98]
    # cursor.execute(
    #     "INSERT INTO employee_qualifications (employee_id, qualification_id) VALUES (%s, %s)",
    #     (random.choice(employee_ids), random.choice(qualification_ids))
    # )

    # employee_constraintsテーブルへのデータ挿入
    # employee_ids = [13,15,20,26,31]
    # constraint_ids = [12,16,20,33,39,40,43,50]
    # cursor.execute(
    #     "INSERT INTO employee_constraints (employee_id, constraint_id, value, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)",
    #     (random.choice(employee_ids), random.choice(constraint_ids), random.randint(3, 7),datetime.now(), datetime.now())
    # )

    # day_off_requestsテーブルへのデータ挿入
    # employee_ids = [13, 15, 20, 26, 31, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    # type_of_vacations = ["有給", "特休", "代休", "慶休", "産休", "育休", "公休"]
    # date = f"2024-08-{random.randint(1,31):02d}"
    # cursor.execute(
    #     "INSERT INTO day_off_requests (employee_id, date, type_of_vacation, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)",
    #     (random.choice(employee_ids), date, random.choice(type_of_vacations), datetime.now(), datetime.now())
    # )


    


conn.commit()
cursor.close()
conn.close()
