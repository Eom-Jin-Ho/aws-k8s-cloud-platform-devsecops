# DAY1 - AWS EC2 환경 구축 및 Docker 기반 Flask API 실행

---

# 1. DAY1 목표

DAY1의 목표는 AWS EC2 환경을 구축하고 Docker 기반 컨테이너 환경을 구성한 뒤 Flask API를 Docker Container에서 실행하는 것이다.

또한 Remote SSH 기반 개발 환경을 구축하여 Windows와 EC2를 GitHub를 중심으로 연동하는 개발 환경을 구성하는 것을 목표로 한다.

---

# 2. DAY1 완료 목표

- AWS EC2 생성
- Remote SSH 환경 구축
- Docker 공식 Repository 등록
- Docker Engine 설치
- Docker 권한 설정
- Flask API 작성
- Docker Image 생성
- Docker Container 실행
- Flask API 외부 접속 확인

---

# 3. 구축 환경

| 항목 | 내용 |
|------|------|
| Cloud | AWS EC2 |
| OS | Ubuntu 24.04 LTS |
| IDE | VS Code Remote SSH |
| Container | Docker CE 29.x |
| Language | Python 3.12 |
| Framework | Flask 3.1 |
| SCM | Git / GitHub |

---

# 4. 전체 아키텍처

```text
Windows (VS Code)

        │

Remote SSH

        │

AWS EC2 (Ubuntu)

        │

Docker Engine

        │

Flask Container

        │

Port Mapping (5000)

        │

Browser
```

---

# 5. DAY1에서 구현한 기능

- AWS EC2 인스턴스 생성
- Remote SSH를 이용한 원격 개발 환경 구축
- Docker 공식 Repository 등록
- Docker Engine 설치
- Docker 권한 설정
- Flask API 개발
- Dockerfile 작성
- Docker Image 생성
- Docker Container 실행
- EC2 Public IP를 이용한 Flask API 접속 확인

---

# 6. 프로젝트 디렉터리

```text
aws-k8s-cloud-platform-devsecops

├── app
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── k8s
├── argocd
├── monitoring
├── docs
│
└── README.md
```

# 7. 구축 과정

DAY1에서는 AWS EC2 환경을 기반으로 Docker 공식 Repository를 등록하고 Docker Engine을 설치하였다.

이후 Flask 애플리케이션을 개발한 뒤 Dockerfile을 이용하여 Docker Image를 생성하고, Docker Container를 실행하여 외부 브라우저에서 정상적으로 접속되는 것까지 확인하였다.

구축 과정은 실제 수행 순서에 따라 작성하였으며, 각 단계마다 수행 목적, 사용 명령어, 결과 및 실무적인 고려사항을 함께 정리하였다.

---

## 7-1. 현재 작업 디렉터리 확인

### 배경

Remote SSH를 이용하여 EC2(Ubuntu)에 접속한 후 프로젝트를 진행하기 전에 현재 작업 위치를 먼저 확인하였다.

Linux는 현재 작업 디렉터리를 기준으로 상대경로를 사용하므로 작업 위치를 확인하는 과정이 필요하였다.

---

### 목적

현재 작업 중인 디렉터리를 확인하고 프로젝트 전용 작업 디렉터리를 생성하기 위한 기준 위치를 확인한다.
---

### Why?

프로젝트마다 작업 디렉터리를 분리하면 관리가 쉬워지고 다른 프로젝트와 충돌을 방지할 수 있다.

---

### 사용 명령어

```bash
pwd
```

---

### 명령어 설명

현재 작업 중인 디렉터리(Working Directory)의 절대 경로를 출력하는 명령어이다.

---

### 실행 결과

```text
/home/ubuntu
```

---

### 결과 분석

현재 로그인한 사용자의 Home Directory에서 작업을 시작한 것을 확인하였다.

이후 프로젝트 관리를 위해 `/home/ubuntu/projects` 디렉터리를 생성하여 별도의 프로젝트 공간에서 작업을 진행하였다.

---

### 학습 포인트

- Linux는 현재 작업 위치를 기준으로 상대경로를 해석한다.
- 프로젝트는 Home Directory보다 별도의 작업 디렉터리에서 관리하는 것이 좋다.
- pwd는 SSH 접속 후 가장 먼저 실행하는 기본 명령어 중 하나이다.

---

### 캡처

![alt text](<1. pwd - 현재 작업 디렉터리 확인.jpg>)

---


### 실무 TIP

SSH 접속 후 가장 먼저 `pwd`를 실행하여 현재 위치를 확인하는 습관을 가지는 것이 좋다.

---

### 운영 시 고려사항

프로젝트를 Home Directory에서 직접 관리하기보다는 프로젝트 전용 디렉터리를 생성하여 관리하는 것이 유지보수와 백업 측면에서 유리하다.

---

## 7-2. 패키지 목록 최신화

### 목적

Docker 설치 전에 Ubuntu 패키지 저장소의 최신 목록(Index)을 가져오기 위해 수행하였다.


---

### Why?

오래된 패키지 목록을 사용하면 최신 Docker Engine이 아닌 이전 버전이 설치될 수 있기 때문이다.

---


### 사용 명령어

```bash
sudo apt update
```

---

### 명령어 설명

APT 저장소의 최신 패키지 목록을 다운로드하는 명령어이다.

패키지를 실제로 업그레이드하는 것이 아니라 설치 가능한 최신 목록만 갱신한다.

---

### 실행 결과

패키지 저장소와 정상적으로 통신하였으며 Docker Repository 등록을 위한 최신 패키지 목록을 확보하였다.

---

### 캡처

![alt text](<2. sudo apt update - 패키지 목록 최신화.jpg>)



---

### 실무 TIP

Linux 서버 구축 시 `apt update`를 먼저 수행한 후 필요한 패키지를 설치하는 것이 일반적인 절차이다.

---

### 운영 시 고려사항

`apt update`와 `apt upgrade`는 서로 다른 명령어이다.

- update : 패키지 목록(Index) 갱신
- upgrade : 설치된 패키지 실제 업데이트

---


## 7-3. Docker 설치를 위한 필수 패키지 설치

### 배경

Docker 공식 Repository를 등록하기 위해서는 HTTPS 통신과 GPG Key 검증에 필요한 패키지가 먼저 설치되어 있어야 한다.

Ubuntu 기본 설치 환경에서는 일부 패키지가 존재하지 않을 수 있으므로 Docker 설치 전에 필수 패키지를 먼저 설치하였다.

---

### 목적

Docker 공식 Repository를 등록하기 위한 필수 패키지를 설치한다.

---

### Why?

Docker는 Ubuntu 기본 저장소가 아닌 Docker 공식 Repository를 사용하여 설치할 예정이다.

공식 Repository를 사용하기 위해서는 HTTPS 통신과 GPG Key 검증 기능이 필요하므로 관련 패키지를 먼저 설치하였다.

---

### 사용 명령어

```bash
sudo apt install -y ca-certificates curl gnupg lsb-release
```

---

### 명령어 설명

Docker 공식 Repository를 등록하기 위해 필요한 패키지를 설치하는 명령어이다.

- **ca-certificates** : HTTPS 인증서를 검증하기 위한 패키지
- **curl** : 웹에서 파일이나 데이터를 다운로드하는 프로그램
- **gnupg** : GPG Key를 관리하는 프로그램
- **lsb-release** : 현재 Ubuntu 배포판 정보를 확인하는 프로그램

---

### 실행 결과

필수 패키지가 정상적으로 설치되었으며 Docker 공식 Repository 등록을 위한 사전 준비가 완료되었다.

설치 과정에서 `ca-certificates` 관련 Warning이 발생하였으나 Docker 설치에는 영향을 주지 않는 일반적인 Warning임을 확인하였다.

---

### 결과 분석

Docker 공식 Repository를 사용하기 위한 기반 환경이 구성되었다.

