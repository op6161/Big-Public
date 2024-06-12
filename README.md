# [以前のプロジェクト](https://github.com/op6161/Big-team-archive/tree/main)
# [AIモデル ダウンロード](https://drive.google.com/file/d/1cClbhm3ddwfMYdL8EkUGavx2StlfzgEG/view?usp=sharing)
> repo/apps/upload/model/*.pt
---
# 無人施設(電気通信交換局舍)安全管理ウェブ

## このプロジェクトは教育したチームプロジェクト以後、個人的な学習目的と、個人的に惜しい点を補完したプロジェクトです。

## 既存のプロジェクトのリリース ファイルしか残っていないため、以前のバージョン管理はありません。

## 私はバックエンド、AI開発補助を担当しました。

<a href="https://www.python.org/">
    <img alt="Python" src ="https://img.shields.io/badge/Python-3776AB.svg?&style=for-the-badge&logo=Python&logoColor=white"/>
</a>
<a href="https://www.djangoproject.com/">
    <img alt="django" src ="https://img.shields.io/badge/django-092E20.svg?&style=for-the-badge&logo=django&logoColor=white"/>
</a>
<a href="https://github.com/ultralytics">
    <img alt="yolo" src ="https://img.shields.io/badge/yolov8-ee99ee.svg?&style=for-the-badge&logo=github&logoColor=white"/>
</a>
<div></div>
<img alt="JavaScript" src ="https://img.shields.io/badge/JavaScriipt-F7DF1E.svg?&style=for-the-badge&logo=JavaScript&logoColor=black"/>
<img alt="Css" src ="https://img.shields.io/badge/CSS3-1572B6.svg?&style=for-the-badge&logo=CSS3&logoColor=white"/>
<a href="https://www.djangoproject.com/">
    <img alt="bootstrap" src ="https://img.shields.io/badge/bootstrap-573A7D.svg?&style=for-the-badge&logo=bootstrap&logoColor=white"/>
</a>
<div></div>
<a href="https://sqlite.org/">
    <img alt="SQLite" src ="https://img.shields.io/badge/SQLite-3776AB.svg?&style=for-the-badge&logo=SQLite&logoColor=white"/>
</a>

---
# プロジェクトについて
### 「分岐局舍」とは？ (Telecommunicaionts switching station)
電気通信役務を提供する施設の維持のための建物


### プロジェクト進行理由
- センサー誤動作率が高い・センサー作動時、作業者の出動が必須
- 人的資源の浪費

### プロジェクト目標
- 指定された領域内の外部からの侵入者の検知(施設外部)(국사외부)
- 火災検知(施設内部)(국사내부)
- 作業者の安全事故の感知・作業服着用管理(作業者)(작업자 안전)

---

# 試演映像
### 作業者の会員登録
- ID重複検査
- パスワード二次検証

[![Join](http://img.youtube.com/vi/Kylr1ejgyyc/0.jpg)](https://youtu.be/Kylr1ejgyyc)

### 管理者の会員登録・お知らせ作成
- 管理者会員登録
- 管理者はお知らせ文を作成可能

[![Manager](http://img.youtube.com/vi/KKPYNn4maaE/0.jpg)](https://youtu.be/KKPYNn4maaE)

### 作業日誌
- 作業者は作業日誌を作成できる
- 管理者は作成された作業を承認することができる

[![Worklog](http://img.youtube.com/vi/Tbg_5vxUD9Y/0.jpg)](https://youtu.be/Tbg_5vxUD9Y)

### 動画アップロード
- 動画をアップロード
- アップロード後、AIオブジェクトを探知・映像ストリーミング
- ストリーミング終了後、アップロードに戻る

[![Upload](http://img.youtube.com/vi/iqDxCqaI4KQ/0.jpg)](https://youtu.be/iqDxCqaI4KQ)

### 映像ログ
- アップロードされた動画のオブジェクト探知内訳を見ることができる

[![Vlog](http://img.youtube.com/vi/XhBbbAUjqqQ/0.jpg)](https://youtu.be/XhBbbAUjqqQ)

### セッション
- ログイン後30分以降はセッションが満了し、再ログインが必要


##### [テスト映像の原本](https://www.youtube.com/watch?v=AXtarXhbbSk)

---
# 修正点

## 1. 映像アップロード (apps/upload)
##### [以前views.py](https://github.com/op6161/Big-team-archive/blob/main/apps/upload/views.py) 
##### [現在views.py](https://github.com/op6161/Big-Public-Codeonly/blob/main/apps/upload/views.py) [uploading.py](https://github.com/op6161/Big-Public-Codeonly/blob/main/apps/upload/uploading.py)
コードの可視性のために、viewコードとロジックコード(uploading.py)を分離しました。

同時に、全体的に重複していたコードを関数化して分離しました。

アップロード&ストリーミングをサイトテンプレートに合わせた新しいページで行うように修正しました。

[videoStream.html](https://github.com/op6161/Big-Public-Codeonly/blob/main/apps/upload/templates/upload/videoStream.html)



アップロード&ストリーミング作業が終わったら、ファイルアップロードページに戻るように修正しました。

[videoStream.html javascript](https://github.com/op6161/Big-Public-Codeonly/blob/main/apps/upload/templates/upload/videoStream.html)
・
[views.py line.15](https://github.com/op6161/Big-Public-Codeonly/blob/main/apps/upload/views.py)

## 2. 映像ログ(apps/videoLog)
##### [以前views.py](https://github.com/op6161/Big-team-archive/blob/main/apps/videoLog/views.py)
##### [現在views.py](https://github.com/op6161/Big-Public-Codeonly/blob/main/apps/videoLog/views.py)


以前のロジックは、映像メタデータによって正常なログ出力が不可能な場合があるため、メタデータを活用するように修正しました。

[(以前) line.35](https://github.com/op6161/Big-team-archive/blob/main/apps/videoLog/views.py)
> texts.append({'day':day,'event':event,'local':time ,'fps':round(int(fps)/24)})

[(現在) line.44](https://github.com/op6161/Big-Public-Codeonly/blob/main/apps/videoLog/views.py)
>texts.append({'day':day,'event':event,'local':time ,'fps':round(int(frame)/fps)})

ログ出力エラーを修正するために映像のメタデータであるfpsファイルを保存するように修正しました
> [apps/upload/uploading.py line.310](https://github.com/op6161/Big-Public-Codeonly/blob/main/apps/upload/uploading.py)