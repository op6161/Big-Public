# [既存のプロジェクト](https://github.com/op6161/Big-team-archive/tree/main)
# [AIモデル ダウンロード](https://drive.google.com/file/d/1cClbhm3ddwfMYdL8EkUGavx2StlfzgEG/view?usp=sharing)
> repo/apps/upload/model/*.pt
---
## このプロジェクトは教育したチームプロジェクト以後、個人的な学習目的と、個人的に惜しい点を補完したプロジェクトです。

## 既存のプロジェクトのリリース ファイルしか残っていないため、以前のバージョン管理はありません。

## 私はバックエンド、AI開発補助を担当しました。

---

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
# 프로젝트에 대해서
### (Telecommunicaionts switching station, 분기국사)

### 프로젝트를 진행한 이유
센서의 오작동시 발생하는 인적 자원 낭비를 방지

### 프로젝트 목표
화재 재난 감지(시설내부)
외부 침입자 감지(시설외부)
작업자 안전 관리(작업자)

### 프로젝트 시연
회원가입
공지사항
작업로그
영상로그
업로드
세션

---
# 修正点

## 1. 映像アップロード (apps/upload)
##### [기존views.py](https://github.com/op6161/Big-team-archive/blob/main/apps/upload/views.py) 
##### [수정views.py](https://github.com/op6161/Big-Public-Codeonly/blob/main/apps/upload/views.py) [uploading.py](https://github.com/op6161/Big-Public-Codeonly/blob/main/apps/upload/uploading.py)
django는 views.py 안에 모든 로직을 포함하도록 권장하지만, 코드의 가시성을 위해 분리한 상태입니다.

중복되는 코드를 함수화하고 분리하였습니다.

업로딩&스트리밍을 사이트 템플릿에 맞춘 새로운 페이지에서 진행하도록 수정하였습니다.

업로딩&스트리밍 작업이 끝나면 파일 업로드 페이지로 돌아가도록 수정하였습니다.

## 2. 영상로그출력(apps/videoLog)
##### [기존views.py](https://github.com/op6161/Big-team-archive/blob/main/apps/videoLog/views.py)
##### [수정views.py](https://github.com/op6161/Big-Public-Codeonly/blob/main/apps/videoLog/views.py)

#### FEAT
후술할 로그 출력 오류를 수정하기 위해서 영상의 메타데이터인 fps파일을 저장하도록 수정하였습니다.
> [apps/upload/uploading.py line.310](https://github.com/op6161/Big-Public-Codeonly/blob/main/apps/upload/uploading.py)

#### FIX
기존의 로직은 영상 메타데이터에 따라서 정상적인 로그 출력이 불가능한 경우가 생길 수 있었기에 메타데이터를 활용하도록 수정하였습니다.
> [(team) line.35    texts.append({'day':day,'event':event,'local':time ,'fps':round(int(fps)/24)})](https://github.com/op6161/Big-team-archive/blob/main/apps/videoLog/views.py)

> [(this) line.44    texts.append({'day':day,'event':event,'local':time ,'fps':round(int(frame)/fps)})](https://github.com/op6161/Big-Public-Codeonly/blob/main/apps/videoLog/views.py)