이후 Docker GPG Key 등록 및 Repository 등록을 진행할 수 있는 상태가 되었다.

---

### 학습 포인트

- Docker 공식 Repository를 사용하기 위해서는 HTTPS와 GPG 검증 환경이 필요하다.
- Docker 설치는 단순히 패키지를 설치하는 것이 아니라 저장소를 신뢰하는 과정부터 시작된다.
- Ubuntu 기본 저장소보다 Docker 공식 Repository를 사용하는 것이 최신 기능과 안정성을 확보하는 데 유리하다.

---

### 캡처

![alt text](<3. sudo apt install -y ca-certificates curl gnupg lsb-release.jpg>)
---

### 실무 TIP

Docker를 설치할 때는 Ubuntu 기본 저장소의 `docker.io`보다 Docker 공식 Repository를 사용하는 것이 일반적이다.

최신 Docker Engine과 Buildx, Compose Plugin 등을 사용할 수 있기 때문이다.

---

### 운영 시 고려사항

패키지 설치 과정에서 Warning이 발생하더라도 실제 Docker 설치와 관련 없는 Warning인지 반드시 확인해야 한다.

모든 Warning이 오류를 의미하는 것은 아니므로 로그를 분석하는 습관이 중요하다.



## 7-4. Docker 공식 Repository 저장 디렉터리 생성

### 배경

Docker는 Ubuntu 기본 저장소가 아닌 Docker 공식 Repository를 사용하여 설치하기로 결정하였다.

공식 Repository를 등록하기 위해서는 Docker에서 제공하는 GPG Key를 저장할 디렉터리가 필요하였다.

Ubuntu에서는 `/etc/apt/keyrings` 디렉터리에 Repository의 GPG Key를 저장하는 방식을 권장하고 있다.

---

### 목적

Docker GPG Key를 저장하기 위한 디렉터리를 생성한다.

---

### Why?

Docker 공식 Repository를 등록하기 위해서는 Docker에서 제공하는 GPG Key를 저장해야 한다.

Ubuntu는 저장소의 무결성과 신뢰성을 검증하기 위해 GPG Key를 사용하며, 이를 저장할 전용 디렉터리가 필요하다.

---

### 사용 명령어

```bash
sudo install -m 0755 -d /etc/apt/keyrings
```

---

### 명령어 설명

`install` 명령어를 이용하여 `/etc/apt/keyrings` 디렉터리를 생성하였다.

옵션 설명은 다음과 같다.

| 옵션 | 설명 |
|------|------|
| `-m 0755` | 디렉터리 권한을 755로 설정 |
| `-d` | 디렉터리를 생성 |
| `/etc/apt/keyrings` | Docker GPG Key 저장 위치 |

---

### 실행 결과

Docker GPG Key를 저장할 `/etc/apt/keyrings` 디렉터리가 정상적으로 생성되었다.

명령어 실행 후 별도의 출력 메시지는 없었으며, Linux에서는 정상적으로 수행된 경우 출력 없이 종료되는 경우가 많다.

---

### 결과 분석

Docker Repository를 신뢰하기 위한 준비 단계가 완료되었다.

이후 Docker에서 제공하는 GPG Key를 해당 디렉터리에 저장하여 공식 Repository를 등록할 수 있는 상태가 되었다.

---

### 학습 포인트

- Linux에서는 성공적으로 수행된 명령어가 별도의 출력 없이 종료되는 경우가 많다.
- Docker 공식 Repository는 GPG Key를 이용하여 패키지의 신뢰성을 검증한다.
- `/etc/apt/keyrings`는 외부 Repository의 GPG Key를 저장하는 표준 위치이다.

---

### 캡처

![alt text](<4. sudo install -m 0755 -d etc apt keyrings.jpg>)

---

### 실무 TIP

최근 Ubuntu에서는 Repository의 GPG Key를 `/etc/apt/keyrings` 디렉터리에 저장하는 방식을 권장한다.

예전 방식인 `apt-key`는 현재 Deprecated(사용 중단 예정) 상태이므로 신규 서버 구축 시에는 사용하지 않는 것이 좋다.

---

### 운영 시 고려사항

Linux 권한 설정은 보안과 직접 연결된다.

특히 Repository Key, SSH Key, Secret 파일은 적절한 권한을 유지해야 하며, 불필요하게 넓은 권한을 부여하지 않도록 주의해야 한다.


## 7-5. Docker GPG Key 등록

### 배경

Docker는 Ubuntu 기본 저장소가 아닌 Docker 공식 Repository를 사용하여 설치하기로 결정하였다.

공식 Repository에서 제공하는 패키지가 신뢰할 수 있는지 검증하기 위해 Docker에서 제공하는 GPG Key를 Ubuntu에 등록하는 과정이 필요하였다.

---

### 목적

Docker 공식 Repository의 GPG Key를 등록하여 패키지의 무결성과 신뢰성을 검증한다.

---

### Why?

Ubuntu는 외부 저장소에서 패키지를 다운로드할 때 해당 저장소가 신뢰할 수 있는지 확인하기 위해 GPG Key를 사용한다.

Docker GPG Key를 등록하면 Docker에서 제공하는 패키지가 위·변조되지 않았음을 검증할 수 있다.

---

### 사용 명령어

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

---

### 명령어 설명

Docker에서 제공하는 GPG Key를 다운로드한 뒤 Ubuntu에서 사용할 수 있는 Binary Keyring 형식으로 변환하여 저장한다.

| 명령어 | 역할 |
|--------|------|
| curl | Docker GPG Key 다운로드 |
| -fsSL | 오류 처리, Silent Mode, Redirect 허용 |
| \| (Pipe) | 다운로드 결과를 다음 명령어로 전달 |
| gpg --dearmor | Binary Keyring 형식으로 변환 |
| -o | 결과를 지정한 파일로 저장 |

---

### 실행 결과

Docker GPG Key가 `/etc/apt/keyrings/docker.gpg` 파일로 정상 등록되었다.

명령어 실행 후 별도의 출력은 없었으며, 정상적으로 종료되었다.

---

### 결과 분석

Docker 공식 Repository를 신뢰할 수 있는 저장소로 등록하기 위한 핵심 과정이 완료되었다.

이후 Docker Repository를 Ubuntu에 등록하여 최신 Docker Engine을 설치할 수 있는 환경이 구성되었다.

---

### 학습 포인트

- Ubuntu는 외부 저장소의 패키지를 GPG Key로 검증한다.
- GPG Key를 등록하면 패키지의 무결성과 출처를 확인할 수 있다.
- Pipe(`|`)는 앞 명령어의 출력을 뒤 명령어의 입력으로 전달한다.
- `--dearmor`는 ASCII 형식의 GPG Key를 Binary Keyring으로 변환한다.

---

### 캡처

![alt text](<5. Docker GPG Key 등록.jpg>)

---

### 실무 TIP

Docker뿐 아니라 HashiCorp, Kubernetes, Grafana 등 대부분의 공식 Repository도 동일한 방식으로 GPG Key를 등록한다.

공식 Repository를 사용할 때는 반드시 GPG Key를 등록하여 신뢰성을 검증하는 것이 좋다.

---

### 운영 시 고려사항

GPG Key는 저장소의 신뢰성을 보장하는 중요한 요소이다.

공식 Repository가 아닌 출처가 불분명한 GPG Key를 등록하면 악성 패키지가 설치될 위험이 있으므로 반드시 공식 사이트에서 제공하는 Key만 사용해야 한다.



## 7-6. Docker 공식 Repository 등록

### 배경

Docker GPG Key를 등록한 후 Ubuntu가 Docker 공식 Repository를 인식할 수 있도록 저장소 정보를 추가하였다.

Ubuntu는 Repository 정보를 기반으로 패키지 목록(Index)을 관리하므로 Docker Repository를 등록해야 최신 Docker Engine을 설치할 수 있다.

---

### 목적

