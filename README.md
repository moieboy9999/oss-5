# OSS4 - Docker FastAPI Courses Assignment

## 학생 정보

- 학번: 2025404027
- 이름: 최세영

## 과제 설명

FastAPI로 구현한 `courses` 프로그램을 Docker 컨테이너로 실행하는 과제입니다.

이번 버전은 `docker compose`를 사용하지 않습니다.

사용하는 방식:

```powershell
docker build
docker run
```

과제 조건에 맞게 외부 포트는 `80`, 컨테이너 내부 FastAPI 포트는 `8000`을 사용합니다.

---

## 1. 프로젝트 파일 구성

```text
oss4_courses_docker_run_assignment/
├── main.py
├── courses.json
├── requirements.txt
├── Dockerfile
├── README.md
├── report.md
├── demo_script.md
├── run_windows.ps1
└── .gitignore
```

`docker-compose.yml`은 사용하지 않으므로 포함하지 않았습니다.

---

## 2. Windows에서 압축 풀기

예시 경로:

```text
C:\Users\david\OneDrive\desktop\광\2학\OSS\oss-6
```

PowerShell에서 프로젝트 폴더로 이동합니다.

```powershell
cd "C:\Users\david\OneDrive\desktop\광\2학\OSS\oss-6"
```

현재 폴더에 `Dockerfile`, `main.py`, `requirements.txt`가 있는지 확인합니다.

```powershell
dir
```

---

## 3. Docker 설치 확인

PowerShell에서 아래 명령어를 실행합니다.

```powershell
docker --version
```

정상 예시:

```text
Docker version 27.x.x, build ...
```

만약 아래처럼 나오면 Docker Desktop이 설치되어 있지 않거나 실행 중이 아닌 상태입니다.

```text
docker : 'docker' 용어가 cmdlet, 함수, 스크립트 파일 또는 실행할 수 있는 프로그램 이름으로 인식되지 않습니다.
```

이 경우 Windows에 Docker Desktop을 설치하고 실행한 뒤 PowerShell을 다시 열어야 합니다.

---

## 4. Docker 이미지 빌드

`docker compose`를 쓰지 않고 직접 이미지를 빌드합니다.

```powershell
docker build -t courses-api .
```

의미:

- `docker build`: Dockerfile을 이용해 이미지 생성
- `-t courses-api`: 이미지 이름을 `courses-api`로 지정
- `.`: 현재 폴더의 Dockerfile 사용

이미지 확인:

```powershell
docker images
```

---

## 5. Docker 컨테이너 실행

과제 조건에 맞게 외부 포트 `80`을 사용하고, 재시작 정책은 `--restart always`로 적용합니다.

```powershell
docker run -d --name courses-api -p 80:8000 --restart always courses-api
```

의미:

- `-d`: 백그라운드 실행
- `--name courses-api`: 컨테이너 이름 지정
- `-p 80:8000`: Windows/EC2의 80번 포트를 컨테이너 내부 8000번 포트에 연결
- `--restart always`: Docker가 다시 시작되어도 컨테이너 자동 재시작
- `courses-api`: 실행할 이미지 이름

---

## 6. 실행 상태 확인

```powershell
docker ps
```

정상이라면 `courses-api` 컨테이너가 실행 중이어야 합니다.

예시:

```text
CONTAINER ID   IMAGE         COMMAND                  PORTS
xxxx           courses-api   "uvicorn main:app ..."   0.0.0.0:80->8000/tcp
```

---

## 7. 브라우저에서 확인

Windows 브라우저에서 아래 주소로 접속합니다.

```text
http://localhost/courses
```

또는 Swagger 문서 확인:

```text
http://localhost/docs
```

---

## 8. PowerShell에서 API 테스트

GET 테스트:

```powershell
curl.exe http://localhost/courses
```

POST 테스트:

```powershell
curl.exe -X POST "http://localhost/courses" -H "Content-Type: application/json" -d "{\"course_name\":\"Docker 실습\",\"year\":\"2026\",\"semester\":\"1\",\"grade\":\"A+\"}"
```

POST 후 다시 확인:

```powershell
curl.exe http://localhost/courses
```

---

## 9. 컨테이너 중지 및 삭제

실행 중지:

```powershell
docker stop courses-api
```

컨테이너 삭제:

```powershell
docker rm courses-api
```

이미지 삭제:

```powershell
docker rmi courses-api
```

다시 실행하려면:

```powershell
docker build -t courses-api .
docker run -d --name courses-api -p 80:8000 --restart always courses-api
```

---

## 10. 이미 같은 이름의 컨테이너가 있다고 나오는 경우

아래 오류가 나올 수 있습니다.

```text
Conflict. The container name "/courses-api" is already in use
```

이 경우 기존 컨테이너를 삭제하고 다시 실행합니다.

```powershell
docker stop courses-api
docker rm courses-api
docker run -d --name courses-api -p 80:8000 --restart always courses-api
```

---

## 11. 80번 포트가 이미 사용 중인 경우

아래와 비슷한 오류가 나올 수 있습니다.

```text
Bind for 0.0.0.0:80 failed: port is already allocated
```

과제는 외부 80번 포트가 조건이므로, 80번 포트를 쓰는 프로그램을 종료해야 합니다.

Windows에서 80번 포트 사용 확인:

```powershell
netstat -ano | findstr :80
```

PID 확인 후 작업 관리자에서 해당 프로그램을 종료합니다.

---

## 12. EC2 배포 방법

EC2에 접속합니다.

```powershell
ssh -i .\키파일.pem ubuntu@EC2_PUBLIC_IP
```

EC2 안에서 저장소를 받습니다.

```bash
git clone https://github.com/moieboy9999/oss4.git
cd oss4
```

Docker 설치 확인:

```bash
docker --version
```

Docker가 없다면 설치:

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker
```

이미지 빌드:

```bash
sudo docker build -t courses-api .
```

컨테이너 실행:

```bash
sudo docker run -d --name courses-api -p 80:8000 --restart always courses-api
```

실행 확인:

```bash
sudo docker ps
```

브라우저에서 확인:

```text
http://EC2_PUBLIC_IP/courses
```

또는:

```text
http://EC2_PUBLIC_IP/docs
```

---

## 13. EC2에서 다시 실행해야 하는 경우

기존 컨테이너 삭제:

```bash
sudo docker stop courses-api
sudo docker rm courses-api
```

다시 빌드 및 실행:

```bash
sudo docker build -t courses-api .
sudo docker run -d --name courses-api -p 80:8000 --restart always courses-api
sudo docker ps
```

---

## 14. 제출 영상에 포함할 내용

영상에는 아래 내용이 들어가야 합니다.

1. EC2 터미널 화면
2. `sudo docker ps` 실행 결과
3. 브라우저에서 `http://EC2_PUBLIC_IP/courses` 접속
4. FastAPI 결과 JSON 출력 화면
5. 필요 시 `http://EC2_PUBLIC_IP/docs` Swagger 화면

---

## 15. 제출물

제출물:

1. GitHub repository 주소
2. YouTube 데모 영상 링크
