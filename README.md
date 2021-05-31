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
`DetailShipAPI` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/d9de7fb485c0efd5c6b1b93dcd6e9ab9b4fcd584/ship_server/Ships/views.py#L30-L86)
* `get` 메서드로 요청이 들어오면 id 값을 통해 해당 선박의 정보를 응답으로 보내줌.
* id 값을 이용하여 쿼리를 날리면 해당 데이터를 불러올 때 register 필드가 외래키이므로 쿼리가 두개가 날아가는 현상을 발견.
* 위 현상을 해결하기 위해 `select_related('register')` 를 이용하여 한개의 쿼리로 가져올수 있음.
* 만약 100개의 선박 데이터 요청이 들어오면 선박 쿼리 100개와 register 필드에 대한 쿼리 100개가 발생하는 문제가 있으므로 `select_related`를 사용하는것이 맞다고 판단.
* `delete` 메서드로 요청이 들어오면 해당 id 값의 데이터를 제거.
* `post` 메서드로 요청이 들어오면 해당 id 값의 데이터를 Body 를 통해 받은 값으로 수정.
* `put` 메서드가 실제 서버 운용시에 요청이 들어오지 않아 사용할 수 없는 문제가 생겨 선박 데이터 생성 API 를 따로 작성.

`CreateShipAPI` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/d9de7fb485c0efd5c6b1b93dcd6e9ab9b4fcd584/ship_server/Ships/views.py#L89-L103)
* Body 를 통해 데이터가 들어오면 DB 에 선박 데이터 추가.
* 추가적으로 선박 등록이 완료 되면 해당 선박 id 값을 응답에 담아서 보내주고 클라이언트에서는 해당 선박의 이미지 등록 API 요청시 요청 Body 에 선박 id 값을 담아서 요청 함. 

`ListShipAPI` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/d9de7fb485c0efd5c6b1b93dcd6e9ab9b4fcd584/ship_server/Ships/views.py#L106-L144)
* 파라미터로 page(페이지 번호), tag(정렬 기준), unit(등록 부대) 를 받고 해당 값을 이용하여 선박 데이터들을 정렬하여 응답으로 보내줌.
* register 는 왜래키 이므로 `selected_relate`구문을 이용하고 정렬 시에는 `order_by`구문을 통해 쿼리를 날릴 때 조건을 추가하여 작성함.
* 가져온 데이터들으 개수를 확인하고 한 페이지에 보여줄 데이터의 개수를 정한 다음 해당 데이터들을 인덱싱하여 요청된 페이지에 맞춰 데이터를 보내줌.
* 응답에 현재 정렬 방식을 통해 계산된 총 페이지의 개수를 보내줌.

`SearchShipAPI` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/d9de7fb485c0efd5c6b1b93dcd6e9ab9b4fcd584/ship_server/Ships/views.py#L147-L180)
* Body 로 받은 데이터를 이용하여 선박 데이터를 필터링 하고 나온 데이터들을 한 페이지 당 보내줄 데이터의 개수에 따라 인덱싱 후 응답으로 보내줌.
* `searching_normal_ship` 함수를 작성하여 매개변수로 받은 데이터를 이용하여 필터링 하여 나온 데이터를 리턴.

`LocationShipAPI` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/d9de7fb485c0efd5c6b1b93dcd6e9ab9b4fcd584/ship_server/Ships/views.py#L183-L214)
* `get` 메서드로 요청이 들어오면 DB에 등록된 모든 선박의 좌표 값을 응답으로 보내줌.
* `post` 메서드로 요청이 들어오면 Body 를 통해 받은 클라이언트의 현재 위치 좌표를 기준으로 정해진 scope 범위 안에 있는 선박 데이터들을 필터링 하여 응답으로 보내줌.

`ListImageAPI` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/d9de7fb485c0efd5c6b1b93dcd6e9ab9b4fcd584/ship_server/Ships/views.py#L404-L417)
* id 값을 이용하여 해당 선박의 모든 이미지들을 가져와서 응답으로 보내줌.

`ImageAPI` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/d9de7fb485c0efd5c6b1b93dcd6e9ab9b4fcd584/ship_server/Ships/views.py#L420-L459)
* `post` 메서드로 요청이 들어오면 Body 에 담긴 id 값을 이용하여 해당 선박에 multipart 로 받은 이미지 데이터를 추가해줌.
* 이미지를 한장 씩 받아서 추가하면 클라이언트에서는 여러장을 요청했을 때 등록이 완료된 이미지의 개수를 알 수 있으므로 등록 상태를 체크할 수 있음.
* `delete` 메서드로 요청이 들어오면 해당 id 값을 가진 이미지 데이터를 DB 에서 제거.
* 추가적으로 선박별로 소유중인 이미지 개수가 있으므로 이미지 개수를 줄이는 작업이 필요.
* 메인 이미지가 제거되었을 때 자동으로 다음 이미지가 메인 이미지가 되야 하는 로직 추가.

`ChangeMainImageAPI` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/d9de7fb485c0efd5c6b1b93dcd6e9ab9b4fcd584/ship_server/Ships/views.py#L462-L476)
* 선박의 대표 이미지를 클라이언트에서 선택한 이미지로 변경해주는 API.

`PredictShipAPI` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/d9de7fb485c0efd5c6b1b93dcd6e9ab9b4fcd584/ship_server/Ships/views.py#L555-L610)
* multipart 로 이미지로 받고 해당 이미지를 서버 로컬 저장소에 저장하며 저장하는 이유는 추후에 해당 사진들을 통해 모델을 테스트할 때 유용할 수 있따고 판단.
* `ai_module`을 이용하여 해당 이미지의 확률 값이 담긴 리스트를 리턴받고 `best_three` 를 통해 확률이 제일 높은 3가지 id 값을 가져옴.
* 리턴 받은 id 값들을 이용하여 DB 에서 필터링 후 해당 선박에 대한 데이터 가져오기.
* 결과로 나온 선박들이 일반 선박이거나 유기 선박일 수 있으므로 해당 문제를 인지하고 로직을 작성.

`OwnerInfoAPI` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/d9de7fb485c0efd5c6b1b93dcd6e9ab9b4fcd584/ship_server/Ships/views.py#L613-L648)
* `get` 메서드로 요청이 들어오면 선박 id 값을 통해 해당 선박의 Owner 정보를 가져와서 응답으로 보내줌.
* `post` 메서드로 요청이 들어오면 선박 id 값을 통해 해당 선박의 Owner 정보를 Body 로 받은 데이터로 수정해줌.

`CreateOwnerAPI` [Code](https://github.com/KangJuSeong/shipCheck_server/blob/d9de7fb485c0efd5c6b1b93dcd6e9ab9b4fcd584/ship_server/Ships/views.py#L651-L666)
* Body 를 통해 받은 데이터와 multipart 로 받은 이미지를 이용하여 해당 선박의 선주 정보를 생성.

## 7. 배포
* 클라우드 서버에 Django 프로젝트 업로드.
* `NginX` 와 `Gunicorn`을 이용하여 서버 개방.
* 약 250명의 유저 사용.

## 8. 해결해야할 문제점
- 선박 학습에 대한 유지보수
    1. 선박은 하루에 10척 이상씩 꾸준히 등록되고 있음.
    2. 그에 따른 선박 학습의 자동화가 필요.
    3. 현재는 관리자가 주 단위로 선박 등록 현황을 파악하고 일정 데이터 수집이 완료된 선박을 추려서 학습을 진행. [선박 학습 프로그램](https://github.com/KangJuSeong/Ship_Classification_Program)
    