Ubuntu 패키지 관리자(APT)에 Docker 공식 Repository를 등록한다.

---

### Why?

Ubuntu 기본 저장소의 Docker 패키지는 최신 버전보다 오래된 경우가 많다.

이번 프로젝트에서는 최신 Docker Engine과 Buildx, Compose Plugin 등을 사용하기 위해 Docker 공식 Repository를 사용하였다.

---

### 사용 명령어

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

---

### 명령어 설명

Docker 공식 Repository 정보를 Ubuntu APT 저장소 목록에 추가하는 명령어이다.

| 명령어 | 역할 |
|--------|------|
| echo | Repository 정보를 출력 |
| dpkg --print-architecture | CPU 아키텍처 확인 (amd64 등) |
| tee | 출력 내용을 파일에 저장 |
| /etc/apt/sources.list.d/docker.list | Docker Repository 목록 파일 |
| /dev/null | 불필요한 출력 제거 |

---

### 실행 결과

Docker Repository가 Ubuntu 저장소 목록에 정상적으로 등록되었다.

등록 후 `apt update`를 실행하면 Docker 공식 Repository의 최신 패키지 목록을 다운로드할 수 있는 상태가 되었다.

---

### 결과 분석

Ubuntu는 Docker Repository를 새로운 패키지 저장소로 인식하게 되었으며 이후 최신 Docker Engine 설치가 가능해졌다.

---

### 학습 포인트

- Ubuntu는 `/etc/apt/sources.list.d/` 디렉터리에 저장된 Repository 목록을 관리한다.
- Docker Repository는 Ubuntu 기본 저장소와 별도로 관리된다.
- `tee` 명령어는 Root 권한이 필요한 파일을 생성하거나 수정할 때 자주 사용된다.
- `/dev/null`은 출력 결과를 버리는 Linux의 특수 파일이다.

---

### 캡처

![alt text](<6. Docker 공식 Repository 등록.jpg>)

---

### 실무 TIP

외부 Repository를 등록한 후에는 반드시 `sudo apt update`를 다시 수행해야 한다.

새로운 저장소를 등록했다고 해서 Ubuntu가 자동으로 최신 패키지 목록을 가져오지는 않는다.

---

### 운영 시 고려사항

외부 Repository는 반드시 공식 사이트에서 제공하는 주소만 사용해야 한다.

출처가 불분명한 Repository를 등록하면 악성 패키지가 설치될 위험이 있다.

---

### 관련 기술

- APT Repository
- Linux Package Management
- tee
- /dev/null
- dpkg



## 7-7. Docker Repository 패키지 목록 갱신

### 배경

Docker 공식 Repository를 Ubuntu에 등록하였지만, Ubuntu는 아직 새롭게 등록된 저장소의 패키지 목록(Index)을 가지고 있지 않은 상태였다.

새로운 Repository를 등록한 후에는 반드시 패키지 목록을 다시 다운로드해야 Docker에서 제공하는 최신 패키지를 설치할 수 있다.

---

### 목적

Docker 공식 Repository의 최신 패키지 목록(Index)을 다운로드한다.

---

### Why?

Repository를 등록했다고 해서 Ubuntu가 자동으로 최신 패키지 목록을 가져오는 것은 아니다.

새로운 Repository를 등록한 후 `apt update`를 다시 수행해야 Ubuntu가 Docker 공식 Repository를 인식하고 최신 Docker Engine 패키지를 검색할 수 있다.

---

### 사용 명령어

```bash
sudo apt update
```

---

### 명령어 설명

APT 저장소의 최신 패키지 목록(Index)을 다시 다운로드하는 명령어이다.

이번 `apt update`는 Docker Repository가 추가된 이후 수행되므로 Docker 공식 저장소의 패키지 정보도 함께 가져오게 된다.

---

### 실행 결과

Docker 공식 Repository에서 최신 패키지 목록을 정상적으로 다운로드하였다.

아래와 같은 로그를 통해 Docker Repository가 정상적으로 인식된 것을 확인하였다.

```text
Hit: https://download.docker.com/linux/ubuntu ...
```

---

### 결과 분석

Ubuntu가 Docker Repository를 정상적으로 인식하였다.

이후 Docker Engine을 Docker 공식 Repository를 통해 설치할 수 있는 환경이 완성되었다.

---

### 학습 포인트

- Repository 등록과 패키지 목록 갱신은 서로 다른 과정이다.
- 새로운 Repository를 등록한 후에는 반드시 `apt update`를 다시 수행해야 한다.
- Ubuntu는 `apt update`를 통해 저장소 목록(Index)을 관리한다.

---

### 캡처

![alt text](<7. Docker Repository 패키지 목록 갱신.jpg>)

---

### 명령어 실행 흐름

```text
Docker Repository 등록
        │
        ▼
APT Repository 목록 변경
        │
        ▼
sudo apt update
        │
        ▼
Docker Repository Index 다운로드
        │
        ▼
최신 Docker Engine 설치 가능
```

---

### 실무 TIP

새로운 Repository를 추가한 후 `apt update`를 수행하지 않으면 Ubuntu는 해당 저장소의 최신 패키지를 검색하지 못한다.

실무에서도 Repository 등록 후 `apt update`는 거의 항상 함께 수행된다.

---

### 운영 시 고려사항

패키지 목록을 갱신한 후에는 Docker Repository 관련 로그가 정상적으로 출력되는지 반드시 확인하는 것이 좋다.

Repository 주소 오류나 GPG Key 오류가 있는 경우 이 단계에서 대부분 확인할 수 있다.

---

### 관련 기술

- APT Index
- Package Repository
- Docker Repository
- Linux Package Manager


## 7-8. Docker Engine 설치

### 배경

Docker 공식 Repository를 등록하고 최신 패키지 목록(Index)을 갱신한 후 Docker Engine을 설치하였다.

Ubuntu 기본 저장소의 `docker.io` 대신 Docker 공식 Repository에서 제공하는 `docker-ce`를 사용하여 최신 기능과 공식 지원 버전을 적용하였다.

---

### 목적

Docker Engine을 설치하여 컨테이너 기반 애플리케이션을 실행할 수 있는 환경을 구축한다.

---

### Why?

Ubuntu 기본 저장소의 `docker.io` 패키지는 Docker 공식 릴리스보다 버전이 오래된 경우가 많다.

이번 프로젝트에서는 최신 Docker Engine과 Buildx, Compose Plugin 등을 사용하기 위해 Docker 공식 Repository의 `docker-ce`를 선택하였다.

---

### 사용 명령어

```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

---

### 명령어 설명

Docker 실행 환경을 구성하는 핵심 구성 요소를 설치하는 명령어이다.

| 패키지 | 역할 |
|---------|------|
| docker-ce | Docker Engine |
| docker-ce-cli | Docker CLI |
| containerd.io | Container Runtime |
| docker-buildx-plugin | Buildx Plugin |
| docker-compose-plugin | Docker Compose Plugin |

---

### 실행 결과

Docker Engine과 Docker 관련 패키지가 정상적으로 설치되었다.

설치 과정에서 Docker Service가 systemd에 등록되었으며 운영체제 부팅 시 자동으로 Docker Daemon이 실행되는 환경이 구성되었다.

---

### 결과 분석

Docker Engine 설치가 완료되면서 Docker Image 생성(Build), Docker Container 실행(Run), Docker Networking 등의 기능을 사용할 수 있는 상태가 되었다.

이후 Flask 애플리케이션을 Docker Container에서 실행하기 위한 기반 환경이 완성되었다.

---

### 학습 포인트

- Docker Engine은 실제 컨테이너를 실행하는 핵심 프로그램이다.
- Docker CLI는 사용자가 입력하는 docker 명령어를 처리한다.
- containerd는 Docker와 Kubernetes에서 사용하는 Container Runtime이다.
- Docker Compose는 여러 개의 컨테이너를 하나의 프로젝트로 관리할 수 있다.
- Docker Buildx는 Multi-Platform 이미지를 생성할 수 있는 Docker Build 기능이다.

---

### 캡처

![alt text](<8. Docker Engine 설치.jpg>)

---

### 명령어 실행 흐름

```text
Docker Repository

        │

        ▼

