#  선박 확인 체계 서버 구현

## 1. 개발 목적
* 기존에 선박을 관리 방식은 문서화를 통해 매번 사진을 찍어 PC에 업로드 후 선박 정보를 작성하여 관리.
* 선박을 등록하고 수정하는 방식의 소요가 너무 크므로 어플을 통해 서버에서 선박을 관리하고 수정되는 방식을 채택하게 됨.
* 추가적으로 등록된 선박들 중 AI를 이용하여 선박을 식별하는 기능이 필요.

## 2. 개발 스택 및 도구
`Python` `Django` `django-restframework` `tensorflow` `postman` `NginX` `guniconr`

## 3. 맡은 역할
* 선박 및 유저 DB 모델 설계 및 구축
* REST API를 이용하여 선박 정보 등록, 수정, 삭제 등을 어플에서 할 수 있도록 작성.
* 선박 DB 에 등록되어 있는 선박 중 학습 데이터가 많은 선박 순으로 학습을 한 후 학습된 h5 파일을 이용하여 선박 예측 값을 어플로 보내주는 API 작성.

## 4. 모델 설계 및 작성
* ERD
![](erd.png)
> 테이블 상세 내용
> 1. Account
>   * 유저 정보 필드를 가지고 있는 테이블.
>   * 기존 django 에서 제공되는 AbstractBaseUser 모델을 상속 받아서 작성.
>   * 필요한 모델을 추가로 작성. ex) unit, rank, phone ...
>   * approve 라는 승인 필드를 만들어 승인되지 않으면 서버 로그인 불가능.
>   * user_level 을 통해 유저 별 권한이 존재.
>   * block_no 을 통해 로그인 실패 조건 충족 시 계정 잠금.
>   * fail_cnt 을 통해 로그인 실패 횟수 저장.
> 2. Question
>   * 1:1 문의를 위해 제목(title), 질문내용(content) 필드
>   * 답변 상태를 status 를 통해 표시
>   * date 필드를 통해 작성 날짜 저장, writer 필드를 통해 작성자 저장.
> 3. Answer
>   * Question에 대한 답변 필드를 1대1로 지정.
>   * date 필드를 통해 답변 날짜 작성.
> 4. Notice
>   * 공지사항에 대한 정보를 저장하는 테이블.
>   * 제목, 날짜, 공지사항 내용을 저장하는 필드
> 5. NormalShip
>   * 기본적인 선박 정보 필드를 가지는 테이블.
>   * 추가적으로 is_train 필드를 통해 학습이 되어있는 선박인지 확인 가능.
>   * 각종 장치 여부를 위한 필드 존재. (is_ff, is_ais, is_vpass, is_vhf)
>   * 해당 선박의 이미지 개수를 저장하는 img_cnt 필드
>   * main_img, main_img_id 필드를 이용하여 선박의 대표 이미지 경로 저장.
> 6. NormalImage
>   * NormalShip 을 외래키로 갖는 n_name 필드
>   * 해당 선박의 이미지를 저장할 img 필드
> 7. WasteShip
>   * 사용되지 않고 방치된 유기 선박들을 따로 관리하기 위한 테이블.
>   * 선박의 위치를 통해 식별하기 위해 lat, lon 필드 존재(위도, 경도)
>   * 유기 선박의 특징을 기록할 수 있는 info 필드 존재.
> 8. WasteImage
>   * WasteShip 을 외래키로 갖는 w_id 필드
>   * 유기 선박의 이미지를 저장할 img 필드
>   * 사진이 찍힌 위치를 저장할 lat, lon 필드
> 9. OwnerInfo
>   * NormalShip 을 외래키로 갖는 ship 필드
>   * 해당 선박의 선주 정보를 저장하는 테이블
>   * agreement_paper 필드에는 개인정보이용동의서를 저장
>   * own_img 필드는 선주 이미지를 저장

## 5. 필요한 모듈 개발
`best_three.py` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/3baf99bbd30ce9402d126a04d690d7b5773c6b4c/ship_server/utils/best_three.py#L1-L26)
* 매개변수로 받은 배열에서 값이 제일 높은 인덱스를 통해 라벨에서 값이 가져오고 해당 값의 포맷팅 변경하여 제일 높은 순서 3개를 리턴.

`change_format.py` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/3baf99bbd30ce9402d126a04d690d7b5773c6b4c/ship_server/utils/change_format.py#L1-L33)
* 매개변수로 받은 serializer 딕셔너리 데이터에서 date 키값의 value 값의 날짜 포맷팅을 변경해준 후 딕셔너리 리턴.
* `change_unit` 함수는 입력 받은 부대의 포맷팅 수정하여 딕셔너리 리턴.

`check_pw.py` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/3baf99bbd30ce9402d126a04d690d7b5773c6b4c/ship_server/utils/check_pw.py#L1-L36)
* 비밀번호 조건의 충족하는지 검사하는 함수 작성.
* 반복된 값이 있는지 여부와 오름차순 또는 내림차순이 있는지 확인.
* 조건이 충족되지 않는다면 어떤 조건이 충족되지 않는지 메시지와 상태 코드 리턴.

`custom_view.py` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/3baf99bbd30ce9402d126a04d690d7b5773c6b4c/ship_server/utils/custom_view.py#L1-L25)
* django 에서 제공해주는 django-restframework 에서 APIView 를 불러와서 상속하여 APIView 를 작성.
* `success`, `fail` 함수를 통해 200, 400 을 리턴해주고 데이터와 메시지를 넣을 수 있도록 작성.

