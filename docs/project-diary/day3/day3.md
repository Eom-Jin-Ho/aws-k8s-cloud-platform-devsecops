# DAY3 - GitHub Actions 기반 CI Pipeline 구축 및 Docker Hub 자동화

---

# 1. DAY3 목표

DAY3의 목표는 GitHub Actions를 이용하여 CI(Continuous Integration) 환경을 구축하고, 코드 변경 시 Docker Image를 자동으로 Build하여 Docker Hub에 Push하는 자동화 파이프라인을 구성하는 것이다.

기존에는 EC2 환경에서 직접 Docker Image를 Build하고 Kubernetes에서 실행하였다.

DAY3에서는 GitHub Actions를 이용하여 Docker Image Build 과정을 자동화하고, Docker Hub를 Image Registry로 활용하여 어디서든 동일한 Docker Image를 사용할 수 있는 환경을 구축하는 것을 목표로 한다.

또한 GitHub Hosted Runner를 이용한 자동 Build 환경을 구성하고, Docker Hub에서 이미지를 다시 Pull하여 실제 Container 실행까지 검증함으로써 CI Pipeline이 정상적으로 동작하는 것을 확인한다.

---

# 2. DAY3 완료 목표

- GitHub Actions Workflow 구축
- Docker Hub Repository 생성
- Docker Hub Access Token 생성
- GitHub Repository Secrets 등록
- Docker Image 자동 Build
- Docker Hub 자동 Push
- GitHub Hosted Runner 기반 CI Pipeline 구축
- Docker Hub Image Pull 검증
- Docker Container 실행 검증

---

# 3. 구축 환경

| 항목 | 내용 |
|------|------|
| Cloud | AWS EC2 (t3.medium) |
| OS | Ubuntu 24.04 LTS |
| Container Runtime | Docker CE |
| Kubernetes | Minikube v1.38.1 |
| CI | GitHub Actions |
| Image Registry | Docker Hub |
| IDE | VS Code Remote SSH |
| SCM | Git / GitHub |
| Git Workflow | Feature Branch Strategy |

---

# 4. 전체 아키텍처

```text
Developer

        │

Git Push

        │

GitHub Repository

        │

GitHub Actions

        │

GitHub Hosted Runner

        │

Docker Build

        │

Docker Hub

        │

Docker Pull

        │

Docker Container
```

---

# 5. DAY3에서 구현한 기능

- Git Main Branch 최신화
- Feature Branch 생성
- Docker Hub Repository 생성
- Docker Hub Access Token 생성
- GitHub Repository Secrets 등록
- GitHub Actions Workflow 작성
- GitHub Hosted Runner 기반 CI Pipeline 구축
- Docker Image 자동 Build
- Docker Hub 자동 Push
- Docker Hub Image Pull 검증
- Docker Container 실행 검증

---

# 6. 프로젝트 디렉터리

```text
aws-k8s-cloud-platform-devsecops

├── app
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── .github
│   └── workflows
│       └── docker-build.yml
│
├── k8s
├── argocd
├── monitoring
├── docs
│
└── README.md
```

---

# 7. 구축 과정


## 7-1. Git Main Branch 최신화

### 배경

DAY2에서는 Feature Branch를 이용하여 Kubernetes 환경을 구축한 후 Main Branch로 Merge를 완료하였다.

DAY3를 시작하기 전에 EC2와 GitHub Repository의 Main Branch가 동일한 상태인지 확인하고 최신 코드를 기준으로 새로운 Feature Branch를 생성할 필요가 있었다.

Feature Branch를 오래된 Main Branch에서 생성하면 최신 코드가 반영되지 않은 상태에서 개발이 진행될 수 있으므로, 프로젝트를 시작하기 전에 Main Branch를 최신 상태로 유지하는 과정을 먼저 수행하였다.

---

### 목적

GitHub Repository의 Main Branch와 로컬 Main Branch를 동기화하여 최신 상태를 유지한 후 DAY3 작업을 위한 Feature Branch를 생성할 준비를 한다.

---

### Why?

Feature Branch는 항상 최신 Main Branch를 기준으로 생성하는 것이 Git 운영의 기본 원칙이다.

오래된 Main Branch를 기준으로 Feature Branch를 생성하면 이후 Merge 과정에서 불필요한 충돌(Conflict)이 발생할 가능성이 높아진다.

이번 프로젝트에서는 Windows와 EC2를 함께 사용하는 Git Workflow를 적용하고 있으므로, DAY 시작 전 Main Branch를 최신 상태로 유지하는 것을 운영 원칙으로 정하였다.

---

### 사용 명령어

```bash
git checkout main

git pull origin main

git status
```

---

### 명령어 설명

| 명령어 | 설명 |
|---------|------|
| `git checkout main` | Main Branch로 전환 |
| `git pull origin main` | GitHub의 Main Branch 최신 Commit을 가져와 동기화 |
| `git status` | 현재 Branch 상태와 변경 사항 확인 |

---

### 실행 결과

Main Branch가 GitHub Repository와 동일한 최신 상태인 것을 확인하였다.

또한 작업 디렉터리에 변경 사항이 없는 `working tree clean` 상태를 확인하여 새로운 Feature Branch를 생성할 준비가 완료되었다.

---

### 결과 분석

DAY3 작업은 최신 Main Branch를 기준으로 시작되었다.

이를 통해 이전 작업(DAY1, DAY2)의 모든 변경 사항이 반영된 상태에서 새로운 Feature Branch를 생성할 수 있게 되었으며, Git Branch 간 충돌 가능성을 최소화하였다.

또한 GitHub를 Source of Truth로 사용하는 프로젝트 운영 원칙에 따라 EC2와 GitHub Repository가 동일한 상태임을 확인하였다.

---

### 학습 포인트

- Feature Branch는 항상 최신 Main Branch를 기준으로 생성하는 것이 좋다.
- `git pull`은 원격 저장소와 로컬 저장소를 동기화하는 명령어이다.
- `git status`를 통해 현재 Branch 상태와 변경 사항을 확인할 수 있다.
- GitHub를 Source of Truth로 사용하는 경우 Main Branch 최신화는 프로젝트 시작 전 필수 작업이다.

---

### 캡처

![Git Main Branch 최신화 확인](docs/screenshots/day3/01-main-branch-updated.jpg)

---

### 실무 TIP

프로젝트를 시작하기 전에 항상 Main Branch를 최신 상태로 유지한 후 Feature Branch를 생성하는 습관을 가지는 것이 좋다.

이를 통해 Merge 시 발생할 수 있는 충돌을 줄일 수 있으며 여러 명이 함께 개발하는 환경에서도 안정적으로 협업할 수 있다.

---

### 운영 시 고려사항

GitHub를 Source of Truth로 사용하는 환경에서는 Main Branch가 프로젝트의 기준이 된다.

새로운 기능을 개발하기 전에 반드시 Main Branch를 최신 상태로 유지하고 Feature Branch를 생성하는 절차를 운영 표준으로 유지하는 것이 중요하다.

## 7-2. Feature Branch 생성

### 배경

DAY2부터 프로젝트의 Git 운영 전략을 Main Branch 기반 개발 방식에서 Feature Branch 기반 개발 방식으로 변경하였다.

Main Branch는 항상 안정적인 상태를 유지하고, 새로운 기능은 Feature Branch에서 독립적으로 개발한 후 충분한 검증을 거쳐 Main Branch로 Merge하는 전략을 적용하였다.

DAY3에서는 GitHub Actions 기반 CI Pipeline 구축을 위한 작업을 진행하기 위해 새로운 Feature Branch를 생성하였다.

---

### 목적

DAY3 기능을 Main Branch와 분리하여 독립적으로 개발하고, 기능 구현 및 검증이 완료된 후 Main Branch로 Merge하기 위한 개발 환경을 구성한다.

---

### Why?

Feature Branch 전략은 새로운 기능을 독립적으로 개발할 수 있도록 지원하는 Git Workflow이다.

만약 Main Branch에서 직접 개발을 진행하면 개발 중 발생한 오류나 미완성 기능이 프로젝트 전체에 영향을 줄 수 있다.

Feature Branch를 사용하면 기능 단위로 Commit과 Push를 수행할 수 있으며, 충분한 테스트를 완료한 이후 Main Branch로 Merge할 수 있으므로 안정적인 프로젝트 운영이 가능하다.

이번 프로젝트에서는 하루 단위(DAY1, DAY2, DAY3...)로 기능을 구분하여 각각 하나의 Feature Branch에서 개발하는 방식을 운영 전략으로 적용하였다.

---

### 사용 명령어

```bash
git checkout -b feature/day3-github-actions

git branch
```

---

### 명령어 설명

| 명령어 | 설명 |
|---------|------|
| `git checkout -b feature/day3-github-actions` | 새로운 Feature Branch 생성과 동시에 해당 Branch로 이동 |
| `git branch` | 현재 생성된 Branch 목록과 현재 작업 중인 Branch 확인 |

---

### 실행 결과

`feature/day3-github-actions` Branch를 생성하고 해당 Branch로 정상적으로 전환하였다.

이후 DAY3에서 수행한 모든 GitHub Actions 관련 작업은 Feature Branch에서 진행하였다.

---

### 결과 분석

DAY3의 모든 변경 사항은 Main Branch와 분리된 상태에서 독립적으로 개발되었다.

GitHub Actions Workflow 작성, Docker Hub 연동, CI Pipeline 구축 및 검증이 완료된 이후 Main Branch로 Merge하는 방식으로 프로젝트를 운영하였다.

이를 통해 Main Branch는 항상 안정적인 상태를 유지하면서 새로운 기능을 단계적으로 추가할 수 있었다.

---

### 학습 포인트

- Feature Branch는 기능 단위 개발을 위한 Git Workflow이다.
- 새로운 기능은 Main Branch가 아닌 Feature Branch에서 개발하는 것이 일반적이다.
- Feature Branch를 이용하면 Merge 전 충분한 테스트를 수행할 수 있다.
- Main Branch는 항상 안정적인 상태를 유지하는 것이 좋다.

---

### 캡처

![DAY3 Feature Branch 생성](docs/screenshots/day3/2. DAY3 Feature Branch 생성.jpg)

---

### 실무 TIP

실무에서는 Feature Branch마다 하나의 기능만 개발하는 것이 일반적이다.

기능 구현이 완료되면 Pull Request(PR)를 생성하여 코드 리뷰를 수행한 후 Main Branch로 Merge하는 방식으로 운영한다.

이번 프로젝트는 개인 프로젝트이므로 Pull Request 과정은 생략하였지만, Feature Branch → 검증 → Merge 순서는 실제 운영 환경과 동일하게 적용하였다.

---

### 운영 시 고려사항

Feature Branch는 가능한 한 짧은 기간 동안 유지하는 것이 좋다.

장기간 Merge하지 않고 개발을 진행하면 Main Branch와의 차이가 커져 Merge Conflict가 발생할 가능성이 높아진다.

이번 프로젝트에서는 DAY 단위로 Feature Branch를 생성하고, 해당 DAY가 종료되면 Main Branch로 Merge한 후 Feature Branch를 삭제하는 운영 전략을 유지하였다.


## 7-3. Docker Hub Repository 생성

### 배경

DAY1에서는 Docker Image를 EC2 환경에서 직접 Build하여 로컬 Docker Engine에서 실행하였다.

DAY2에서도 동일한 로컬 Docker Image를 Minikube에 등록하여 Kubernetes Pod를 실행하였다.