Docker Engine 설치

        │

        ▼

Docker CLI 설치

        │

        ▼

containerd 설치

        │

        ▼

Docker Service 등록

        │

        ▼

Docker 사용 가능
```

---

### 실무 TIP

Ubuntu 기본 저장소의 `docker.io`보다 Docker 공식 Repository의 `docker-ce`를 사용하는 것이 일반적이다.

Docker Buildx, Compose Plugin 등 최신 기능을 사용할 수 있으며 Docker 공식 지원을 받을 수 있다.

---

### 운영 시 고려사항

Docker Engine 설치 후에는 반드시 다음 항목을 확인하는 것이 좋다.

- Docker Service 정상 실행 여부
- Docker Version
- Docker Info
- Docker 권한(docker 그룹)

이후 테스트 이미지를 실행하여 Docker Engine이 정상적으로 동작하는지 검증한다.

---

### 관련 기술

- Docker Engine
- Docker CLI
- Container Runtime
- containerd
- Docker Buildx
- Docker Compose
- systemd


## 7-9. Docker 권한 설정 및 Docker Daemon 접근 문제 해결

### 배경

Docker Engine 설치 후 `docker version` 명령어를 실행하였으나 `permission denied while trying to connect to the Docker daemon socket` 오류가 발생하였다.

Docker는 정상적으로 설치되어 있었지만 현재 로그인한 사용자가 Docker Daemon에 접근할 권한이 없어 Docker CLI와 Docker Engine이 통신하지 못하는 상태였다.

---

### 목적

Docker Daemon에 접근할 수 있도록 현재 사용자를 docker 그룹에 추가하고 정상적으로 Docker 명령어를 사용할 수 있도록 구성한다.

---

### Why?

Docker는 일반 사용자가 직접 Docker Daemon을 제어하지 못하도록 Linux Group Permission을 이용하여 접근 권한을 관리한다.

현재 사용자인 `ubuntu`는 docker 그룹에 포함되어 있지 않았기 때문에 Docker Socket(`/var/run/docker.sock`)에 접근할 수 없었다.

---

### 사용 명령어

```bash
sudo usermod -aG docker ubuntu

newgrp docker

groups

docker version
```

---

### 명령어 설명

| 명령어 | 설명 |
|---------|------|
| usermod | 사용자 그룹 수정 |
| -aG | 기존 그룹을 유지하면서 docker 그룹 추가 |
| newgrp | 현재 Shell에 새로운 그룹 적용 |
| groups | 현재 사용자의 그룹 확인 |
| docker version | Docker Engine 정상 동작 확인 |

---

### 실행 결과

처음에는 Docker Daemon 접근 권한이 없어 `permission denied` 오류가 발생하였다.

`ubuntu` 사용자를 docker 그룹에 추가하고 `newgrp docker`를 실행한 후 Docker Client와 Docker Server가 정상적으로 통신하는 것을 확인하였다.

---

### 결과 분석

Docker는 CLI와 Docker Daemon이 Unix Socket(`/var/run/docker.sock`)을 통해 통신한다.

사용자가 docker 그룹에 속하지 않으면 해당 Socket에 접근할 수 없기 때문에 Docker 명령어 실행이 실패한다.

권한을 부여한 이후에는 일반 사용자 권한으로도 Docker 명령어를 사용할 수 있게 되었다.

---

### 학습 포인트

- Docker CLI와 Docker Engine은 Unix Socket으로 통신한다.
- Docker Socket은 `/var/run/docker.sock` 파일을 사용한다.
- Linux에서는 Group Permission을 이용하여 Docker 접근 권한을 관리한다.
- `newgrp`는 현재 Shell에 새로운 Group을 즉시 적용한다.

---

### 캡처

![alt text](<9-1. docker version - Docker 설치 확인.jpg>)

![alt text](<9-2. docker version - Docker Client,Server 확인 Trouble Shooting.jpg>)

---

### 명령어 실행 흐름

```text
Docker Engine 설치

        │

        ▼

docker version 실행

        │

        ▼

Permission Denied 발생

        │

        ▼

ubuntu → docker 그룹 추가

        │

        ▼

newgrp docker

        │

        ▼

Docker Client ↔ Docker Server 연결 성공
```

---

### 실무 TIP

Docker 설치 후 가장 먼저 확인해야 하는 항목은 Docker Daemon과 정상적으로 통신하는지 여부이다.

Docker 권한 문제는 Linux 환경에서 가장 자주 발생하는 Docker 초기 설정 문제 중 하나이다.

---

### 운영 시 고려사항

`sudo usermod -aG docker`를 수행한 후에는 현재 로그인 세션에는 바로 반영되지 않을 수 있다.

실무에서는 다음 중 하나를 수행한다.

- `newgrp docker`
- SSH 재접속
- 로그아웃 후 재로그인

---

### 관련 기술

- Docker Daemon
- Docker CLI
- docker.sock
- Linux Group Permission
- Unix Socket

### 실제 문제 해결 과정

1. docker version 실행
2. permission denied 발생
3. docker 그룹 확인
4. usermod로 그룹 추가
5. newgrp docker 적용
6. docker version 재확인
7. Docker Client / Server 정상 연결 확인


## 7-10. Flask API 실행 및 Docker Container 검증

### 배경

Docker Image 생성이 완료된 후 Flask 애플리케이션이 정상적으로 실행되는지 확인하기 위해 Docker Container를 실행하였다.

또한 Docker Container가 정상적으로 동작하는지 확인하고 EC2 외부에서 Flask API에 접근 가능한지 검증하였다.

---

### 목적

Docker Image를 기반으로 Docker Container를 실행하고 Flask API가 정상적으로 서비스되는지 확인한다.

---

### Why?

Docker Image는 실행 가능한 템플릿일 뿐 실제 서비스는 제공하지 않는다.

실제 서비스를 제공하기 위해서는 Docker Image를 기반으로 Container를 생성하고 실행해야 한다.

---

### 사용 명령어

```bash
docker run -d \
--name flask-api \
-p 5000:5000 \
flask-api:v1

docker ps

docker logs flask-api
```

---

### 명령어 설명

| 명령어 | 설명 |
|---------|------|
| docker run | Docker Container 실행 |
| -d | 백그라운드 실행(Detached Mode) |
| --name | Container 이름 지정 |
| -p 5000:5000 | Host와 Container 포트 연결 |
| docker ps | 실행 중인 Container 확인 |
| docker logs | Container 로그 확인 |

---

### 실행 결과

Docker Image를 기반으로 Flask Container가 정상적으로 실행되었다.

`docker ps` 명령을 통해 Container 상태가 `Up`인 것을 확인하였으며 Host의 5000 포트와 Container의 5000 포트가 정상적으로 연결된 것을 확인하였다.

이후 EC2 Public IP를 이용하여 Flask API에 정상적으로 접근되는 것을 확인하였다.

---

### 결과 분석

Docker Engine은 Flask Image를 기반으로 새로운 Container를 생성하였다.

Container 내부에서 Flask API가 실행되었으며 Port Mapping을 통해 EC2 외부에서도 서비스에 접근할 수 있었다.

이를 통해 Docker Image → Docker Container → 외부 서비스 제공까지의 전체 흐름을 확인하였다.

---

### 학습 포인트

- Docker Image는 실행 가능한 템플릿이다.
- Docker Container는 Docker Image를 실행한 실제 프로세스이다.
- `docker run`은 Image를 기반으로 새로운 Container를 생성한다.
- `docker ps`는 실행 중인 Container를 확인한다.
- `docker logs`는 Container 내부 로그를 확인한다.
- Port Mapping을 통해 Host와 Container를 연결할 수 있다.

---

### 캡처

#### 그림 13. Docker Image 생성

![alt text](<13. Docker Image 생성.jpg>)

#### 그림 14. Docker Image 확인

![alt text](<14. Docker Image 확인.jpg>)

#### 그림 15. Flask Container 실행

![alt text](<15. Flask Container 실행.jpg>)

#### 그림 16. Docker Container 상태 확인

![alt text](<16. Docker Container 확인.jpg>)

#### 그림 17. Flask API 정상 동작 확인
alt text

#### 그림 18. Docker Container 로그 확인

![alt text](<18. Docker Container 로그 확인.jpg>)

---

### 명령어 실행 흐름

```text
Dockerfile

        │

