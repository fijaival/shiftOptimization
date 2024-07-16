# シフト自動生成 API

## 修正

テーブル定義しなおし
constraint を constraint に(外部製薬のところも変える)
リレーションシップ更新
instance を gitignore
drivers をなくす
employee に雇用形態追加
データ結合して返すときはどこで定義するか調査
service の切り出し

## 導入

このプロジェクトは、従業員のスキルセット、利用可能性、およびその他の制約を考慮して、効率的にシフトを自動生成する API を提供します。Flask をバックエンドフレームワークとして、SQLite をデータベースとして使用しています。

## 目次

- [導入](#導入)
- [機能](#機能)
- [始め方](#始め方)
  - [前提条件](#前提条件)
  - [インストール](#インストール)
  - [開発サーバ起動](#開発サーバ起動)
- [API エンドポイント](#apiエンドポイント)
- [依存関係](#依存関係)
- [参考サイト](#参考サイト)
- [API リクエストボディ](#リクエストボディ)

## 機能

- 従業員の利用可能性に基づいたシフト自動生成
- スキルセットと役割に基づくシフト割り当て
- シフトの調整と更新機能
- 従業員と管理者のためのインターフェース

## 始め方

### 前提条件

- Python 3.12.0 で動作確認済み
- pip

### インストール

リポジトリをクローンします。

```bash
git clone https://github.com/fijaival/shift_optimization_flask.git
cd shift_optimization_flask
```

python 仮想環境を構築し、環境を切り替えます。[参考](https://www.python.jp/install/windows/venv.html)

```
python -m venv .venv
.venv\Scripts\activate.bat
```

パッケージをインストールします。

```
pip install -r requirements.txt
```

### 開発サーバ起動

アプリケーションを起動します。

```
flask run
```

## API エンドポイント

# Authentication API

## Signup

**Method:** POST  
**Path:** `/auth/signup`  
**Request Body:**

```json
{
  "username": "string",
  "password": "string",
  "facility_id": "string"
}
```

**ResponseBody**:

```json
{
  "created_at": "2024-06-11T17:35:33",
  "facility": {
    "facility_id": 1,
    "name": ""
  },
  "is_admin": false,
  "updated_at": "2024-06-11T17:35:33",
  "user_id": 6,
  "username": "ope3"
}
```

## LOGIN

**Method:** POST  
**Path:** `/auth/login`  
**Request Body:**

```json
{
  "username": "string",
  "password": "string"
}
```

ResponseBody:

```json
{
  "login": true
}
```

## Refresh token

**Method:** POST  
**Path:** `/auth/login`  
**Request Body:**
**ResponseBody**:

```json
{
  "refresh": true,
  "access_token": "string"
}
```

## Logout

**Method:** DELETE  
**Path:** `/logout`  
**Request Body:**
**ResponseBody**:

```json
{
  "refresh": true,
  "access_token": "string"
}
```

## Get employees

**Method:** GET  
**Path:** `/facilities/<int:facility_id>/employees`  
**Request Body:**
**ResponseBody**:

```json
{
  "employees": [
    {
      "created_at": "2024-06-27T12:48:17",
      "dependencies": [],
      "employee_constraints": [],
      "employee_id": 10,
      "employee_type": {
        "employee_type_id": 3,
        "type_name": "非常勤調理員"
      },
      "first_name": "first_name",
      "last_name": "last_name",
      "qualifications": [],
      "updated_at": "2024-06-27T12:59:24"
    }
  ]
}
```

## Register employees

**Method:** POST
**Path:** `/facilities/<int:facility_id>/employees`  
**Request Body:**

```json
{
  "constraints": [
    {
      "constraint_id": 4,
      "value": 7
    },
    {
      "constraint_id": 3,
      "value": 4
    }
  ],
  "employee_type_id": 1,
  "first_name": "りょうま",
  "last_name": "さかもと",
  "qualifications": [
    {
      "qualification_id": 1
    },
    {
      "qualification_id": 2
    }
  ],
  "dependencies": [1]
}
```

**ResponseBody**:

```json
{
    "id": "integer",
    "name": "string",
    "position": "string",
    "salary": "number",
    "hire_date": "string" (ISO 8601 format, e.g., "2023-06-01T12:00:00Z")
}

```

## Delete employee

**Method:** DELETE
**Path:** `/facilities/<int:facility_id>/employees/<int:employee_id>`  
**Request Body:**
**ResponseBody**:

```json
{
  "message": "Employee deleted successfully!"
}
```

## Update employee

**Method:** PUT
**Path:** `/facilities/<int:facility_id>/employees/<int:employee_id>`  
**Request Body:**

```json
{
  "constraints": [
    {
      "constraint_id": 4,
      "value": 7
    },
    {
      "constraint_id": 3,
      "value": 4
    }
  ],
  "employee_type_id": 1,
  "first_name": "りょうま",
  "last_name": "さかもと",
  "qualifications": [
    {
      "qualification_id": 1
    },
    {
      "qualification_id": 2
    }
  ],
  "dependencies": [1]
}
```

**ResponseBody**:

```json
{
  "message": "Employee deleted successfully!"
}
```

## Register facility

**Method:** POST
**Path:** `/facilities`  
**Request Body:**

```json
{
  "name": "string"
}
```

## Delete facility

**Method:** DELETE
**Path:** `/facilities/<int:facility_id>`  
**Request Body:**

## Get facility info

**Method:** GET
**Path:** `/facilities/<int:facility_id>`  
**Request Body:**

## edit facility info

**Method:** POST
**Path:** `/facilities/<int:facility_id>`  
**Request Body:**

```json
{
  "name": "test_facility",
  "constraints": [{ "constraint_id": 1 }, { "constraint_id": 3 }],
  "qualifications": [{ "qualification_id": 1 }, { "qualification_id": 3 }],
  "tasks": [
    { "task_id": 2 },
    { "task_id": 4 },
    { "task_id": 1 },
    { "task_id": 3 },
    { "task_id": 5 }
  ]
}
```