그러나 로컬 Docker Image는 해당 EC2 환경에서만 사용할 수 있으며, 다른 서버에서는 동일한 Docker Image를 사용할 수 없다는 한계가 있었다.

DAY3에서는 GitHub Actions를 이용하여 Docker Image를 자동으로 Build하고 Docker Hub에 Push하기 위해 Docker Hub Repository를 생성하였다.

---

### 목적

Docker Image를 중앙 저장소(Image Registry)에 저장하여 GitHub Actions, Kubernetes, 다른 서버 환경에서도 동일한 Docker Image를 사용할 수 있도록 구성한다.

---

### Why?

Docker Image는 EC2 로컬 환경에만 존재하면 다른 시스템에서는 사용할 수 없다.

Docker Hub와 같은 Image Registry를 사용하면 GitHub Actions에서 Build한 Docker Image를 중앙 저장소에 업로드할 수 있으며, 이후 Kubernetes나 다른 서버에서 동일한 이미지를 다운로드(Pull)하여 사용할 수 있다.

이번 프로젝트에서는 Docker Hub를 공식 Container Image Registry로 사용하여 CI Pipeline의 결과물을 관리하도록 구성하였다.

---

### 수행 내용

- Docker Hub 계정 생성 및 로그인
- Docker Hub Repository 생성
- Repository 공개(Public) 설정
- GitHub Actions에서 사용할 Image Repository 준비

---

### 실행 결과

Docker Hub에 `flask-api` Repository를 생성하였다.

이후 GitHub Actions에서 Build한 Docker Image를 해당 Repository로 자동 Push할 수 있는 환경이 준비되었다.

---

### 결과 분석

DAY1과 DAY2에서는 Docker Image가 EC2 내부에만 존재하였다.

DAY3에서는 Docker Hub Repository를 구축함으로써 Docker Image를 중앙에서 관리할 수 있게 되었으며, GitHub Actions와 Kubernetes가 동일한 Docker Image를 사용할 수 있는 기반을 마련하였다.

이를 통해 개발 환경과 운영 환경에서 동일한 Docker Image를 사용하는 Immutable Infrastructure 환경의 첫 단계를 구성하였다.

---

### 학습 포인트

- Docker Hub는 Docker Image를 저장하는 공식 Image Registry이다.
- Docker Image는 Registry를 통해 여러 환경에서 공유할 수 있다.
- GitHub Actions는 Docker Hub를 이용하여 Build 결과를 저장한다.
- Kubernetes는 Docker Hub에서 Docker Image를 Pull하여 Pod를 생성할 수 있다.

---

### 캡처

![Docker Hub Repository 생성 완료](docs/screenshots/day3/3. Docker Hub Repository 생성 완료.jpg)

---

### 실무 TIP

실무에서는 Docker Hub 외에도 AWS ECR(Elastic Container Registry), Azure Container Registry(ACR), Google Artifact Registry와 같은 Private Registry를 사용하는 경우가 많다.

이번 프로젝트에서는 가장 범용적으로 사용할 수 있는 Docker Hub를 선택하여 CI Pipeline을 구성하였다.

---

### 운영 시 고려사항

Docker Hub Repository는 Public과 Private 형태로 운영할 수 있다.

학습 및 포트폴리오 프로젝트에서는 Public Repository를 사용하여 누구나 Docker Image를 확인할 수 있도록 구성하였으며, 운영 환경에서는 보안 정책에 따라 Private Repository를 사용하는 것이 일반적이다.


## 7-4. GitHub Repository Secrets 등록

### 배경

GitHub Actions는 GitHub Hosted Runner 환경에서 자동으로 Workflow를 실행한다.

Runner는 Docker Hub에 Docker Image를 Push하기 위해 Docker Hub 계정으로 인증(Authentication)을 수행해야 한다.

그러나 GitHub Actions Workflow 파일(`docker-build.yml`) 내부에 Docker Hub 계정 정보나 Access Token을 직접 작성하면 Repository에 인증 정보가 노출되는 심각한 보안 문제가 발생할 수 있다.

이를 방지하기 위해 GitHub에서 제공하는 Repository Secrets 기능을 이용하여 Docker Hub 인증 정보를 안전하게 관리하였다.

---

### 목적

GitHub Actions가 Docker Hub에 안전하게 로그인할 수 있도록 인증 정보를 암호화하여 저장하고, Workflow에서는 Secrets를 참조하도록 구성한다.

---

### Why?

GitHub Actions는 사람이 직접 로그인하는 환경이 아니라 GitHub Hosted Runner가 자동으로 Docker Hub에 로그인하여 Docker Image를 Push하는 구조이다.

Runner가 Docker Hub에 접근하기 위해서는 인증 정보가 필요하지만, Workflow 파일 안에 Username이나 Password를 직접 작성하면 Git Repository를 통해 인증 정보가 외부로 노출될 위험이 있다.

GitHub Repository Secrets를 이용하면 인증 정보를 암호화하여 저장할 수 있으며 Workflow에서는 `${{ secrets.변수명 }}` 형태로 참조하기 때문에 인증 정보를 코드에 노출하지 않고 안전하게 사용할 수 있다.

이번 프로젝트에서는 Docker Hub 계정명과 Access Token을 각각 Repository Secrets에 저장하여 GitHub Actions에서 안전하게 활용하도록 구성하였다.

---

### 수행 내용

- GitHub Repository Settings 이동
- Repository Secrets 생성
- Docker Hub Username 등록
- Docker Hub Access Token 등록
- GitHub Actions에서 Secrets 참조 구성

등록한 Secret은 다음과 같다.

| Secret | 용도 |
|---------|------|
| DOCKERHUB_USERNAME | Docker Hub 계정명 |
| DOCKERHUB_TOKEN | Docker Hub Access Token |

---

### 실행 결과

Repository Secrets에 Docker Hub 계정 정보와 Access Token을 정상적으로 등록하였다.

이후 GitHub Actions Workflow에서는 `${{ secrets.DOCKERHUB_USERNAME }}`와 `${{ secrets.DOCKERHUB_TOKEN }}`을 이용하여 Docker Hub에 자동 로그인할 수 있는 환경을 구성하였다.

---

### 결과 분석

GitHub Repository Secrets를 이용하여 인증 정보를 Workflow와 분리하였다.

이를 통해 Git Repository에는 인증 정보가 저장되지 않으며 GitHub Hosted Runner가 실행되는 동안에만 암호화된 Secret이 전달되어 Docker Hub 인증에 사용된다.

또한 프로젝트마다 서로 다른 인증 정보를 사용할 수 있도록 Repository 단위로 Secrets를 관리하여 프로젝트 간 인증 정보가 분리되도록 구성하였다.

---

### 학습 포인트

- GitHub Repository Secrets는 인증 정보를 암호화하여 저장하는 기능이다.
- Workflow에서는 `${{ secrets.변수명 }}` 형태로 Secret을 참조한다.
- 인증 정보는 코드에 직접 작성하지 않는 것이 기본 보안 원칙이다.
- Repository마다 독립적인 Secrets를 관리할 수 있다.

---

### 캡처

![GitHub Repository Secrets 설정 화면](docs/screenshots/day3/4. GitHub Repository Secrets 설정 화면.jpg)

![Docker Hub Access Token 생성](docs/screenshots/day3/5. Docker Hub Access Token 생성.jpg)

![GitHub Repository Secrets 등록 완료](docs/screenshots/day3/6. GitHub Repository Secrets 등록 완료.jpg)

---

### 실무 TIP

실무에서는 Docker Hub뿐 아니라 AWS Access Key, Azure Service Principal, Kubernetes Token, Slack Webhook 등 다양한 민감한 정보를 GitHub Repository Secrets를 이용하여 관리한다.

인증 정보는 코드에 포함하지 않고 Secret Manager를 통해 관리하는 것이 DevSecOps의 기본적인 보안 원칙이다.

---

### 운영 시 고려사항

Repository Secrets는 Repository 단위로 관리된다.

프로젝트마다 서로 다른 Docker Registry나 Cloud 계정을 사용할 수 있으므로 Repository별로 인증 정보를 분리하여 관리하는 것이 일반적이다.

또한 Docker Hub Password 대신 Access Token을 사용하는 것이 권장되며, 필요 최소 권한(Principle of Least Privilege)을 부여한 Token을 사용하는 것이 보안 측면에서 유리하다.


## 7-5. GitHub Actions Workflow 생성

### 배경

Docker Hub Repository와 GitHub Repository Secrets 구성이 완료되었으므로 GitHub Actions를 이용한 CI(Continuous Integration) Pipeline을 구성하였다.

GitHub Actions는 Repository에서 발생하는 이벤트(Event)를 감지하여 자동으로 Workflow를 실행하는 CI/CD 플랫폼이다.

이번 프로젝트에서는 Docker Image Build와 Docker Hub Push 과정을 자동화하기 위해 `.github/workflows/docker-build.yml` Workflow를 작성하였다.

---

### 목적

GitHub Actions Workflow를 생성하여 Git Push가 발생하면 Docker Image를 자동으로 Build하고 Docker Hub로 Push하는 CI Pipeline을 구축한다.

---

### Why?

DAY1과 DAY2에서는 Docker Image를 직접 Build한 후 Docker Hub 또는 Kubernetes에서 사용하였다.

이 방식은 개발자가 직접 Docker Build와 Push를 수행해야 하므로 반복 작업이 발생하고, 사람의 실수(Human Error)가 발생할 가능성이 존재한다.

GitHub Actions Workflow를 이용하면 Git Push만으로 Docker Image Build부터 Docker Hub Push까지 자동으로 수행할 수 있으며 항상 동일한 절차를 유지할 수 있다.

이를 통해 Build 과정의 표준화와 자동화를 동시에 달성할 수 있다.

---

### 수행 내용

- `.github/workflows` 디렉터리 생성
- `docker-build.yml` 생성
- GitHub Actions Workflow 작성
- Push Event Trigger 구성
- Docker Build 및 Push 자동화 구성

---

### 실행 결과

GitHub Actions Workflow 파일을 정상적으로 생성하였다.

Workflow는 Git Push를 감지하여 자동으로 실행되도록 구성하였으며 이후 GitHub Hosted Runner에서 Docker Build 및 Docker Hub Push를 수행할 수 있는 기반을 마련하였다.

---

### 결과 분석

GitHub Repository에는 `.github/workflows` 디렉터리에 위치한 모든 Workflow를 자동으로 인식하는 기능이 있다.

Git Push가 발생하면 GitHub는 Repository 내부의 Workflow를 검색하고 Trigger 조건을 만족하는 Workflow를 자동으로 실행한다.

이번 프로젝트에서는 `docker-build.yml`을 이용하여 GitHub Actions 기반 CI Pipeline을 구성하였다.

---

### 학습 포인트

- GitHub Actions Workflow는 `.github/workflows` 디렉터리에 저장된다.
- Workflow는 YAML 형식으로 작성된다.
- GitHub는 Push Event를 감지하여 Workflow를 자동 실행한다.
- Workflow는 CI/CD 자동화의 시작점이다.

---

### 캡처

![GitHub Actions Workflow 디렉터리 생성 완료](docs/screenshots/day3/7. GitHub Actions Workflow 디렉터리 생성 완료.jpg)

---

### 실무 TIP

실무에서는 Repository마다 여러 개의 Workflow를 운영하는 경우가 많다.