docker build

        │

Docker Image

        │

docker run

        │

Docker Container

        │

Port Mapping

        │

Browser

        │

Flask API 응답
```

---

### 실무 TIP

Container 실행 후에는 반드시 다음 항목을 확인하는 것이 좋다.

- docker ps
- docker logs
- API 정상 응답
- Port Mapping
- Container 상태

운영 환경에서는 위 다섯 가지를 기본 점검 항목으로 사용한다.

---

### 운영 시 고려사항

Container가 정상적으로 실행되더라도 Security Group, Port Mapping, 애플리케이션 Binding(0.0.0.0) 설정이 올바르지 않으면 외부에서는 접근할 수 없다.

Container 내부와 외부 네트워크를 함께 확인하는 것이 중요하다.

---

### 관련 기술

- Docker Image
- Docker Container
- Docker Networking
- Port Mapping
- Flask
- REST API



# 8. 핵심 기술 이해

---

## 8-1. Docker란?

### Docker의 정의

Docker는 애플리케이션과 실행 환경을 하나의 패키지(Container)로 구성하여 어느 환경에서도 동일하게 실행할 수 있도록 지원하는 Container Platform이다.

운영체제 수준의 가상화를 이용하기 때문에 Virtual Machine보다 가볍고 빠르게 실행된다.

---

### Docker를 사용하는 이유

프로젝트를 개발하다 보면 개발 환경과 운영 환경의 차이로 인해 애플리케이션이 정상적으로 동작하지 않는 문제가 자주 발생한다.

Docker는 애플리케이션 실행에 필요한 라이브러리와 설정을 함께 패키징하여 환경에 관계없이 동일한 실행 환경을 제공한다.

---

### 이번 프로젝트에서 Docker를 사용한 이유

본 프로젝트에서는 Flask API를 Container 환경에서 실행하기 위해 Docker를 사용하였다.

이후 Kubernetes가 Docker Image를 기반으로 Pod를 생성하게 되므로 Docker는 Kubernetes의 기반 기술이다.

---

### Docker 특징

- 환경 독립성
- 빠른 배포
- 높은 이식성
- 이미지 기반 배포
- 컨테이너 격리
- DevOps 친화적

---

### 프로젝트 적용

이번 프로젝트에서는

Docker Engine

↓

Dockerfile

↓

Docker Image

↓

Docker Container

↓

Flask API

순으로 구축하였다.

이를 기반으로 DAY2에서는 Kubernetes Deployment를 진행할 예정이다.


## 8-2. Container란?

### Container의 정의

Container는 애플리케이션과 실행 환경을 하나의 독립된 실행 단위로 구성한 기술이다.

Container는 Host OS의 Kernel을 공유하면서 각각 독립적인 프로세스로 실행된다.

---

### Container를 사용하는 이유

애플리케이션마다 필요한 라이브러리와 실행 환경이 다르기 때문에 동일한 서버에서도 충돌 없이 실행하기 위해 사용한다.

---

### 프로젝트 적용

Flask API를 Docker Container에서 실행하였다.

Host의 5000번 포트를 Container의 5000번 포트와 연결하여 외부에서도 Flask API에 접근할 수 있도록 구성하였다.

---

### Container 특징

- Host Kernel 공유

- 빠른 실행

- 작은 용량

- 높은 이식성

- 독립적인 실행 환경



## 8-3. Docker Engine이란?

### Docker Engine의 정의

Docker Engine은 Docker Platform의 핵심 구성 요소로, Docker Image를 관리하고 Docker Container를 생성 및 실행하는 역할을 담당한다.

사용자가 실행하는 모든 Docker 명령은 Docker Engine을 통해 실제 작업이 수행된다.

---

### Docker Engine의 구성

Docker Engine은 크게 다음 세 가지 구성 요소로 이루어진다.

| 구성 요소 | 역할 |
|-----------|------|
| Docker CLI | 사용자가 입력하는 docker 명령어 처리 |
| Docker Daemon | Docker Image 및 Container 관리 |
| REST API | CLI와 Docker Daemon 간 통신 |

---

### Docker Engine 동작 과정

```text
docker build

        │

Docker CLI

        │

REST API

        │

Docker Daemon

        │

Docker Image 생성
```

Container 실행도 동일한 구조를 사용한다.

```text
docker run

        │

Docker CLI

        │

REST API

        │

Docker Daemon

        │

Container 생성

        │

Container 실행
```

---

### 이번 프로젝트에서 Docker Engine 역할

DAY1에서는 Docker Engine을 설치한 후 Flask 애플리케이션을 Docker Image로 생성하였다.

이후 Docker Engine이 Flask Image를 기반으로 새로운 Container를 생성하여 Flask API를 실행하였다.

즉, 이번 프로젝트에서 실제 Container를 생성하고 실행한 주체는 Docker Engine이다.

---

### Docker Engine을 사용하는 이유

Docker CLI는 단순히 명령어를 입력하는 프로그램이다.

실제 Image 생성, Container 생성, 네트워크 연결 등의 작업은 모두 Docker Engine이 수행한다.

---

### 학습 포인트

- Docker Engine은 Docker의 핵심 실행 환경이다.
- Docker CLI와 Docker Engine은 서로 다른 구성 요소이다.
- Docker Engine이 실제 Container를 생성하고 실행한다.
- Docker Engine은 Kubernetes에서도 Container Runtime과 함께 중요한 역할을 수행한다.

---

### 실무 TIP

Docker 장애가 발생하면 먼저 Docker Engine(Docker Daemon)이 정상적으로 실행 중인지 확인한다.

대표적인 확인 명령어

```bash
docker version

docker info

systemctl status docker
```

---

### 운영 시 고려사항

Docker Engine이 실행 중이어도 Docker Socket 권한(docker 그룹)이 없으면 Docker CLI는 Docker Engine과 통신하지 못한다.

이번 프로젝트에서도 docker.sock 권한 문제를 해결한 후 정상적으로 Docker Engine과 통신할 수 있었다.


## 8-4. Docker CLI란?

### Docker CLI의 정의

Docker CLI(Command Line Interface)는 사용자가 Docker를 제어하기 위해 사용하는 명령어 인터페이스이다.

사용자가 입력하는 `docker build`, `docker run`, `docker ps` 등의 명령어는 Docker CLI를 통해 Docker Engine(Docker Daemon)으로 전달된다.

---

### Docker CLI 동작 과정

```text
사용자

↓

docker run

↓

Docker CLI

↓

Docker Engine

↓

