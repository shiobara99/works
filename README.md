# 冷蔵庫の在庫管理 + ユーザー管理システム

卒業制作プロジェクト

## プロジェクト概要

- **logintest.py**: ユーザー登録・ログインシステム
- **foodslist.py**: 冷蔵庫の在庫管理アプリ
  - 食材データの登録・編集・削除
  - 期限切れ警告表示
  - カテゴリ絞り込み
  - 在庫金額計算

## 技術スタック

- **Framework**: Flask
- **Database**: MySQL/MariaDB (limitrecord)
- **ORM**: SQLAlchemy
- **Password Hashing**: Werkzeug

## セットアップ

### 前提条件

- Python 3.8+
- XAMPP (MySQL/MariaDB)
- Git

### インストール

1. リポジトリをクローン
   ```bash
   git clone <repository_url>
   cd 卒業制作
   ```

2. 仮想環境を作成
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. 依存パッケージをインストール
   ```bash
   pip install flask flask-sqlalchemy pymysql werkzeug
   ```

4. XAMPP を起動して MySQL を実行
   - MySQL が 127.0.0.1:3306 で稼働している必要があります

5. データベースを作成
   - phpMyAdmin で `limitrecord` データベースを作成

### 実行

#### ユーザー管理システム (ポート 5000)
```bash
python logintest.py
```

#### 在庫管理システム (ポート 5001)
```bash
python foodslist.py
```

ブラウザで以下にアクセス：
- ユーザー管理: http://127.0.0.1:5000
- 在庫管理: http://127.0.0.1:5001

## ファイル構成

```
卒業制作/
├── logintest.py           # ユーザー管理アプリケーション
├── foodslist.py          # 在庫管理アプリケーション
├── templates/
│   ├── logintest.html    # ユーザー登録・ログイン画面
│   ├── foodslist.html    # 在庫一覧・追加画面
│   └── edit_food.html    # 在庫編集画面
├── static/
│   └── images/           # カテゴリ別のアイコン画像
├── .gitignore
└── README.md
```

## データベース情報

- **ホスト**: 127.0.0.1
- **ユーザー**: root
- **パスワード**: なし（設定済みの場合は編集してください）
- **データベース**: limitrecord

### テーブル構成

#### User テーブル
- user_id (Primary Key)
- name (ユーザー名)
- email (メール、一意）
- password（ハッシュ化済み)

#### Food テーブル
- id (Primary Key)
- name (食材名)
- category (カテゴリ)
- quantity (数量)
- unit_price (単価)
- expiration_date (期限日)
- notes (メモ)

## 機能

### ユーザー管理
- ユーザー登録
- ログイン / ログアウト
- パスワードはハッシュ化して暗号化保存
- セッション管理

### 在庫管理
- 食材の登録・編集・削除
- カテゴリ別の絞り込み
- 期限切れ・期限間近の警告表示
  - 期限切れ: 赤色背景
  - 期限3日以内: ピンク色背景
- 在庫の合計金額表示
- カテゴリアイコン表示（野菜・果物・乳製品・肉・調味料・その他）

## 今後の拡張案

- [ ] ログイン連携（在庫管理とユーザー管理の統合）
- [ ] 食材写真のアップロード機能
- [ ] 数量単位の複数対応（個・g・ml など）
- [ ] 購入日の記録
- [ ] 食材の検索機能
- [ ] エクスポート機能（CSV など）

## ライセンス

プロジェクトの内容

## 作成者

卒業制作チーム