예를 들어 Build Workflow, Test Workflow, Security Scan Workflow, Deploy Workflow 등을 각각 분리하여 관리한다.

이번 프로젝트에서는 Docker Image Build와 Push만 수행하는 단일 Workflow를 구성하였으며 이후 DAY4에서 ArgoCD를 이용한 CD Workflow로 확장할 예정이다.

---

### 운영 시 고려사항

Workflow 파일은 Git Repository에 포함되므로 코드와 동일하게 버전 관리된다.

Workflow 수정 사항도 Git Commit을 통해 추적할 수 있으므로 CI 환경 또한 코드(Infrastructure as Code) 형태로 관리할 수 있다.


## 7-6. GitHub Actions Workflow Trigger 구성

### 배경

GitHub Actions Workflow를 생성한 후에는 언제 Workflow를 실행할 것인지 정의하는 Trigger 구성이 필요하였다.

GitHub Actions는 항상 실행되는 서비스가 아니라 Repository에서 특정 이벤트(Event)가 발생했을 때만 Workflow를 실행하는 Event-Driven 구조를 사용한다.

이번 프로젝트에서는 Git Push가 발생하면 Docker Image Build와 Docker Hub Push가 자동으로 수행되도록 Push Event를 Trigger로 구성하였다.

---

### 목적

Git Push가 발생하면 GitHub Actions Workflow가 자동으로 실행되도록 Trigger를 구성한다.

---

### Why?

Workflow는 Repository에 존재한다고 해서 자동으로 실행되지 않는다.

GitHub Actions는 Repository에서 발생하는 다양한 이벤트를 감지한 후 Trigger 조건을 만족하는 Workflow만 실행한다.

이번 프로젝트에서는 Git Push를 기준으로 Docker Image를 자동 Build하는 CI Pipeline을 구성하였으므로 Push Event를 Trigger로 선택하였다.

또한 모든 Branch에서 Workflow가 실행되는 것을 방지하기 위해 DAY3 Feature Branch와 Main Branch에서만 Workflow가 실행되도록 Branch 조건을 함께 설정하였다.

---

### 사용 코드

```yaml
name: Docker Build and Push

on:
  push:
    branches:
      - feature/day3-github-actions
      - main
```

---

### 코드 설명

| 항목 | 설명 |
|------|------|
| `name` | GitHub Actions Workflow 이름 |
| `on` | Workflow 실행 조건(Event Trigger) |
| `push` | Git Push 발생 시 실행 |
| `branches` | 특정 Branch에서만 Workflow 실행 |

---

### 실행 결과

Git Push가 발생하면 GitHub Actions가 Repository 내부의 Workflow를 자동으로 검색한 후 Branch 조건을 확인하여 Workflow를 실행하였다.

DAY3에서는 `feature/day3-github-actions` Branch에서 Push가 발생하였으므로 Docker Build Workflow가 정상적으로 실행되었다.

---

### 결과 분석

GitHub Actions는 Push Event를 감지한 후 Repository 내부의 `.github/workflows` 디렉터리를 검색한다.

이후 Workflow의 Trigger 조건을 확인하고 Branch 조건이 일치하는 경우에만 GitHub Hosted Runner를 생성하여 Workflow를 실행한다.

이번 프로젝트에서는 Feature Branch에서 먼저 CI Pipeline을 검증한 후 Main Branch Merge 이후에도 동일한 Workflow가 자동 실행되도록 구성하였다.

이를 통해 개발 단계와 운영 단계에서 동일한 CI Pipeline을 사용할 수 있는 구조를 구축하였다.

---

### 학습 포인트

- GitHub Actions는 Event-Driven 방식으로 동작한다.
- Workflow는 Trigger 조건을 만족할 때만 실행된다.
- Push는 GitHub Actions에서 가장 많이 사용하는 Trigger이다.
- Branch 조건을 이용하여 원하는 Branch에서만 Workflow를 실행할 수 있다.

---

### 캡처

![GitHub Actions Workflow Trigger 작성](docs/screenshots/day3/8. GitHub Actions Workflow Trigger 작성.jpg)

---

### 실무 TIP

실무에서는 모든 Branch에서 Workflow를 실행하지 않는다.

일반적으로 다음과 같이 Branch별 Workflow를 구분한다.