Container 실행
```

---

### 이번 프로젝트에서 Docker CLI 역할

DAY1에서는 Docker CLI를 이용하여 다음 작업을 수행하였다.

- Docker Image 생성
- Docker Container 실행
- Docker Image 확인
- Docker Container 상태 확인
- Docker 로그 확인

즉, 사용자는 Docker CLI를 통해 Docker Engine을 제어하였다.

---

### 학습 포인트

- Docker CLI는 명령어를 입력하는 프로그램이다.
- 실제 작업은 Docker Engine이 수행한다.
- Docker CLI와 Docker Engine은 서로 다른 구성 요소이다.

---

### 실무 TIP

Docker 장애가 발생했을 때 Docker CLI가 정상적으로 실행되더라도 Docker Engine(Daemon)이 실행 중이지 않으면 Docker 명령은 실패한다.

따라서 Docker CLI와 Docker Engine을 구분하여 이해하는 것이 중요하다.


## 8-5. Dockerfile이란?

### Dockerfile의 정의

Dockerfile은 Docker Image를 생성하기 위한 설계도(Recipe)이다.

Docker Image를 생성하기 위해 필요한 모든 과정을 코드 형태로 정의한 파일이며, Docker Build 과정에서 순차적으로 실행된다.

---

### 이번 프로젝트에서 Dockerfile 역할

DAY1에서는 Flask 애플리케이션을 Container 환경에서 실행하기 위해 Dockerfile을 작성하였다.

Dockerfile에는 다음 작업을 정의하였다.

- Python Base Image 선택
- 작업 디렉터리 생성
- Flask 설치
- 프로젝트 소스 복사
- 5000 포트 개방
- Flask 실행

Docker Build는 Dockerfile을 순서대로 실행하여 Docker Image를 생성하였다.

---

### Dockerfile 실행 흐름

```text
FROM

↓

WORKDIR

↓

COPY requirements.txt

↓

RUN pip install

↓

COPY .

↓

EXPOSE

↓

CMD

↓

Docker Image
```

---

### Dockerfile을 사용하는 이유

Docker는 애플리케이션을 직접 실행하지 않는다.

먼저 Dockerfile을 이용하여 실행 환경을 포함한 Docker Image를 생성한 후 해당 이미지를 기반으로 Container를 실행한다.

---

### 학습 포인트

- Dockerfile은 Docker Image를 생성하는 설계도이다.
- Docker Build는 Dockerfile을 순차적으로 실행한다.
- Dockerfile 자체는 실행되지 않는다.
- Dockerfile의 결과물이 Docker Image이다.

---

### 실무 TIP

Dockerfile은 변경이 적은 Layer부터 작성하는 것이 좋다.

이번 프로젝트에서도 requirements.txt를 먼저 복사한 후 pip install을 수행하여 Docker Layer Cache를 최대한 활용하였다.

### 이번 프로젝트 설계 이유

Flask 애플리케이션은 Kubernetes에서 Pod 형태로 실행될 예정이므로 Dockerfile을 이용하여 실행 환경을 코드로 관리하였다.

이를 통해 동일한 실행 환경을 유지할 수 있으며 GitHub Actions를 이용한 자동 Image Build에도 동일한 Dockerfile을 재사용할 수 있도록 설계하였다.



## 8-6. Docker Image란?

### Docker Image의 정의

Docker Image는 Container를 생성하기 위한 실행 가능한 템플릿이다.

애플리케이션 실행에 필요한 운영체제, 라이브러리, 소스코드, 실행 명령 등이 모두 포함되어 있으며 변경되지 않는(Read-Only) 특성을 가진다.

---

### 이번 프로젝트에서 Docker Image 역할

DAY1에서는 Flask 애플리케이션을 Dockerfile을 이용하여 Docker Image로 생성하였다.

생성된 Image는 `flask-api:v1`이라는 이름으로 저장되었으며 이후 Docker Container를 생성하는 기반이 되었다.

즉, 실제 서비스는 Container가 수행하지만 Container를 생성하기 위한 기반은 Docker Image이다.

---

### Docker Image 생성 과정

```text
Dockerfile

↓

docker build

↓

Docker Image (flask-api:v1)
```

---

### Docker Image 특징

- 변경되지 않는(Read-Only) 구조
- 여러 Container가 하나의 Image를 공유 가능
- Docker Hub를 통해 배포 가능
- 버전(Tag) 관리 가능

---

### 이번 프로젝트 적용

```bash
docker build -t flask-api:v1 .
```

명령을 수행하여 Flask API를 Docker Image로 생성하였다.

생성된 Image는 `docker images` 명령으로 확인하였다.

---

### 학습 포인트

- Dockerfile은 Image를 생성하는 설계도이다.
- Docker Image는 실행 가능한 패키지이다.
- Image 자체는 실행되지 않는다.
- Image를 기반으로 Container가 생성된다.

---

### 실무 TIP

Image에는 버전(Tag)을 반드시 관리하는 것이 좋다.

예)

- flask-api:v1
- flask-api:v2
- flask-api:latest

GitHub Actions에서도 Image Tag를 이용하여 버전을 관리하는 경우가 많다.

---

### 이번 프로젝트 설계 이유

DAY1에서는 Flask API를 Docker Image로 생성하였다.

이 Image는 DAY2 Kubernetes Deployment에서 Pod를 생성할 때 사용되며, DAY3 GitHub Actions에서는 자동으로 Build되어 Docker Hub에 Push되는 구조로 확장될 예정이다.



## 8-7. Docker Container란?

### Docker Container의 정의

Docker Container는 Docker Image를 실행한 실제 프로세스이다.

Docker Image는 실행 가능한 템플릿이며 Container는 Image를 기반으로 생성되는 실행 환경이다.

---

### 이번 프로젝트에서 Docker Container 역할

DAY1에서는 `flask-api:v1` Image를 기반으로 새로운 Container를 생성하였다.

Container 내부에서 Flask API가 실행되었으며 EC2 Host의 5000번 포트와 연결하여 외부 브라우저에서도 접근할 수 있도록 구성하였다.

---

### Docker Container 생성 과정

```text
Docker Image

↓

docker run

↓

Docker Container

↓

Flask API 실행
```

---

### Docker Container 특징

- Image 기반으로 생성
- 독립적인 실행 환경 제공
- 생성 및 삭제가 빠름
- Host OS Kernel 공유

---

### 이번 프로젝트 적용

```bash
docker run -d \
--name flask-api \
-p 5000:5000 \
flask-api:v1
```

Container를 생성한 뒤 `docker ps` 명령을 통해 실행 상태를 확인하였다.

이후 브라우저에서 EC2 Public IP를 이용하여 Flask API에 정상적으로 접근되는 것을 확인하였다.

---

### 학습 포인트

- Image는 실행되지 않는다.
- Container가 실제 실행된다.
- 하나의 Image로 여러 개의 Container를 생성할 수 있다.
- docker ps는 실행 중인 Container를 확인하는 명령어이다.

---

### 실무 TIP

Container 실행 후에는 반드시 다음 항목을 확인한다.

- Container 상태
- Port Mapping
- Logs
- API 응답

운영 환경에서는 위 항목을 기본 점검 사항으로 사용한다.

---

### 이번 프로젝트 설계 이유

Container를 이용하여 Flask API를 실행한 이유는 동일한 실행 환경을 유지하기 위해서이다.

향후 Kubernetes에서는 동일한 Image를 이용하여 여러 개의 Pod를 생성하게 되며 Container는 Pod 내부에서 실행되는 애플리케이션의 기본 단위가 된다.



## 8-8. Docker Layer와 Build Cache

### Docker Layer란?

Docker Image는 하나의 파일이 아니라 여러 개의 Layer(계층)로 구성된다.

Dockerfile의 각 명령어는 하나의 Layer를 생성하며 Docker Build는 Dockerfile을 위에서 아래 순서대로 실행하면서 Layer를 하나씩 쌓아간다.

---

### 이번 프로젝트 Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python","app.py"]
```

Docker Build 과정은 다음과 같이 Layer를 생성한다.

```text
Layer 1

FROM python:3.12-slim

↓

Layer 2

WORKDIR /app

↓

Layer 3

COPY requirements.txt

↓

Layer 4

RUN pip install

↓

Layer 5

COPY app.py

↓

Layer 6

EXPOSE 5000

↓

Layer 7

CMD python app.py
```

---

### Docker Layer Cache란?

Docker는 이미 생성된 Layer를 다시 생성하지 않는다.

