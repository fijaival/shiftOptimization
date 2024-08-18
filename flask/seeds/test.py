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
for _ in range(30):
    name = fake.name()
    facility = fake.company()
    job = fake.job()
    password = generate_password_hash('password')
    facility_id = random.randint(33, 37)    
    is_admin = random.randint(0, 1)
    employee_type_id = random.randint(23, 30)
    
    
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
    cursor.execute(
        "INSERT INTO employees (facility_id, first_name, last_name, employee_type_id, is_delete, created_at, updated_at) VALUES (%s, %s, %s, %s, %s,%s, %s)",
        (facility_id, fake.first_name(), fake.last_name(), employee_type_id, 0,datetime.now(), datetime.now())  # employee_type_idやis_deleteもランダムで設定
    )

conn.commit()
cursor.close()
conn.close()