`prediction_ship.py` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/3baf99bbd30ce9402d126a04d690d7b5773c6b4c/ship_server/keras_model/prediction_ship.py#L1-L19)
* h5 모델 파일을 로드한 후 입력 받은 이미지를 전처리하여 데이터 입력 후 결과 값을 리턴.

## 6. API 작성

### 1. Accounts
`LoginAPI` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/3baf99bbd30ce9402d126a04d690d7b5773c6b4c/ship_server/Accounts/views.py#L19-L47)
* 클라이언트로부터 받은 srvno, password 를 이용하여 DB에 등록된 유저인지 확인 후 유효한 데이터라면 토큰 값을 respnse에 담아서 리턴.
* 유효한지 체크할 때는 serializers 에서 validate 를 통해 유효성 검사 로직 작성. [LoginSerializer.validate](https://github.com/KangJuSeong/shipCheck_server/blob/3baf99bbd30ce9402d126a04d690d7b5773c6b4c/ship_server/Accounts/serializers.py#L20-L73)
* 유효한 유저 정보라도 로그인 실패 조건(3달간 미접속, 비밀번호 3회 이상 불일치, 계정 정지)이 충족되면 로그인이 될 수 없음.

`LogoutAPI` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/3baf99bbd30ce9402d126a04d690d7b5773c6b4c/ship_server/Accounts/views.py#L50-L57)
* 요청이 왔을 때 헤더에 담긴 토큰 값이 유효하다면 로그아웃 성공을 응답으로 보내주고 유효하지 않다면 실패 메시지를 리턴.

`SignUpAPI` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/3baf99bbd30ce9402d126a04d690d7b5773c6b4c/ship_server/Accounts/views.py#L60-L90)
* `permission_classes = [AllowAny]` 구문을 작성하여 회원가입을 할 때는 토큰값이 필요 없으므로 모든 클라이언트가 접근 가능하도록 함.
* Body 로 받은 값을 이용하여 유저를 생성해주고 만약 조건이 충족되지 않는다면 실패 메시지를 응답으로 보내줌.

`UserInfoAPI` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/3baf99bbd30ce9402d126a04d690d7b5773c6b4c/ship_server/Accounts/views.py#L93-L102)
* 헤더에 담긴 토큰값을 통해 유저의 정보를 응답으로 보내줌.

`UserPermissionAPI` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/3baf99bbd30ce9402d126a04d690d7b5773c6b4c/ship_server/Accounts/views.py#L105-L113)
* 유저의 권한을 요청하는 API 로 유저 권한 값을 응답으로 보내줌.
* 유저의 권한이 특정 값 이상일 때만 요청할 수 있는 API 가 있기 때문에 필요.

`VersionCheckAPI` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/3baf99bbd30ce9402d126a04d690d7b5773c6b4c/ship_server/Accounts/views.py#L116-L122)
* 현재 클라이언트에서 사용중인 버전을 요청으로 보내면 현재 서버 버전과 일치하는지 확인하는 API.
* 추가로 응답을 보낼 때 현재 서버가 운영중인지 점검중인지에 대한 데이터를 보내줌.

### 2. Post
`NoticeAPI` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/3baf99bbd30ce9402d126a04d690d7b5773c6b4c/ship_server/Post/views.py#L12-L25)
* id 값을 통해 클라이언트에서 선택한 공지사항에 대한 데이터를 DB 에서 가져와서 리턴.

`NoticeListAPI` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/3baf99bbd30ce9402d126a04d690d7b5773c6b4c/ship_server/Post/views.py#L28-L41)
* 클라이언트에 DB 에 등록되어 있는 모든 공지사항을 목록으로 보여주기 위해 모든 공지사항을 불러와서 리턴.
* 공지사항 목록이 클라이언트에 보여질 때 최근 날짜가 맨 위로 보여야되기 때문에 쿼리를 날릴 때 `order_by('-date')`를 추가하여 날려줌.

`QuestionAPI` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/ca0cb7169f162e8c3496d8f556bf5fbb36e8d961/ship_server/Post/views.py#L44-L71)
* `get` 메서드로 요청이 들어오면 id 값을 가진 질문에 대한 데이터를 응답해줌.
* `delete` 메서드로 요청이 들어오면 id 값을 가진 데이터를 DB 에서 제거.

`QuestionCreateAPI` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/0bc923fedf59c94c7b82bf423dd0a9e5d9055e0c/ship_server/Post/views.py#L74-L87)
* Body 를 통해 받은 값을 이용하여 Question 데이터를 생성.

`QuestionListAPI` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/0bc923fedf59c94c7b82bf423dd0a9e5d9055e0c/ship_server/Post/views.py#L90-L104)
* 모든 질문 데이터를 DB 에서 가져와 응답으로 보내줌.
* `order_by('-date')` 를 쿼리에 추가하여 날리므로 최근 등록된 질문 부터 순서대로 정렬되어 클라이언트에서 볼 수 있음.

`AnswerAPI` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/0bc923fedf59c94c7b82bf423dd0a9e5d9055e0c/ship_server/Post/views.py#L107-L120)
* 클라이언트에서 질문에 대한 답변을 요청하면 해당 질문의 id 값을 통해 DB 에서 질문의 답변을 가져와서 응답.

### 3. Ships
`DetailNormalShipAPI, DetailWasteShipAPI`

`CreateNormalShipAPI, CreateWasteShipAPI`

## 7. 배포
* 클라우드 서버에 Django 프로젝트 업로드.
* `NginX` 와 `Gunicorn`을 이용하여 서버 배포