Dockerfile이 변경되지 않은 Layer는 이전 Build 결과를 재사용(Cache)하여 Build 속도를 크게 향상시킨다.

---

### 이번 프로젝트 적용

이번 프로젝트에서는 아래와 같이 작성하였다.

```dockerfile
COPY requirements.txt .

RUN pip install ...

COPY . .
```

이유는 requirements.txt가 변경되지 않으면 pip install Layer를 다시 실행하지 않도록 하기 위함이다.

만약 app.py만 수정한 경우 Docker는 마지막 Layer만 다시 생성한다.

이를 Docker Layer Cache라고 한다.

---

### 학습 포인트

- Dockerfile의 각 명령은 하나의 Layer를 생성한다.
- Docker Build는 Layer 단위로 캐시를 재사용한다.
- 변경되지 않은 Layer는 다시 Build하지 않는다.
- Dockerfile 순서에 따라 Build 속도가 크게 달라질 수 있다.

---

### 실무 TIP

변경 가능성이 적은 파일(requirements.txt 등)을 먼저 COPY하는 것이 좋다.

이렇게 하면 pip install Layer를 계속 재사용할 수 있어 Build 시간을 크게 단축할 수 있다.

---

### 이번 프로젝트 설계 이유

이번 프로젝트에서는 Docker Build 속도를 고려하여 requirements.txt를 먼저 복사한 뒤 Python 패키지를 설치하도록 Dockerfile을 구성하였다.

이는 GitHub Actions에서도 동일하게 적용되어 CI Build 시간을 줄이는 효과를 얻을 수 있다.



## 8-9. Build Context란?

### Build Context의 정의

Build Context는 Docker Build 과정에서 Docker에게 전달되는 작업 디렉터리를 의미한다.

Docker는 Build Context 안에 있는 파일만 사용할 수 있다.

---

### 이번 프로젝트 적용

Docker Build는 아래 명령으로 수행하였다.

```bash
docker build -t flask-api:v1 .
```

여기서 마지막 `.`은 현재 디렉터리를 의미한다.

즉,

```text
.

↓

현재 디렉터리(app)

↓

Docker에게 전달

↓

Docker Build
```

과정이 수행된다.

---

### Build Context 동작 과정

```text
현재 디렉터리

↓

Build Context

↓

Docker Daemon

↓

Dockerfile 실행

↓

Image 생성
```

---

### 왜 Build Context가 필요한가?

Docker Daemon은 현재 디렉터리를 자동으로 읽지 않는다.

Docker Build를 수행할 때 Build Context를 전달하여 필요한 파일(app.py, Dockerfile, requirements.txt)을 함께 보내야 한다.

---

### 학습 포인트

- 마지막 `.`은 현재 디렉터리를 의미한다.
- Docker는 Build Context 안의 파일만 사용할 수 있다.
- Dockerfile도 Build Context 내부에 있어야 한다.

---

### 실무 TIP

Build Context가 너무 크면 Docker Build 속도가 느려진다.

불필요한 파일은 `.dockerignore`를 사용하여 제외하는 것이 좋다.

---

### 이번 프로젝트 설계 이유

이번 프로젝트에서는 app 디렉터리를 Build Context로 사용하였다.

Dockerfile, Flask 소스코드, requirements.txt만 포함하여 Build 시간을 최소화하도록 구성하였다.

### Build Context 최적화

이번 프로젝트에서는 Build Context를 최소화하기 위해 `.dockerignore` 파일을 추가하였다.

```text
__pycache__/
*.pyc
.git
.gitignore
.vscode
```

Docker Build 시 불필요한 파일을 제외하여 Build 속도를 향상시키고 Docker Image 크기를 최소화하였다.

---

### Why?

Build Context가 커질수록 Docker Daemon으로 전달되는 파일이 많아져 Build 시간이 증가한다.

불필요한 파일은 `.dockerignore`를 통해 제외하는 것이 효율적이다.

---

### 실무 TIP

`.gitignore`는 Git에서 제외할 파일을 정의하고,

`.dockerignore`는 Docker Build에서 제외할 파일을 정의한다.

두 파일은 목적이 다르므로 함께 사용하는 것이 일반적이다.


## 8-10. Docker Networking

### Docker Networking의 정의

Docker Networking은 Host와 Docker Container, 그리고 Container 간의 네트워크 통신을 제공하는 기능이다.

Docker는 Container마다 독립적인 네트워크 환경을 제공하며 Port Mapping을 통해 외부와 연결할 수 있다.

---

### 이번 프로젝트에서 Docker Networking 역할

이번 프로젝트에서는 Flask API를 Docker Container 내부에서 실행하였다.

외부 브라우저에서 접근할 수 있도록 Host의 5000번 포트와 Container의 5000번 포트를 연결하였다.

```bash
docker run -d \
--name flask-api \
-p 5000:5000 \
flask-api:v1
```

---

### Port Mapping 구조

```text
Browser

        │

EC2 Public IP:5000

        │

Docker Host

        │

5000 → 5000

        │

Flask Container

        │

Flask API
```

---

### 학습 포인트

- Container 내부 포트는 외부에서 직접 접근할 수 없다.
- Host Port와 Container Port를 Mapping해야 외부 접근이 가능하다.
- `-p HostPort:ContainerPort` 형식을 사용한다.

---

### 실무 TIP

Container는 실행되더라도 Security Group이나 Port Mapping이 올바르지 않으면 외부에서는 접근할 수 없다.

Docker 문제인지 AWS 네트워크 문제인지 구분하여 확인하는 습관이 중요하다.

---

### 운영 시 고려사항

Container 실행 후에는 반드시 다음을 확인한다.

- docker ps
- Port Mapping
- Security Group
- Application Binding(0.0.0.0)

이번 프로젝트에서는 Security Group에 TCP 5000 포트를 추가하여 외부에서 Flask API에 정상적으로 접근할 수 있었다.


## 8-11. Docker Hub

### Docker Hub의 정의

Docker Hub는 Docker에서 제공하는 공식 Image Registry이다.

사용자는 Docker Hub에서 다양한 Docker Image를 다운로드(Pull)하거나 직접 생성한 Docker Image를 업로드(Push)할 수 있다.

---

### 이번 프로젝트에서 Docker Hub 역할

Docker 설치가 정상적으로 완료되었는지 확인하기 위해 Docker 공식 테스트 이미지인 `hello-world`를 Docker Hub에서 다운로드하여 실행하였다.

```bash
docker run hello-world
```

또한 직접 생성한 Flask Docker Image는 향후 GitHub Actions를 이용하여 Docker Hub에 자동 Push할 예정이다.

---

### Docker Hub 동작 과정

```text
Docker Hub

        │

docker pull

        │

Docker Image

        │

docker run

        │

Docker Container
```

---

### 학습 포인트

- Docker Hub는 Docker Image 저장소이다.
- docker pull은 Docker Hub에서 Image를 다운로드한다.
- docker push는 Docker Image를 Registry에 업로드한다.
- Docker Hub는 GitHub Actions와 연계하여 자동 배포에 활용할 수 있다.

---

### 실무 TIP

프로젝트에서는 Docker Image를 직접 Build하는 것보다 CI/CD를 통해 자동으로 Docker Hub에 Push하는 구조를 많이 사용한다.

이번 프로젝트도 DAY3에서 GitHub Actions를 이용하여 Docker Hub 자동 Push를 구현할 예정이다.

---

### 운영 시 고려사항

Docker Hub는 Public과 Private Repository를 모두 지원한다.

운영 환경에서는 불필요하게 Public Repository를 사용하지 않도록 주의하며, 민감한 이미지는 Private Repository에 저장하는 것이 좋다.



# 9. 문제 해결 (Problem Solving)

DAY1을 진행하면서 Docker 설치 및 Flask API 실행 과정에서 몇 가지 문제가 발생하였다.

각 문제에 대해 원인을 분석하고 해결 과정을 정리하였다.