- feature/* : 개발 및 테스트
- develop : 통합 테스트
- main : 운영 Build
- release : Release Build

Branch별 Trigger를 분리하면 불필요한 Build를 줄이고 운영 안정성을 높일 수 있다.

---

### 운영 시 고려사항

이번 프로젝트에서는 Feature Branch와 Main Branch에서만 Workflow가 실행되도록 구성하였다.

Feature Branch에서는 새로운 기능을 검증하고 Main Branch에서는 최종 Docker Image를 생성하는 방식으로 운영하여 안정적인 CI 환경을 유지하도록 설계하였다.



## 7-7. GitHub Hosted Runner 구성 (Job / Runner)

### 배경

GitHub Actions Workflow가 실행되기 위해서는 실제 명령어를 수행할 실행 환경이 필요하다.

GitHub Actions는 Git Push와 같은 이벤트가 발생하면 GitHub Hosted Runner를 자동으로 생성하고, 생성된 Runner에서 Workflow 내부의 Job과 Step을 순차적으로 실행한다.

이번 프로젝트에서는 별도의 Jenkins 서버나 Self-hosted Runner를 구축하지 않고 GitHub에서 제공하는 Ubuntu Runner를 이용하여 Docker Build 및 Docker Hub Push를 수행하였다.

---

### 목적

GitHub Hosted Runner를 이용하여 Docker Build 및 Docker Hub Push를 수행할 수 있는 자동 실행 환경을 구성한다.

---

### Why?

GitHub Actions Workflow는 단순한 설정 파일(YAML)이 아니라 실제 Linux 환경에서 실행되어야 한다.

GitHub Hosted Runner를 이용하면 별도의 Build Server를 구축하지 않아도 GitHub가 Ubuntu 가상 서버를 자동으로 생성하여 Workflow를 실행한다.

이를 통해 별도의 CI 서버를 운영하지 않고도 자동 Build 환경을 구성할 수 있다.

이번 프로젝트에서는 GitHub Hosted Runner를 이용하여 Docker Build와 Docker Hub Push를 자동으로 수행하도록 구성하였다.

---

### 사용 코드

```yaml
jobs:
  docker-build:
    runs-on: ubuntu-latest
```

---

### 코드 설명

| 항목 | 설명 |
|------|------|
| jobs | Workflow에서 실행할 작업(Job) 정의 |
| docker-build | Job 이름 |
| runs-on | Job이 실행될 Runner 환경 지정 |
| ubuntu-latest | GitHub Hosted Ubuntu Runner 사용 |

---

### 실행 결과

Git Push가 발생하면 GitHub가 Ubuntu Runner를 자동으로 생성하였다.

Runner는 Repository를 다운로드한 후 Docker Login, Docker Build, Docker Push를 순차적으로 수행하였으며 모든 작업이 완료된 후 자동으로 삭제되었다.

---

### 결과 분석

GitHub Hosted Runner는 Git Push 이벤트가 발생할 때마다 새로운 Ubuntu 가상 환경을 생성한다.

Runner는 Workflow 실행이 완료되면 자동으로 삭제되므로 항상 동일한 초기 환경(Clean Environment)에서 Build가 수행된다.

이를 통해 이전 Build 결과가 다음 Build에 영향을 주지 않으며 항상 동일한 조건에서 Docker Image를 생성할 수 있다.

이번 프로젝트에서는 GitHub Hosted Runner를 이용하여 Docker Build부터 Docker Hub Push까지의 전체 CI Pipeline을 자동으로 수행하였다.

---

### 학습 포인트

- Runner는 GitHub Actions가 실행되는 실제 Linux 환경이다.
- GitHub Hosted Runner는 GitHub가 자동으로 생성하고 삭제한다.
- Job은 Runner 내부에서 실행되는 작업 단위이다.
- Workflow는 하나 이상의 Job으로 구성될 수 있다.
- Runner는 항상 새로운 환경에서 실행되므로 Build 결과의 일관성을 유지할 수 있다.

---

### 캡처

![GitHub Actions Job 및 Runner 설정](docs/screenshots/day3/9. GitHub Actions Job 및 Runner 설정.jpg)

---

### 실무 TIP

GitHub Actions는 GitHub Hosted Runner와 Self-hosted Runner 두 가지 방식을 지원한다.

- GitHub Hosted Runner
  - GitHub가 Runner를 관리
  - 별도의 서버 운영이 필요 없음
  - 가장 많이 사용하는 방식

- Self-hosted Runner
  - 사용자가 직접 Runner 서버 운영
  - 사내망이나 내부 시스템 접근 가능
  - 기업 환경에서 많이 사용

이번 프로젝트에서는 관리 부담이 적고 빠르게 구축할 수 있는 GitHub Hosted Runner를 선택하였다.

---

### 운영 시 고려사항

GitHub Hosted Runner는 Workflow 실행이 완료되면 자동으로 삭제된다.

따라서 Runner 내부에 생성된 파일이나 Docker Image는 다음 Workflow에서 사용할 수 없다.

매번 새로운 Runner에서 Build가 수행되므로 필요한 모든 작업은 Workflow 내부에서 다시 수행해야 한다.

이러한 특성 때문에 GitHub Actions에서는 Docker Hub와 같은 외부 Image Registry를 함께 사용하는 것이 일반적이다.



## 7-8. GitHub Repository Checkout (Checkout Action)

### 배경

GitHub Hosted Runner는 Workflow가 실행될 때마다 새로운 Ubuntu 환경을 생성한다.

새롭게 생성된 Runner는 프로젝트 소스코드를 가지고 있지 않은 초기 상태(Clean Environment)이므로 Docker Build를 수행하기 전에 GitHub Repository의 소스코드를 먼저 다운로드해야 한다.

이번 프로젝트에서는 GitHub 공식 Action인 `actions/checkout`을 이용하여 Runner 내부로 프로젝트 소스코드를 가져오도록 구성하였다.

---

### 목적

GitHub Repository의 프로젝트 소스코드를 GitHub Hosted Runner로 다운로드하여 Docker Build를 수행할 수 있는 환경을 구성한다.

---

### Why?

GitHub Hosted Runner는 Workflow가 실행될 때마다 새롭게 생성되는 임시 환경이다.

Runner 내부에는 프로젝트 소스코드가 존재하지 않으므로 Dockerfile, Flask 애플리케이션, requirements.txt 등을 사용할 수 없다.

Docker Build를 수행하려면 먼저 GitHub Repository의 최신 소스코드를 Runner 환경으로 가져와야 한다.

이를 위해 GitHub에서 공식적으로 제공하는 `actions/checkout` Action을 사용하였다.

---

### 사용 코드

```yaml
steps:
  - name: Checkout source code
    uses: actions/checkout@v5
```

---

### 코드 설명

| 항목 | 설명 |
|------|------|
| steps | Job 내부에서 실행되는 작업 목록 |
| name | Step 이름 |
| uses | GitHub Marketplace Action 사용 |
| actions/checkout | GitHub Repository 다운로드 |
| @v5 | Action Version |

---

### 실행 결과

GitHub Hosted Runner가 GitHub Repository의 최신 소스코드를 자동으로 다운로드하였다.

Runner 내부에는 프로젝트 전체 디렉터리가 생성되었으며 Dockerfile과 Flask 애플리케이션을 이용하여 Docker Build를 수행할 수 있는 환경이 구성되었다.

---

### 결과 분석

GitHub Hosted Runner는 처음 생성될 때 아무 파일도 존재하지 않는 빈 Ubuntu 환경이다.

`actions/checkout` Action은 GitHub Repository를 Runner 내부로 Clone하여 Docker Build에 필요한 프로젝트 파일을 준비하는 역할을 수행한다.

이번 프로젝트에서는 Checkout Action을 수행한 이후 Docker Login, Docker Build, Docker Push를 순차적으로 실행하였다.

Checkout 과정이 수행되지 않으면 Dockerfile을 찾을 수 없으므로 Docker Build 자체가 실패하게 된다.

---

### 학습 포인트

- GitHub Hosted Runner는 초기 상태에서는 프로젝트 파일을 가지고 있지 않다.
- Checkout Action은 GitHub Repository를 Runner로 다운로드하는 역할을 수행한다.
- `uses`는 GitHub Marketplace Action을 사용하는 문법이다.
- `@v5`는 Action의 버전을 의미하며 동일한 실행 환경을 유지하기 위해 버전을 고정한다.

---

### 캡처

![GitHub Actions Checkout Step 작성](docs/screenshots/day3/10. GitHub Actions Checkout Step 작성.jpg)

---

### 실무 TIP

GitHub Marketplace에는 Checkout 외에도 Docker Login, Security Scan, Kubernetes Deploy 등 다양한 공식 Action이 제공된다.

실무에서는 직접 스크립트를 작성하기보다 검증된 Marketplace Action을 조합하여 CI/CD Pipeline을 구성하는 경우가 많다.

---

### 운영 시 고려사항

Checkout Action은 Workflow에서 가장 먼저 수행되는 Step이다.

Repository를 정상적으로 다운로드하지 못하면 이후 Docker Build, Test, Security Scan 등 모든 작업이 실패하게 된다.

또한 Action은 버전(`@v5`)을 명시하여 사용하는 것이 일반적이며, 최신 버전으로 자동 변경되는 것을 방지하여 Workflow의 안정성과 재현성을 확보할 수 있다.


## 7-9. Docker Hub 인증 구성 (Docker Login Action)

### 배경

GitHub Hosted Runner는 Docker Image를 Docker Hub로 Push하기 위해 Docker Hub 계정으로 인증(Authentication)을 수행해야 한다.

그러나 GitHub Actions Workflow 내부에 Docker Hub Username이나 Password를 직접 작성하면 Git Repository를 통해 인증 정보가 노출될 수 있으므로 보안상 매우 위험하다.

이번 프로젝트에서는 GitHub Repository Secrets를 이용하여 Docker Hub 인증 정보를 암호화하여 저장하고, Docker 공식 Login Action을 이용하여 GitHub Hosted Runner가 Docker Hub에 안전하게 로그인하도록 구성하였다.

---

### 목적

GitHub Hosted Runner가 Docker Hub에 안전하게 인증하여 Docker Image를 Push할 수 있는 환경을 구축한다.

---

### Why?

Docker Hub는 인증된 사용자만 Docker Image를 Push할 수 있다.

GitHub Hosted Runner도 Docker Hub에 로그인해야 Docker Image를 업로드할 수 있지만 Workflow 파일 내부에 Password를 직접 작성하면 Git Repository를 통해 인증 정보가 외부에 노출될 위험이 있다.

GitHub Repository Secrets를 사용하면 인증 정보를 암호화하여 관리할 수 있으며 Workflow에서는 `${{ secrets.변수명 }}` 형태로만 참조하기 때문에 인증 정보를 안전하게 사용할 수 있다.

또한 Docker Hub Password 대신 Access Token을 사용하여 필요한 권한만 부여하는 최소 권한 원칙(Principle of Least Privilege)을 적용하였다.

---

### 사용 코드

```yaml
- name: Login to Docker Hub
  uses: docker/login-action@v4
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}
```

---

### 코드 설명

| 항목 | 설명 |
|------|------|
| `uses` | Docker 공식 Login Action 사용 |
| `docker/login-action` | Docker Hub 로그인 수행 |
| `@v4` | Login Action Version |
| `username` | GitHub Repository Secret에 저장된 Docker Hub 계정 |
| `password` | GitHub Repository Secret에 저장된 Docker Hub Access Token |

---

### 실행 결과

GitHub Hosted Runner가 Repository Secrets에서 Docker Hub Username과 Access Token을 가져와 Docker Hub 로그인에 성공하였다.

로그인이 완료된 이후 Docker Build 및 Docker Push를 정상적으로 수행할 수 있는 환경이 구성되었다.

---

### 결과 분석

GitHub Hosted Runner는 Workflow 실행 중에만 Repository Secrets를 전달받는다.

Runner 내부에서는 Secrets가 메모리에서만 사용되며 Workflow가 종료되면 Runner와 함께 제거된다.

이를 통해 Docker Hub 인증 정보를 코드에 노출하지 않고 안전하게 Docker Image를 Push할 수 있는 CI Pipeline을 구축하였다.

또한 프로젝트별로 서로 다른 Docker Hub 계정을 사용할 수 있도록 Repository 단위로 Secrets를 분리하여 관리하였다.

---

### 학습 포인트

- Docker Hub Push를 위해서는 인증(Authentication)이 필요하다.
- GitHub Repository Secrets를 이용하면 인증 정보를 안전하게 관리할 수 있다.
- Workflow에서는 `${{ secrets.변수명 }}` 형태로 Secret을 참조한다.
- Password 대신 Access Token을 사용하는 것이 보안상 권장된다.
- GitHub Hosted Runner는 Workflow 실행 중에만 Secret을 사용할 수 있다.

---

### 캡처

![GitHub Actions Docker Hub Login Step 작성](docs/screenshots/day3/11. GitHub Actions Docker Hub Login Step 작성.jpg)

---

### 실무 TIP

실무에서는 Docker Hub뿐 아니라 AWS, Azure, GCP, Kubernetes API Token 등 모든 민감한 인증 정보를 GitHub Repository Secrets 또는 Secret Manager를 이용하여 관리한다.

또한 Access Token은 필요한 권한만 부여하여 사용하는 것이 일반적인 보안 정책이다.

---

### 운영 시 고려사항

Repository마다 서로 다른 Docker Registry를 사용할 수 있으므로 Repository별로 Secrets를 분리하여 관리하는 것이 좋다.

Access Token은 주기적으로 교체(Rotation)하는 것이 권장되며, Password보다 Access Token을 사용하는 것이 보안성과 관리 측면에서 유리하다.

## 7-10. Docker Image Build 및 Docker Hub Push

### 배경

GitHub Hosted Runner가 GitHub Repository의 소스코드를 다운로드하고 Docker Hub 인증을 완료한 이후에는 Docker Image를 생성(Build)하고 Docker Hub에 업로드(Push)하는 과정이 필요하였다.

DAY1에서는 EC2 환경에서 `docker build` 명령을 직접 실행하여 Docker Image를 생성하였다.

DAY3에서는 Docker 공식 GitHub Action을 이용하여 GitHub Hosted Runner가 Docker Image를 자동으로 Build하고 Docker Hub에 Push하도록 구성하였다.

---

### 목적

GitHub Hosted Runner를 이용하여 Docker Image를 자동으로 Build하고 Docker Hub에 업로드하는 CI Pipeline을 구축한다.

---

### Why?

기존 방식에서는 개발자가 직접 Docker Image를 Build하고 Docker Hub에 Push해야 하므로 반복 작업이 발생하였다.

또한 Build 과정이 개발자마다 달라질 수 있으므로 동일한 Docker Image가 생성되지 않을 가능성이 존재하였다.

GitHub Actions를 이용하면 Git Push만으로 항상 동일한 Build 과정을 수행할 수 있으며 Docker Hub에 최신 Docker Image를 자동으로 저장할 수 있다.

이를 통해 CI Pipeline의 자동화와 Build 과정의 표준화를 동시에 구현하였다.

---

### 사용 코드

```yaml
- name: Build and Push Docker Image
  uses: docker/build-push-action@v6
  with:
    context: ./app
    file: ./app/Dockerfile
    push: true
    tags: ${{ secrets.DOCKERHUB_USERNAME }}/flask-api:latest
```

---

### 코드 설명

| 항목 | 설명 |
|------|------|
| `docker/build-push-action` | Docker Image Build 및 Push 수행 |
| `@v6` | Docker 공식 Build Action Version |
| `context` | Docker Build Context 지정 |
| `file` | Dockerfile 위치 |
| `push` | Docker Hub Push 수행 여부 |
| `tags` | Docker Image 이름 및 Tag 지정 |

---

### 실행 결과

GitHub Hosted Runner는 Build Context로 지정된 `./app` 디렉터리를 이용하여 Docker Image를 생성하였다.

생성된 Docker Image는 `hawku13/flask-api:latest` Tag를 부여한 후 Docker Hub Repository로 자동 Push되었다.

Workflow 종료 후 Docker Hub Repository에서 새로운 Docker Image가 정상적으로 생성된 것을 확인하였다.

---

### 결과 분석

GitHub Hosted Runner는 먼저 Docker Build Context를 Docker Buildx로 전달하였다.

Buildx는 Dockerfile과 프로젝트 소스코드를 이용하여 Docker Image를 생성한 후 지정된 Tag(`latest`)를 부여하였다.

이후 Docker Hub 인증 정보를 이용하여 Docker Image를 Docker Hub Repository에 업로드하였다.

이번 프로젝트에서는 Docker Build부터 Docker Hub Push까지의 모든 과정이 Git Push만으로 자동 수행되는 CI Pipeline을 구축하였다.

---

### 학습 포인트

- Docker Buildx는 Docker Image를 생성하는 공식 Build 도구이다.
- Build Context는 Docker Build에 전달되는 프로젝트 디렉터리이다.
- Dockerfile은 Build Context 내부에 존재해야 한다.
- `push: true`를 이용하여 Build 완료 후 Docker Hub에 자동 업로드할 수 있다.
- Docker Image는 Tag를 이용하여 버전을 관리한다.

---

### 캡처

![GitHub Actions Workflow 작성 완료](docs/screenshots/day3/12. GitHub Actions Workflow 작성 완료.jpg)

![GitHub Actions Workflow Push 완료](docs/screenshots/day3/13. GitHub Actions Workflow Push 완료.jpg)

![GitHub Actions Workflow 실행 성공](docs/screenshots/day3/14. GitHub Actions Workflow 실행 성공.jpg)

![GitHub Actions Job 실행 결과](docs/screenshots/day3/15. GitHub Actions Job 실행 결과.jpg)

![Docker Hub Image Push 완료](docs/screenshots/day3/16. Docker Hub Image Push 완료.jpg)

---

### 실무 TIP

실무에서는 `latest` Tag만 사용하는 것이 아니라 Git Commit SHA 또는 Semantic Version을 함께 사용하여 Docker Image 버전을 관리한다.

예를 들어 다음과 같은 형태를 많이 사용한다.

```text
flask-api:latest

flask-api:v1.0.0

flask-api:a82f7c1
```

이를 통해 장애 발생 시 이전 버전으로 Rollback할 수 있다.

---

### 운영 시 고려사항

이번 프로젝트에서는 학습과 GitOps 환경 구성을 위해 `latest` Tag를 사용하였다.

DAY4에서 ArgoCD는 Docker Hub의 `latest` 이미지를 기준으로 Kubernetes Deployment를 자동 동기화하도록 구성할 예정이다.

운영 환경에서는 `latest` 대신 Immutable Tag(Git SHA 또는 Semantic Version)를 사용하는 것이 일반적이다.


## 7-11. GitHub Actions 실행 검증 및 Docker Hub Image 검증

### 배경

GitHub Actions Workflow를 작성한 이후 실제로 Docker Image가 정상적으로 Build되고 Docker Hub에 Push되는지 검증하는 과정이 필요하였다.

또한 GitHub Actions가 생성한 Docker Image가 실제 실행 가능한 상태인지 확인하기 위해 Docker Hub에서 이미지를 다시 다운로드(Pull)하여 Container를 실행하는 검증을 추가로 수행하였다.

이번 검증은 단순히 Workflow 성공 여부를 확인하는 것이 아니라 CI Pipeline의 결과물(Artifact)이 실제 운영 가능한 상태인지 확인하기 위한 과정이다.

---

### 목적

GitHub Actions Workflow가 정상적으로 실행되는지 확인하고, Docker Hub에 업로드된 Docker Image를 다시 다운로드하여 실제 실행 가능한 상태인지 검증한다.

---

### Why?

GitHub Actions가 성공했다고 해서 반드시 Docker Image가 정상적으로 동작하는 것은 아니다.

Build 과정은 성공했더라도 Dockerfile이나 애플리케이션 문제로 인해 Container가 실행되지 않을 수도 있다.

따라서 Docker Hub에서 생성된 Docker Image를 다시 Pull하여 실제 Container 실행까지 검증함으로써 CI Pipeline의 결과물을 최종 확인하였다.

---

### 사용 명령어

```bash
docker pull hawku13/flask-api:latest

docker run --rm -p 5001:5000 hawku13/flask-api:latest
```

---

### 명령어 설명

| 명령어 | 설명 |
|---------|------|
| `docker pull` | Docker Hub에서 Docker Image 다운로드 |
| `docker run` | Docker Image를 이용하여 Container 실행 |
| `--rm` | Container 종료 시 자동 삭제 |
| `-p 5001:5000` | Host Port와 Container Port 연결 |

---

### 실행 결과

GitHub Actions Workflow가 정상적으로 실행되었으며 모든 Step이 성공하였다.

Docker Hub에는 `hawku13/flask-api:latest` Docker Image가 정상적으로 Push되었다.

이후 Docker Hub에서 해당 이미지를 다시 다운로드(Pull)하여 새로운 Container를 실행하였으며 Flask 애플리케이션이 정상적으로 실행되는 것을 확인하였다.

---

### 결과 분석

GitHub Actions는 Git Push를 감지하여 GitHub Hosted Runner를 생성하였다.

Runner는 Docker Image를 Build하고 Docker Hub에 Push한 후 자동으로 종료되었다.

이후 Docker Hub에서 동일한 Docker Image를 다시 다운로드하여 실행한 결과 Flask 애플리케이션이 정상적으로 동작하는 것을 확인하였다.

이를 통해 GitHub Actions가 생성한 Docker Image가 실제 운영 가능한 상태임을 검증하였다.

또한 이번 검증을 통해 CI Pipeline의 결과물(Artifact)이 정상적으로 생성되고 활용될 수 있음을 확인하였다.

---

### 학습 포인트

- GitHub Actions 성공과 Docker Image 정상 동작은 서로 다른 검증 과정이다.
- Docker Hub는 Build 결과를 저장하는 Image Registry 역할을 수행한다.
- `docker pull`을 이용하여 언제든 동일한 Docker Image를 사용할 수 있다.
- `--rm` 옵션은 Container 종료 시 자동으로 삭제한다.
- `-p 5001:5000`은 Host Port와 Container Port를 연결하는 Port Mapping 기능이다.

---

### 캡처

![GitHub Actions Workflow 실행 성공](docs/screenshots/day3/14. GitHub Actions Workflow 실행 성공.jpg)

![GitHub Actions Job 실행 결과](docs/screenshots/day3/15. GitHub Actions Job 실행 결과.jpg)

![Docker Hub Image Push 완료](docs/screenshots/day3/16. Docker Hub Image Push 완료.jpg)

![Docker Hub Image Pull 및 Container 실행 검증](docs/screenshots/day3/17. Docker Hub Image Pull 및 Container 실행 검증.jpg)

---

### 실무 TIP

CI Pipeline에서는 Build 성공 여부만 확인하지 않고 생성된 Docker Image를 실제 실행하여 정상 동작하는지 검증하는 것이 좋다.

최근에는 Integration Test나 Container Test를 추가하여 Build 이후 자동 검증을 수행하는 경우도 많다.

---

### 운영 시 고려사항

이번 프로젝트에서는 Docker Hub에서 이미지를 다시 Pull하여 수동으로 실행을 검증하였다.

운영 환경에서는 GitHub Actions 내부에서 자동 테스트를 수행하거나 Kubernetes에 임시 배포하여 Health Check를 수행하는 방식으로 CI Pipeline을 구성하는 것이 일반적이다.



# 8. 핵심 기술 이해

---

## 8-1. GitHub Actions와 CI(Continuous Integration)

### GitHub Actions란?

GitHub Actions는 GitHub에서 제공하는 CI/CD 자동화 플랫폼이다.

Repository에서 발생하는 Push, Pull Request, Release 등의 이벤트를 감지하여 Workflow를 자동으로 실행할 수 있다.

Workflow는 GitHub Hosted Runner 또는 Self-hosted Runner에서 실행되며 Build, Test, Security Scan, Deploy 등 다양한 자동화 작업을 수행할 수 있다.

---

### CI(Continuous Integration)란?

CI는 지속적 통합(Continuous Integration)을 의미한다.

개발자가 새로운 코드를 Git Repository에 Push하면 자동으로 Build, Test 등을 수행하여 코드 품질을 검증하는 개발 방식이다.

CI를 적용하면 사람이 직접 Docker Build를 수행하지 않아도 Git Push만으로 동일한 Build 환경을 유지할 수 있다.

---

### 이번 프로젝트에서 GitHub Actions 역할

이번 프로젝트에서는 Git Push를 Trigger로 GitHub Actions Workflow를 실행하였다.

Workflow는 GitHub Hosted Runner에서 Docker Image를 Build한 후 Docker Hub에 자동으로 Push하도록 구성하였다.

이를 통해 Docker Image 생성 과정을 자동화하는 CI Pipeline을 구축하였다.

---

### CI Pipeline 구조

```text
Developer

↓

Git Push

↓

GitHub Repository

↓

GitHub Actions

↓

GitHub Hosted Runner

↓

Docker Build

↓

Docker Push

↓

Docker Hub
```

---

### 학습 포인트

- GitHub Actions는 GitHub에서 제공하는 CI/CD 플랫폼이다.
- CI는 Git Push 이후 Build와 Test를 자동 수행하는 개발 방식이다.
- GitHub Actions는 Git Push를 Trigger로 자동 실행된다.
- 이번 프로젝트에서는 Docker Image Build를 자동화하는 CI Pipeline을 구축하였다.


## 8-2. GitHub Actions Workflow / Job / Step / Runner

### Workflow란?

Workflow는 GitHub Actions에서 자동으로 실행되는 작업 전체를 의미한다.

Workflow는 하나의 YAML 파일(`.github/workflows/*.yml`)로 정의되며 GitHub Repository에서 특정 이벤트가 발생하면 자동으로 실행된다.

이번 프로젝트에서는 `docker-build.yml` Workflow를 생성하여 Git Push가 발생하면 Docker Image를 자동으로 Build하고 Docker Hub에 Push하도록 구성하였다.

---

### Job이란?

Job은 Workflow 내부에서 실행되는 작업 단위이다.

하나의 Workflow는 하나 이상의 Job으로 구성될 수 있으며, 각각의 Job은 독립적인 Runner에서 실행된다.

이번 프로젝트에서는 `docker-build`라는 하나의 Job을 생성하여 Docker Build와 Docker Push를 수행하였다.

```yaml
jobs:
  docker-build:
    runs-on: ubuntu-latest
```

---

### Step이란?

Step은 Job 내부에서 순차적으로 실행되는 개별 작업이다.

각 Step은 하나의 명령(Command)을 실행하거나 GitHub Marketplace Action을 호출한다.

이번 프로젝트에서는 다음과 같은 Step으로 구성하였다.

```text
Checkout Source Code

↓

Docker Login

↓

Docker Build

↓

Docker Push
```

Step은 위에서 아래 순서대로 실행되며 이전 Step이 성공해야 다음 Step이 수행된다.

---

### Runner란?

Runner는 GitHub Actions Workflow를 실제로 실행하는 컴퓨터(실행 환경)이다.

GitHub Hosted Runner를 사용할 경우 GitHub가 Ubuntu Virtual Machine을 자동으로 생성하여 Workflow를 실행한다.

Workflow 실행이 완료되면 Runner는 자동으로 삭제된다.

이번 프로젝트에서는 GitHub Hosted Runner(Ubuntu)를 이용하여 Docker Build를 수행하였다.

---

### GitHub Hosted Runner 동작 과정

```text
Git Push

↓

GitHub Actions

↓

Ubuntu Runner 생성

↓

Repository Checkout

↓

Docker Login

↓

Docker Build

↓

Docker Push

↓

Runner 삭제
```

---

### Workflow 구조

이번 프로젝트의 GitHub Actions 구조는 다음과 같다.

```text
Workflow

↓

Job

↓

Step

↓

Action
```

각 Step은 GitHub Marketplace에서 제공하는 Action을 이용하여 구성하였다.

---

### 이번 프로젝트에서 적용한 Workflow

```text
docker-build.yml

↓

Workflow

↓

docker-build(Job)

↓

Checkout

↓

Docker Login

↓

Docker Build

↓

Docker Push
```

---

### 학습 포인트

- Workflow는 GitHub Actions 전체 실행 단위이다.
- Job은 Workflow 내부에서 실행되는 작업이다.
- Step은 Job 내부에서 순차적으로 수행되는 개별 작업이다.
- Runner는 Workflow를 실제 실행하는 Ubuntu 환경이다.
- GitHub Hosted Runner는 실행 후 자동 삭제된다.

---

### 실무 TIP

실무에서는 하나의 Workflow 안에 여러 개의 Job을 구성하는 경우가 많다.

예를 들어 다음과 같이 Build와 Security Scan을 병렬로 수행할 수 있다.

```text
Workflow

├── Build Job

├── Test Job

├── Security Scan Job

└── Deploy Job
```

Job 간에는 의존성을 설정하여 순차 실행 또는 병렬 실행이 가능하다.

---

### 운영 시 고려사항

GitHub Hosted Runner는 Workflow가 실행될 때마다 새롭게 생성되는 환경이다.

따라서 이전 Build에서 생성된 Docker Image나 임시 파일은 다음 Workflow에서 사용할 수 없다.

Runner가 항상 새로운 환경에서 실행되므로 필요한 모든 작업은 Workflow 안에서 다시 수행해야 한다.


## 8-3. GitHub Marketplace Action과 uses 문법

### GitHub Marketplace Action이란?

GitHub Marketplace Action은 GitHub Actions Workflow에서 사용할 수 있도록 미리 구현되어 있는 자동화 모듈이다.

GitHub 또는 다양한 오픈소스 프로젝트에서 제공하며, Workflow 내부에서 `uses` 문법을 이용하여 간단하게 사용할 수 있다.

개발자는 직접 Shell Script를 작성하지 않고도 Docker Login, Git Checkout, Kubernetes Deploy, Security Scan 등 다양한 기능을 손쉽게 사용할 수 있다.

---

### uses란?

`uses`는 GitHub Marketplace에 등록되어 있는 Action을 Workflow에서 가져와 실행하는 문법이다.

이번 프로젝트에서는 다음 세 가지 Action을 사용하였다.

```yaml
uses: actions/checkout@v5

uses: docker/login-action@v4

uses: docker/build-push-action@v6
```

GitHub Hosted Runner는 Workflow를 실행하면서 지정된 Action을 다운로드한 후 Runner 내부에서 실행한다.

---

### 이번 프로젝트에서 사용한 Action

#### actions/checkout

Repository의 최신 소스코드를 GitHub Hosted Runner로 다운로드한다.

```yaml
uses: actions/checkout@v5
```

역할

```text
GitHub Repository

↓

Runner

↓

프로젝트 다운로드
```

Checkout Action이 수행되지 않으면 Runner에는 프로젝트 파일이 존재하지 않으므로 Docker Build를 수행할 수 없다.

---

#### docker/login-action

Docker Hub에 로그인한다.

```yaml
uses: docker/login-action@v4
```

GitHub Repository Secrets에 저장된 Username과 Access Token을 이용하여 Docker Hub 인증을 수행한다.

---

#### docker/build-push-action

Docker Image를 Build하고 Docker Hub로 Push한다.

```yaml
uses: docker/build-push-action@v6
```

Build Context와 Dockerfile을 이용하여 Docker Image를 생성하고 Docker Hub에 자동 업로드한다.

---

### @v5, @v4, @v6의 의미

Action 뒤에 붙는 `@v5`, `@v4`, `@v6`은 Action의 Version을 의미한다.

예를 들어

```yaml
uses: actions/checkout@v5
```

는 Checkout Action Version 5를 사용한다는 의미이다.

GitHub Actions는 Version을 명시하여 사용하는 것이 일반적이다.

---

### Why?

Version을 지정하지 않으면 Action이 자동으로 변경될 수 있다.

새로운 Version에서 기능 변경이나 호환성 문제가 발생하면 기존 Workflow가 정상적으로 동작하지 않을 가능성이 있다.

Version을 고정하면 항상 동일한 Action을 실행하므로 Workflow의 재현성과 안정성을 확보할 수 있다.

---

### GitHub Marketplace Action 구조

```text
GitHub Marketplace

↓

Action 선택

↓

Runner 다운로드

↓

Workflow 실행
```

GitHub Hosted Runner는 Workflow 실행 시 필요한 Action을 자동으로 다운로드하여 사용한다.

---

### 학습 포인트

- `uses`는 GitHub Marketplace Action을 사용하는 문법이다.
- Marketplace Action은 미리 구현된 자동화 모듈이다.
- `actions/checkout`은 Repository를 Runner로 다운로드한다.
- `docker/login-action`은 Docker Hub 인증을 수행한다.
- `docker/build-push-action`은 Docker Image Build와 Push를 수행한다.
- `@v5`와 같은 Version을 지정하여 Workflow의 안정성을 확보한다.

---

### 실무 TIP

GitHub Marketplace에는 수천 개 이상의 Action이 등록되어 있다.

실무에서는 Build, Test, Security Scan, Kubernetes Deploy, Slack Notification 등을 Marketplace Action으로 조합하여 CI/CD Pipeline을 구성하는 경우가 많다.

---

### 운영 시 고려사항

Action Version은 가능한 고정하여 사용하는 것이 좋다.

또한 공식 Organization(GitHub, Docker 등)에서 제공하는 Action을 우선적으로 사용하는 것이 보안과 유지보수 측면에서 유리하다.

운영 환경에서는 최신 Version을 바로 적용하기보다 충분한 테스트를 거친 후 업그레이드하는 것이 일반적이다.


## 8-4. GitHub Repository Secrets

### GitHub Repository Secrets란?

GitHub Repository Secrets는 GitHub Actions Workflow에서 사용할 민감한 정보(Secret)를 암호화하여 저장하는 기능이다.

Workflow에서는 Secret 값을 직접 작성하지 않고 `${{ secrets.변수명 }}` 형태로 참조하여 사용할 수 있다.

Secrets는 Git Repository와 분리되어 관리되므로 코드에는 인증 정보가 포함되지 않는다.

---

### GitHub Secrets를 사용하는 이유

CI Pipeline에서는 Docker Hub, AWS, Kubernetes Cluster 등 다양한 외부 시스템에 접근해야 한다.

이 과정에서 Username, Password, API Key, Access Token과 같은 민감한 인증 정보가 필요하다.

이러한 정보를 Workflow 파일에 직접 작성하면 Git Repository를 통해 외부에 노출될 위험이 있다.

GitHub Repository Secrets를 사용하면 인증 정보를 암호화하여 안전하게 저장할 수 있으며 Workflow에서는 필요한 순간에만 참조하여 사용할 수 있다.

---

### 이번 프로젝트에서 사용한 Secrets

이번 프로젝트에서는 Docker Hub 인증을 위해 다음 두 개의 Secret을 등록하였다.

| Secret | 설명 |
|---------|------|
| DOCKERHUB_USERNAME | Docker Hub 계정명 |
| DOCKERHUB_TOKEN | Docker Hub Access Token |

Workflow에서는 다음과 같이 참조하였다.

```yaml
username: ${{ secrets.DOCKERHUB_USERNAME }}

password: ${{ secrets.DOCKERHUB_TOKEN }}
```

---

### GitHub Secrets 동작 과정

```text
Developer

↓

Repository Secrets

↓

GitHub Hosted Runner

↓

Workflow 실행

↓

Docker Login

↓

Workflow 종료

↓

Runner 삭제
```

GitHub Hosted Runner는 Workflow가 실행되는 동안에만 Secret을 전달받는다.

Workflow가 종료되면 Runner가 삭제되므로 Secret도 함께 제거된다.

---

### Password 대신 Access Token을 사용하는 이유

Docker Hub Password를 직접 사용하는 것도 가능하지만 보안상 권장되지 않는다.

Access Token은 필요한 권한만 부여할 수 있으며 언제든 폐기하거나 재발급할 수 있다.

또한 Password를 변경하지 않고도 Token만 교체할 수 있으므로 운영 관리가 용이하다.

이번 프로젝트에서도 Docker Hub Password 대신 Access Token을 사용하여 인증을 구성하였다.

---

### Repository마다 Secrets를 관리하는 이유

GitHub는 Repository 단위로 Secrets를 관리한다.

프로젝트마다 사용하는 Cloud 환경이나 Docker Registry가 서로 다를 수 있기 때문이다.

예를 들어

```text
Project A

↓

Docker Hub

────────────────────

Project B

↓

AWS ECR

────────────────────

Project C

↓

Azure Container Registry
```

처럼 프로젝트마다 서로 다른 인증 정보를 사용할 수 있으므로 Repository별로 Secrets를 분리하여 관리하는 것이 일반적이다.

---

### 학습 포인트

- GitHub Secrets는 민감한 인증 정보를 저장하는 기능이다.
- Workflow에서는 `${{ secrets.변수명 }}` 형태로 Secret을 참조한다.
- Secret은 Git Repository에 저장되지 않는다.
- Access Token을 사용하는 것이 Password보다 안전하다.
- Repository마다 독립적인 Secret을 관리할 수 있다.

---

### 실무 TIP

실무에서는 Docker Hub뿐 아니라 AWS Access Key, Azure Service Principal, Kubernetes Token, Slack Webhook 등 다양한 인증 정보를 GitHub Secrets 또는 Cloud Secret Manager를 이용하여 관리한다.

또한 Access Token은 최소 권한 원칙(Principle of Least Privilege)에 따라 필요한 권한만 부여하는 것이 일반적이다.

---

### 운영 시 고려사항

Secret은 코드와 분리하여 관리하는 것이 DevSecOps의 기본 원칙이다.

또한 Access Token은 주기적으로 Rotation(교체)하고 사용하지 않는 Token은 즉시 폐기하여 인증 정보 유출 위험을 최소화하는 것이 좋다.


## 8-5. Docker Hub(Image Registry)

### Docker Hub란?

Docker Hub는 Docker에서 제공하는 공식 Container Image Registry이다.

Docker Image를 중앙 저장소에 저장하고 관리할 수 있으며, 필요한 환경에서 언제든 동일한 Docker Image를 다운로드(Pull)하여 사용할 수 있다.

Docker Hub를 이용하면 개발 환경, 테스트 환경, 운영 환경에서 동일한 Docker Image를 사용할 수 있으므로 Build 환경의 일관성을 유지할 수 있다.

---

### Image Registry란?

Image Registry는 Docker Image를 저장하고 배포하는 저장소이다.

GitHub가 Source Code를 저장하는 Repository라면 Docker Hub는 Docker Image를 저장하는 Repository라고 볼 수 있다.

대표적인 Image Registry는 다음과 같다.

- Docker Hub
- Amazon ECR (Elastic Container Registry)
- Azure Container Registry (ACR)
- Google Artifact Registry
- Harbor

---

### Docker Hub를 사용하는 이유

DAY1에서는 Docker Image를 EC2 환경에서 직접 Build하였다.

```text
EC2

↓

docker build

↓

Local Docker Image
```

그러나 Local Docker Image는 해당 EC2 내부에서만 사용할 수 있다는 한계가 존재한다.

새로운 서버에서는 동일한 Docker Image를 다시 Build해야 한다.

Docker Hub를 사용하면 Build된 Docker Image를 중앙에서 관리할 수 있으며 어느 환경에서도 동일한 Docker Image를 사용할 수 있다.

---

### Local Image와 Remote Image 차이

#### Local Image

```text
EC2

↓

docker build

↓

Local Image
```

현재 서버에서만 사용할 수 있다.

다른 서버에서는 존재하지 않는다.

---

#### Remote Image

```text
Docker Hub

↓

docker pull

↓

Container 실행
```

Docker Hub에 저장되어 있으므로 어느 환경에서도 동일한 Docker Image를 사용할 수 있다.

---

### 이번 프로젝트에서 Docker Hub 역할

이번 프로젝트에서는 GitHub Actions가 Docker Image를 Build한 후 Docker Hub Repository에 자동으로 Push하도록 구성하였다.

이후 EC2에서 Docker Hub의 이미지를 다시 Pull하여 새로운 Container를 실행함으로써 CI Pipeline의 결과물이 정상적으로 동작하는 것을 검증하였다.

또한 DAY4에서는 ArgoCD가 Docker Hub의 Docker Image를 기준으로 Kubernetes Deployment를 자동 동기화하도록 구성할 예정이다.

---

### Docker Hub 동작 과정

```text
Developer

↓

Git Push

↓

GitHub Actions

↓

GitHub Hosted Runner

↓

Docker Build

↓

Docker Push

↓

Docker Hub

↓

docker pull

↓

Docker Container


```

---

### 학습 포인트

- Docker Hub는 Docker Image를 저장하는 Image Registry이다.
- Docker Hub를 이용하면 어느 환경에서도 동일한 Docker Image를 사용할 수 있다.
- GitHub는 Source Code를 저장하고 Docker Hub는 Docker Image를 저장한다.
- Docker Hub는 Kubernetes 및 GitOps 환경의 기반이 된다.

---

### 실무 TIP

실무에서는 Docker Hub보다 Amazon ECR, Azure Container Registry, Harbor와 같은 Private Registry를 사용하는 경우가 많다.

특히 기업 환경에서는 외부 공개를 방지하기 위해 Private Registry를 운영하는 것이 일반적이다.

---

### 운영 시 고려사항

Docker Hub는 Public Repository와 Private Repository를 모두 지원한다.

이번 프로젝트에서는 포트폴리오 및 학습 목적이므로 Public Repository를 사용하였다.

운영 환경에서는 Private Registry와 이미지 접근 권한을 함께 관리하는 것이 일반적이다.


## 8-6. Docker Build Context와 Docker Buildx

### Docker Build Context란?

Build Context는 Docker Image를 생성하기 위해 Docker Build에 전달되는 작업 디렉터리이다.

Docker Build는 Build Context 내부에 존재하는 파일만 사용할 수 있으며, Dockerfile과 애플리케이션 소스코드 역시 Build Context 안에 존재해야 한다.

이번 프로젝트에서는 Flask 애플리케이션이 `app` 디렉터리에 위치하고 있으므로 Build Context를 `./app`으로 지정하였다.

```yaml
context: ./app
```

---

### Build Context를 사용하는 이유

GitHub Hosted Runner는 Repository 전체를 다운로드하지만 Docker Build는 Repository 전체를 사용하는 것이 아니라 Build Context로 지정된 디렉터리만 Docker Engine으로 전달한다.

Build Context를 적절하게 지정하면 불필요한 파일이 Docker Build에 포함되지 않으므로 Build 시간이 단축되고 Docker Image 크기도 최소화할 수 있다.

이번 프로젝트에서는 Flask 애플리케이션과 Dockerfile만 포함되어 있는 `app` 디렉터리를 Build Context로 사용하였다.

---

### Docker Buildx란?

Docker Buildx는 Docker에서 제공하는 공식 Build 도구이다.

기존 `docker build` 명령보다 향상된 Build 기능을 제공하며 Multi-Platform Build, Build Cache, 병렬 Build 등 다양한 기능을 지원한다.

GitHub Actions에서는 Docker 공식 Action인 `docker/build-push-action` 내부에서 Docker Buildx를 이용하여 Docker Image를 생성한다.

---

### 이번 프로젝트에서 Buildx 역할

이번 프로젝트에서는 GitHub Hosted Runner가 Build Context를 Docker Buildx에 전달하였다.

Buildx는 Dockerfile을 읽어 Docker Image를 생성하고 Docker Hub에 Push하는 작업을 수행하였다.

사용자는 직접 Docker Buildx를 실행하지 않았지만 GitHub Actions 내부에서는 Buildx가 자동으로 동작하였다.

---

### Build 과정

```text
GitHub Repository

↓

Checkout

↓

Build Context (./app)

↓

Docker Buildx

↓

Docker Image 생성

↓

Docker Hub Push
```

---

### Build Context와 Dockerfile 관계

이번 프로젝트에서는 다음과 같이 Build Context와 Dockerfile 위치를 지정하였다.

```yaml
context: ./app

file: ./app/Dockerfile
```

- `context` : Docker Build에 전달할 작업 디렉터리
- `file` : 사용할 Dockerfile 위치

Build Context 내부에는 Flask 애플리케이션, Dockerfile, requirements.txt가 포함되어 있으므로 Docker Image 생성에 필요한 모든 파일을 사용할 수 있다.

---

### 학습 포인트

- Build Context는 Docker Build에 전달되는 작업 디렉터리이다.
- Docker Build는 Build Context 내부의 파일만 사용할 수 있다.
- Docker Buildx는 Docker 공식 Build 도구이다.
- GitHub Actions에서는 Buildx를 이용하여 Docker Image를 생성한다.
- Build Context를 최소화하면 Build 성능과 Docker Image 크기를 최적화할 수 있다.

---

### 실무 TIP

실무에서는 Build Context를 최소한으로 유지하기 위해 `.dockerignore`를 적극적으로 사용한다.

Build Context가 커질수록 Docker Engine으로 전달되는 파일이 많아져 Build 시간이 증가하므로 필요하지 않은 파일은 Build Context에서 제외하는 것이 일반적이다.

---

### 운영 시 고려사항

이번 프로젝트에서는 `app` 디렉터리만 Build Context로 지정하여 불필요한 Kubernetes Manifest, 문서, Git 파일 등이 Docker Image 생성 과정에 포함되지 않도록 구성하였다.

또한 GitHub Actions에서 Docker Buildx를 사용함으로써 동일한 Build 환경을 유지하고 Docker Image 생성 과정을 자동화하였다.


## 8-7. Docker Image Tag 관리 (latest, Semantic Version, Git SHA)

### Docker Image Tag란?

Docker Image Tag는 동일한 Docker Image를 구분하기 위한 버전 정보이다.

Docker Hub에는 하나의 Repository 안에 여러 개의 Docker Image를 저장할 수 있으며 Tag를 이용하여 각 Image를 구분한다.

대표적인 예는 다음과 같다.

```text
flask-api:latest

flask-api:v1.0.0

flask-api:v1.1.0

flask-api:a82f7c1
```

Tag를 이용하면 원하는 Docker Image를 선택하여 실행하거나 이전 버전으로 Rollback할 수 있다.

---

### latest Tag란?

`latest`는 Docker에서 가장 많이 사용하는 기본 Tag이다.

새로운 Docker Image를 Push하면 `latest` Tag가 최신 Docker Image를 가리키도록 변경된다.

이번 프로젝트에서는 GitHub Actions가 Docker Image를 Build한 후 다음과 같이 `latest` Tag를 부여하였다.

```yaml
tags: ${{ secrets.DOCKERHUB_USERNAME }}/flask-api:latest
```

이를 통해 항상 최신 Docker Image를 Docker Hub에서 사용할 수 있도록 구성하였다.

---

### 이번 프로젝트에서 latest를 사용한 이유

이번 프로젝트는 GitHub Actions를 이용한 CI Pipeline과 DAY4에서 구현할 ArgoCD 기반 GitOps 자동 배포 환경을 학습하는 것이 목적이다.

ArgoCD는 Docker Hub의 최신 Docker Image를 기준으로 Kubernetes Deployment를 자동 동기화하도록 구성할 예정이므로 이번 단계에서는 `latest` Tag를 사용하였다.

이를 통해 Git Push 이후 Docker Hub의 최신 Docker Image를 이용하여 자동 배포 환경을 구성할 수 있다.

---

### 운영 환경에서 latest만 사용하는 문제점

`latest`는 새로운 Docker Image가 Push될 때마다 기존 Image를 덮어쓰게 된다.

예를 들어

```text
DAY1

latest

↓

v1

────────────────────

DAY2

latest

↓

v2

────────────────────

DAY3

latest

↓

v3
```

항상 최신 Image만 남게 된다.

따라서 운영 환경에서는 장애가 발생했을 때 이전 Docker Image를 정확하게 선택하기 어렵다.

---

### Semantic Version

운영 환경에서는 Docker Image를 Semantic Version으로 관리하는 경우가 많다.

예를 들어

```text
v1.0.0

v1.1.0

v1.2.0
```

와 같이 관리하면 원하는 버전으로 쉽게 Rollback할 수 있다.

---

### Git Commit SHA Tag

최근 DevOps 환경에서는 Git Commit SHA를 Docker Image Tag로 사용하는 경우도 많다.

예를 들어

```text
flask-api:a82f7c1
```

과 같이 Git Commit과 Docker Image를 1:1로 연결하여 운영한다.

이 방식은 어떤 Source Code로 Docker Image가 생성되었는지 추적하기 쉽고 Rollback도 간단하게 수행할 수 있다는 장점이 있다.

---

### Tag 관리 전략

```text
Development

↓

latest

────────────────────

Release

↓

Semantic Version

────────────────────

Production

↓

Git Commit SHA
```

프로젝트 규모와 운영 환경에 따라 여러 Tag를 함께 사용하는 것이 일반적이다.

---

### 학습 포인트

- Docker Image Tag는 Docker Image 버전을 구분한다.
- `latest`는 가장 최근 Docker Image를 의미한다.
- 운영 환경에서는 `latest`만 사용하는 것을 권장하지 않는다.
- Semantic Version과 Git Commit SHA를 이용하여 Docker Image를 관리할 수 있다.
- Docker Image Tag는 Rollback 전략과 직접 연결된다.

---

### 실무 TIP

실무에서는 하나의 Docker Image에 여러 개의 Tag를 동시에 부여하는 경우가 많다.

예를 들어

```text
flask-api:latest

flask-api:v1.2.0

flask-api:a82f7c1
```

와 같이 관리하면 최신 버전, Release 버전, Git Commit을 모두 추적할 수 있다.

---

### 운영 시 고려사항

이번 프로젝트에서는 학습과 GitOps 자동 배포 환경 구성을 위해 `latest` Tag를 사용하였다.

향후 DAY6 DevSecOps 단계에서는 Git Commit SHA 기반 Immutable Tag 전략을 적용하여 보다 안정적인 운영 환경을 구성할 예정이다.



## 8-8. GitHub Hosted Runner와 Self-hosted Runner

### GitHub Hosted Runner란?

GitHub Hosted Runner는 GitHub에서 제공하는 관리형 실행 환경(Managed Runner)이다.

Workflow가 실행되면 GitHub가 Ubuntu, Windows, macOS 환경의 Virtual Machine을 자동으로 생성하고 Workflow를 실행한다.

Workflow 실행이 완료되면 Runner는 자동으로 삭제되므로 항상 동일한 초기 환경(Clean Environment)에서 Build가 수행된다.

이번 프로젝트에서는 `ubuntu-latest` Runner를 이용하여 Docker Build 및 Docker Hub Push를 수행하였다.

---

### Self-hosted Runner란?

Self-hosted Runner는 사용자가 직접 구축하고 운영하는 Runner이다.

EC2, 물리 서버, Virtual Machine 등에 GitHub Runner를 설치하여 Workflow를 실행할 수 있다.

기업 내부망이나 Private Network에 접근해야 하는 경우 주로 사용된다.

---

### GitHub Hosted Runner와 Self-hosted Runner 비교

| 항목 | GitHub Hosted Runner | Self-hosted Runner |
|------|----------------------|--------------------|
| 운영 주체 | GitHub | 사용자 |
| 서버 구축 | 불필요 | 필요 |
| 초기 환경 | 항상 동일 | 유지됨 |
| Workflow 종료 후 | 자동 삭제 | 계속 유지 |
| 내부망 접근 | 불가능 | 가능 |
| 유지보수 | GitHub | 사용자 |

---

### 이번 프로젝트에서 GitHub Hosted Runner를 선택한 이유

이번 프로젝트의 목적은 GitHub Actions 기반 CI Pipeline을 구축하고 Docker Image Build를 자동화하는 것이다.

별도의 CI 서버를 구축하지 않고도 GitHub에서 제공하는 Runner를 이용하여 Docker Build부터 Docker Hub Push까지 자동으로 수행할 수 있으므로 GitHub Hosted Runner를 선택하였다.

또한 항상 새로운 Ubuntu 환경에서 Workflow가 실행되므로 Build 환경의 일관성을 유지할 수 있다는 장점이 있다.

---

### Self-hosted Runner를 사용하는 경우

다음과 같은 환경에서는 Self-hosted Runner를 많이 사용한다.

- 사내망(Private Network)에 접근해야 하는 경우
- Kubernetes Cluster가 외부에서 접근되지 않는 경우
- 사내 Docker Registry를 사용하는 경우
- 내부 보안 정책상 외부 Runner를 사용할 수 없는 경우
- GPU Server 또는 고성능 Build Server를 사용하는 경우

---

### GitHub Hosted Runner 동작 과정

```text
Git Push

↓

GitHub Actions

↓

GitHub Hosted Runner 생성

↓

Workflow 실행

↓

Runner 삭제
```

---

### Self-hosted Runner 동작 과정

```text
Git Push

↓

GitHub Actions

↓

EC2(Self-hosted Runner)

↓

Workflow 실행

↓

Runner 유지
```

---

### 학습 포인트

- GitHub Hosted Runner는 GitHub가 관리하는 Runner이다.
- Self-hosted Runner는 사용자가 직접 구축하는 Runner이다.
- Hosted Runner는 Workflow 종료 후 자동 삭제된다.
- Self-hosted Runner는 서버를 계속 운영해야 한다.
- 기업 환경에서는 보안 정책에 따라 Self-hosted Runner를 사용하는 경우가 많다.

---

### 실무 TIP

최근에는 일반적인 Build와 Test는 GitHub Hosted Runner에서 수행하고,

운영 배포(Production Deploy)는 Self-hosted Runner에서 수행하는 Hybrid 구조를 많이 사용한다.

이를 통해 Build 환경은 GitHub가 관리하고, 운영 환경은 기업 내부 인프라에서 안전하게 관리할 수 있다.

---

### 운영 시 고려사항

이번 프로젝트에서는 GitHub Hosted Runner를 이용하여 Docker Build를 자동화하였다.

향후 Kubernetes Cluster가 Private Network 환경으로 변경되거나 내부 Docker Registry를 운영하게 되면 Self-hosted Runner를 구축하여 GitHub Actions와 연동하는 방식으로 확장할 수 있다.


# 9. 문제 해결 (Problem Solving)

DAY3에서는 GitHub Actions 기반 CI Pipeline을 구축하는 과정에서 몇 가지 문제가 발생하였다.

각 문제에 대해 원인을 분석하고 해결 과정을 정리하였다.

실제 프로젝트를 수행하면서 경험한 문제를 기반으로 작성하였으며, 이후 동일한 환경에서 GitHub Actions를 구축할 때 참고할 수 있도록 기록하였다.

---

## 9-1. GitHub Actions Workflow 경로 생성 오류

### 문제

GitHub Actions Workflow를 생성하는 과정에서 `.github/workflows` 디렉터리 내부에 동일한 디렉터리가 중첩 생성되는 문제가 발생하였다.

```text
.github
└── workflows
    └── .github
        └── workflows
            └── docker-build.yml
```

그 결과 GitHub가 Workflow 파일을 정상적으로 인식하지 못할 가능성이 있는 구조가 생성되었다.

---

### 원인 분석

현재 작업 디렉터리가 이미 `.github/workflows`인 상태에서 다시 상대경로(`.github/workflows/docker-build.yml`)를 사용하여 파일을 생성하였다.

Linux는 현재 작업 디렉터리를 기준으로 상대경로를 해석하므로 동일한 경로가 중첩 생성되었다.

---

### 해결 과정

잘못 생성된 `.github` 디렉터리를 삭제한 후 프로젝트 루트 기준으로 Workflow 파일을 다시 생성하였다.

```bash
rm -rf .github/workflows/.github
```

이후 디렉터리 구조를 확인하여 정상적으로 Workflow 파일이 존재하는 것을 확인하였다.

```text
.github
└── workflows
    └── docker-build.yml
```

---

### 결과

GitHub Actions가 Workflow 파일을 정상적으로 인식할 수 있는 구조로 수정하였다.

---

### 배운 점

상대경로를 사용할 때는 현재 작업 디렉터리를 반드시 확인해야 한다.

Workflow 파일은 반드시 `.github/workflows` 디렉터리 바로 아래에 위치해야 GitHub Actions가 자동으로 인식한다.

---

## 9-2. Windows에서 Feature Branch 조회 실패

### 문제

EC2에서 Feature Branch를 Push한 이후 Windows 환경에서 해당 Branch를 Checkout하려고 하였으나 Branch를 찾을 수 없다는 오류가 발생하였다.

---

### 원인 분석

EC2에서는 이미 원격 저장소(Remote Repository)에 Feature Branch가 Push된 상태였지만 Windows Git은 아직 원격 Branch 정보를 가져오지 않은 상태였다.

따라서 Windows 로컬 Git은 새로운 Branch가 생성된 사실을 알지 못하였다.

---

### 해결 과정

원격 Branch 정보를 다시 가져오기 위해 다음 명령을 수행하였다.

```bash
git fetch origin
```

이후 Feature Branch를 정상적으로 Checkout하였다.

---

### 결과

Windows와 GitHub Repository가 동일한 Branch 정보를 가지게 되었으며 이후 문서 작업을 정상적으로 수행할 수 있었다.

---

### 배운 점

다른 개발 환경에서 새로운 Branch를 생성한 경우에는 `git fetch`를 수행하여 원격 Branch 정보를 먼저 동기화하는 것이 필요하다.

---

## 9-3. Docker Hub 인증 정보 구성

### 문제

GitHub Actions Workflow 작성 과정에서 Docker Hub 인증 정보의 Secret 이름을 잘못 참조하여 Docker Login 단계가 정상적으로 수행되지 않을 가능성이 있었다.

---

### 원인 분석

Workflow에서는 Secret 이름을 정확하게 일치시켜야 한다.

Repository Secrets에는 `DOCKERHUB_TOKEN`으로 등록하였지만 Workflow에서는 다른 이름을 참조하고 있었다.

---

### 해결 과정

Workflow를 수정하여 Repository Secrets와 동일한 이름을 참조하도록 변경하였다.

```yaml
username: ${{ secrets.DOCKERHUB_USERNAME }}

password: ${{ secrets.DOCKERHUB_TOKEN }}
```

이후 GitHub Actions Workflow를 다시 실행하여 Docker Hub 인증이 정상적으로 수행되는 것을 확인하였다.

---

### 결과

GitHub Hosted Runner가 Docker Hub에 정상적으로 로그인하였으며 Docker Image Build 및 Push가 정상적으로 수행되었다.

---

### 배운 점

GitHub Actions Workflow에서 사용하는 Secret 이름은 Repository Secrets와 완전히 동일해야 한다.

Secret 이름이 하나라도 다르면 인증이 실패하므로 Workflow 작성 시 Secret 이름을 정확하게 확인하는 습관이 중요하다.

# 10. DAY3 회고

DAY3에서는 GitHub Actions를 이용하여 Docker Image Build와 Docker Hub Push를 자동화하는 CI(Continuous Integration) Pipeline을 구축하였다.

기존에는 Docker Image를 직접 Build하고 Docker Hub에 Push하는 과정을 수동으로 수행하였다.

이번에는 Git Push만으로 GitHub Hosted Runner가 Docker Image를 Build하고 Docker Hub에 자동으로 Push하도록 구성하여 Build 과정을 표준화하고 자동화하였다.

또한 Docker Hub에 업로드된 Docker Image를 다시 Pull하여 Container 실행까지 검증함으로써 GitHub Actions가 생성한 결과물이 실제 운영 가능한 상태임을 확인하였다.

이번 DAY3를 통해 GitHub Actions Workflow뿐 아니라 Workflow, Job, Step, Runner, GitHub Secrets, Docker Hub, Build Context 등 CI를 구성하는 핵심 요소들의 동작 원리를 이해할 수 있었다.

---

## 잘된 점

- GitHub Actions 기반 CI Pipeline을 성공적으로 구축하였다.
- Docker Hub와 GitHub Actions를 연동하여 Docker Image Build를 자동화하였다.
- GitHub Hosted Runner 기반 Build 환경을 구성하였다.
- Docker Hub Image Pull 및 Container 실행까지 검증하였다.
- Git Push만으로 Docker Image Build부터 Docker Hub Push까지 자동 수행되는 환경을 구축하였다.

---

## 아쉬운 점

- GitHub Actions Workflow 디렉터리 생성 과정에서 상대경로를 잘못 사용하여 Workflow 경로가 중첩 생성되는 문제가 발생하였다.
- Docker Hub 인증 정보(Repository Secrets) 구성 과정에서 Secret 이름을 정확하게 확인하는 과정이 필요하였다.
- GitHub Hosted Runner 내부 동작 구조를 처음 접하면서 Workflow 실행 과정을 이해하는 데 시간이 소요되었다.

---

## 개선할 점

- Docker Image Tag를 Git Commit SHA 및 Semantic Version 기반으로 관리하도록 개선한다.
- GitHub Actions 내부에 Security Scan과 Test 단계를 추가하여 CI Pipeline을 고도화한다.
- Build Cache를 활용하여 Docker Build 시간을 단축한다.
- 이후 ArgoCD를 연동하여 GitOps 기반 CD(Continuous Deployment)를 구축한다.

---

## DAY3 핵심 성과

- GitHub Actions Workflow 구축 완료
- GitHub Hosted Runner 기반 CI Pipeline 구축 완료
- Docker Hub Repository 구축 완료
- Docker Image 자동 Build 완료
- Docker Hub 자동 Push 완료
- Docker Hub Image Pull 검증 완료
- Docker Container 실행 검증 완료

---

## 이번 프로젝트에서 가장 크게 배운 점

CI는 단순히 Build를 자동화하는 기능이 아니라, 개발자가 수행하던 Build 과정을 표준화하고 항상 동일한 환경에서 반복 수행할 수 있도록 만드는 자동화 기술이라는 것을 이해하였다.

또한 GitHub Hosted Runner가 매번 새로운 Ubuntu 환경을 생성하여 Workflow를 수행한다는 점과 Docker Hub를 이용하여 Build 결과를 중앙에서 관리하는 구조를 직접 구축하면서 DevOps 환경의 전체 흐름을 이해할 수 있었다.


# 11. DAY4 계획

DAY4에서는 GitHub Actions로 생성한 Docker Image를 Kubernetes 환경에 자동으로 배포하기 위한 GitOps 기반 CD(Continuous Deployment) 환경을 구축한다.

DAY3에서 구축한 CI Pipeline과 Docker Hub를 기반으로 ArgoCD를 설치하고 Git Repository를 Single Source of Truth로 사용하는 GitOps 구조를 구현할 예정이다.

---

## DAY4 목표

- ArgoCD 설치
- GitOps 기반 CD 구축
- Docker Hub Image 자동 배포
- Kubernetes Deployment 자동 동기화
- GitHub Actions와 ArgoCD 연계
- GitOps 기반 자동 배포 검증

---

## DAY4 산출물

- ArgoCD 구축
- GitOps Repository 연동
- Kubernetes 자동 동기화
- GitHub Actions → Docker Hub → ArgoCD → Kubernetes 자동 배포 환경 구축
- DAY4.md 작성
- README 업데이트
- Master Document v1.4 업데이트

---

## DAY4에서 중점적으로 학습할 내용

- GitOps
- ArgoCD
- Sync
- Desired State
- Continuous Deployment(CD)
- Declarative Infrastructure
- Kubernetes Manifest 자동 동기화

---

## DAY4 완료 목표

GitHub Actions에서 생성한 Docker Image를 ArgoCD가 자동으로 감지하여 Kubernetes Deployment를 동기화하는 GitOps 기반 CD 환경을 구축한다.