프로젝트를 수행하면서 발생한 실제 문제를 해결한 경험이므로 이후 유사한 환경에서도 참고할 수 있도록 기록하였다.

---



## 9-1. Docker Permission Denied

### 문제

Docker 설치 후 아래 명령어를 실행하였을 때 Docker Engine과 통신하지 못하는 문제가 발생하였다.

```bash
docker version
```

오류 메시지

```text
permission denied while trying to connect to the Docker daemon socket
```

---

### 원인 분석

Docker CLI는 Docker Engine과 직접 통신하지 않는다.

Linux에서는 Docker Daemon과 Unix Socket(`/var/run/docker.sock`)을 이용하여 통신하며 해당 Socket은 docker 그룹 사용자만 접근할 수 있다.

현재 로그인한 ubuntu 사용자는 docker 그룹에 포함되어 있지 않았기 때문에 Docker Daemon 접근 권한이 없었다.

---

### 해결 과정

사용자를 docker 그룹에 추가하였다.

```bash
sudo usermod -aG docker ubuntu
```

이후 현재 Shell에 새로운 Group을 적용하였다.

```bash
newgrp docker
```

마지막으로 Docker Client와 Docker Server가 정상적으로 통신하는 것을 확인하였다.

```bash
docker version
```

---

### 결과

Docker Engine과 정상적으로 통신할 수 있게 되었으며 이후 Docker Build 및 Docker Run이 정상적으로 수행되었다.

---

### 배운 점

Linux에서는 사용자 권한(Group Permission)이 Docker 실행과 직접 연결된다.

Docker 설치 후에는 docker 그룹 권한을 반드시 확인하는 것이 좋다.




## 9-2. Flask API 외부 접속 실패

### 문제

Docker Container는 정상적으로 실행되었으나 EC2 Public IP를 이용한 Flask API 접속이 되지 않았다.

브라우저에서는 연결할 수 없다는 메시지가 표시되었다.

---

### 원인 분석

Docker Container 내부에서는 Flask API가 정상적으로 실행되고 있었으나 AWS Security Group에서 TCP 5000 포트가 허용되지 않은 상태였다.

Docker Networking은 정상적으로 구성되어 있었지만 AWS 네트워크 레벨에서 접근이 차단되고 있었다.

---

### 해결 과정

AWS Security Group에 TCP 5000 포트를 추가하였다.

이후 EC2 Public IP를 이용하여 다시 접속한 결과 Flask API가 정상적으로 응답하는 것을 확인하였다.

---

### 결과

Docker Container뿐 아니라 AWS 네트워크까지 정상적으로 구성되었음을 확인하였다.

---

### 배운 점

Docker 문제와 AWS 네트워크 문제는 반드시 구분하여 확인해야 한다.

Container 내부가 정상이라고 해서 외부 접근까지 가능한 것은 아니다.



## 9-3. GitHub 인증 문제

### 문제

EC2에서 Git Push를 수행하는 과정에서 GitHub 인증이 실패하였다.

---

### 원인 분석

Windows에서 설정한 Git 인증 정보는 EC2로 전달되지 않는다.

EC2는 별도의 Linux 환경이므로 GitHub 인증을 다시 수행해야 한다.

---

### 해결 과정

GitHub Personal Access Token(PAT)을 생성하여 EC2에서 Git Push를 수행하였다.

향후에는 SSH Key 기반 인증으로 변경하여 보다 안전한 Git 인증 환경을 구성할 예정이다.

---

### 결과

EC2에서도 GitHub Repository와 정상적으로 동기화할 수 있는 환경을 구성하였다.

---

### 배운 점

Windows와 EC2는 서로 다른 Git 환경이다.

원격 서버에서는 별도의 Git 인증 구성이 필요하다.



### 예방 방법

- Docker 설치 후 docker 그룹 권한을 먼저 확인한다.
- Security Group은 서비스 포트를 미리 검토한다.
- EC2 Git 인증은 프로젝트 시작 시 SSH Key 또는 PAT를 설정한다.




# 10. DAY1 회고

DAY1에서는 AWS EC2 환경을 기반으로 Docker 플랫폼을 구축하고 Flask API를 Docker Container 환경에서 실행하는 것까지 완료하였다.

처음에는 단순히 Docker를 설치하는 것이 목표였지만 프로젝트를 진행하면서 Docker Engine, Docker Repository, Dockerfile, Docker Image, Docker Container의 관계를 이해하는 것이 훨씬 중요하다는 것을 확인하였다.

또한 Docker Permission 문제와 Flask 외부 접속 문제를 직접 해결하면서 Docker 자체뿐 아니라 Linux 권한과 AWS Security Group도 함께 이해할 수 있었다.

이번 DAY1을 통해 단순히 Docker를 설치한 것이 아니라 Docker 기반 애플리케이션을 구축하고 운영하는 전체 흐름을 경험하였다.

---

## 잘된 점

- Docker 공식 Repository를 이용하여 최신 Docker Engine을 설치하였다.
- Remote SSH 기반 개발 환경을 구축하였다.
- Flask API를 Docker Container 환경에서 정상적으로 실행하였다.
- GitHub를 Source of Truth로 사용하는 개발 환경을 구성하였다.
- 프로젝트 수행 과정과 기술 내용을 동시에 문서화하였다.

---

## 아쉬운 점

- Docker 권한 문제(docker.sock) 해결에 예상보다 시간이 많이 소요되었다.
- Docker Build 과정에서 Layer 구조를 더 일찍 이해했다면 Dockerfile 작성이 더 효율적이었을 것이다.
- Git 인증(PAT)보다 SSH Key 기반 인증을 먼저 적용했으면 더 좋았을 것이다.

---

## 개선할 점

- DAY2 시작 전 GitHub 인증을 SSH Key 방식으로 변경한다.
- Docker Build 최적화를 위해 .dockerignore를 적극 활용한다.
- 모든 구축 과정을 문서와 동시에 관리하여 문서 작업이 밀리지 않도록 유지한다.

---

## DAY1 핵심 성과

- AWS EC2 구축 완료
- Remote SSH 개발 환경 구축
- Docker Engine 설치 완료
- Docker Image 생성 완료
- Docker Container 실행 완료
- Flask API 정상 서비스 확인
- GitHub와 EC2 연동 완료

---

## 이번 프로젝트에서 가장 크게 배운 점

Docker는 단순히 컨테이너를 실행하는 프로그램이 아니라 Image, Container, Docker Engine, Docker CLI, Repository, Build 과정이 유기적으로 연결된 플랫폼이라는 것을 이해하였다.

또한 GitHub를 중심으로 Windows와 EC2를 연결하여 실제 DevOps 개발 흐름과 유사한 환경을 구축할 수 있었다.



# 11. DAY2 계획

DAY2에서는 Docker 환경을 기반으로 Kubernetes Cluster를 구축한다.

DAY1에서 생성한 Docker Image를 Kubernetes에서 실행 가능한 형태로 변경하고 Deployment와 Service를 이용하여 컨테이너를 오케스트레이션하는 것을 목표로 한다.

---

## DAY2 목표

- Minikube 설치
- kubectl 설치
- Kubernetes Cluster 생성
- Deployment 생성
- Service 생성
- Pod 배포
- Flask API를 Kubernetes 환경에서 실행

---

## DAY2 산출물

- Kubernetes Cluster 구축
- Deployment YAML
- Service YAML
- Pod 상태 확인
- kubectl 명령어 정리
- DAY2.md 작성
- README 업데이트
- Master Document 업데이트

---

## DAY2에서 중점적으로 학습할 내용

- Kubernetes Architecture
- Pod
- Deployment
- Service
- ReplicaSet
- kubectl
- Kubernetes Networking

---

## DAY2 완료 목표

Docker Container 환경에서 실행 중인 Flask API를 Kubernetes Pod 환경으로 이전하여 Kubernetes 기반 Cloud Platform 구축을 완료한다.