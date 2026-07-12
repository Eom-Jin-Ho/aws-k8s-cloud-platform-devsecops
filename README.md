# AWS 기반 Kubernetes Cloud Platform 구축 및 DevSecOps 보안 자동화

<p align="center">

![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

</p>

<p align="center">

![ArgoCD](https://img.shields.io/badge/ArgoCD-EF7B4D?style=for-the-badge)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)

</p>

---

## 프로젝트 소개

본 프로젝트는 AWS EC2 환경에서 Kubernetes(Minikube) 기반 Cloud Platform을 직접 구축하고 운영하는 개인 프로젝트입니다.

Docker 기반 컨테이너 환경을 시작으로 Kubernetes Cluster를 구축하고, GitHub Actions(CI)와 ArgoCD(GitOps CD)를 연계하여 **Git Push만으로 Kubernetes 환경이 자동으로 동기화되는 GitOps 기반 CI/CD 파이프라인**을 구현하였습니다.

또한 Prometheus/Grafana를 이용한 Monitoring 플랫폼과 Trivy 기반 Security Scan, Kubernetes Secret, ConfigMap, NetworkPolicy를 적용하여 DevSecOps 보안 자동화 환경까지 직접 구축하였습니다.

단순한 애플리케이션 배포가 아닌 **클라우드 플랫폼 구축 · Kubernetes 운영 · Monitoring · CI/CD 자동화 · GitOps · DevSecOps 보안 자동화** 전 과정을 직접 구현하는 것을 목표로 합니다.

---

# 프로젝트 목표

- Kubernetes 기반 Cloud Platform 구축
- Docker 기반 컨테이너 환경 구축
- GitHub Actions 기반 CI 자동화
- ArgoCD 기반 GitOps CD 구축
- Prometheus / Grafana 모니터링 구축
- DevSecOps 보안 자동화 구축
- Container Image Security Scan 자동화
- Kubernetes 보안 구성(Security Hardening)
- Self-Healing 검증

---

# 프로젝트 운영 전략

## Git Workflow

```text
Windows
        │
        ▼
GitHub
        ▲
        │
EC2
```

- Windows : README, 문서, 스크린샷 관리
- EC2 : 애플리케이션 코드 및 Docker/Kubernetes 구축
- GitHub : Source of Truth

### Branch Strategy

main
        │
feature/dayX
        │
Implement
        │
Commit
        │
Push
        │
Documentation
        │
Merge
        ▼
main

---

# 설계 의사결정 (Design Decisions)

## 왜 EC2를 선택했는가?

Amazon EKS를 바로 사용하는 대신 EC2 기반에서 Kubernetes를 직접 구축하여 클러스터 구성과 운영 원리를 이해하는 것을 목표로 하였습니다.

---

## 왜 Minikube를 선택했는가?

관리형 Kubernetes 서비스(EKS)보다 Kubernetes의 동작 원리를 학습하고 직접 구축하기 위해 Minikube를 선택하였습니다.

향후에는 동일한 구성을 Amazon EKS로 확장할 계획입니다.

---

## 왜 GitHub Actions를 선택했는가?

GitHub Repository와 자연스럽게 연동되며 코드 변경 시 자동으로 Docker 이미지를 빌드하고 Docker Hub에 Push하는 CI 환경을 구축하기 위함입니다.

---

## 왜 ArgoCD를 선택했는가?

Git Repository를 Single Source of Truth로 사용하는 GitOps 방식을 구현하기 위해 선택하였습니다.

---

## 왜 Prometheus / Grafana를 선택했는가?

Kubernetes 환경에서 가장 널리 사용되는 오픈소스 모니터링 플랫폼이며 Pod 상태, CPU, Memory 등을 실시간으로 확인하기 위해 선택하였습니다.

---

## 왜 Trivy를 선택했는가?

Docker Image의 취약점을 자동으로 검사하여 DevSecOps 파이프라인에 보안 검사를 포함하기 위해 선택하였습니다.

---

## 왜 Kubernetes Secret을 선택했는가?

애플리케이션 코드와 민감한 설정 정보를 분리하기 위해 Kubernetes Secret을 적용하였습니다.

실제 운영 환경에서는 AWS Secrets Manager, HashiCorp Vault 등을 사용하지만 본 프로젝트에서는 Kubernetes Secret의 동작 원리와 환경 변수 주입 방식을 검증하는 것을 목표로 하였습니다.

---

## 왜 ConfigMap을 선택했는가?

애플리케이션의 일반 설정(LOG_LEVEL, APP_REGION 등)을 코드와 분리하여 관리하기 위해 ConfigMap을 적용하였습니다.

이를 통해 운영 환경에서 설정 변경 시 애플리케이션 이미지를 다시 빌드하지 않아도 되는 구조를 구현하였습니다.

---

## 왜 NetworkPolicy를 선택했는가?

Kubernetes Pod 간 통신을 최소 권한 원칙(Least Privilege)에 따라 제어하기 위해 NetworkPolicy를 적용하였습니다.

Calico CNI를 이용하여 실제 통신 허용 및 차단을 검증하였으며, 허용된 Pod만 접근 가능한 화이트리스트 기반 정책을 구현하였습니다.

---



# 프로젝트 진행 현황

| Day | 내용 | 상태 |
|------|------|------|
| Day1 | AWS EC2 / Docker / Flask | ✅ 완료 |
| Day2 | Kubernetes Cluster / Deployment / Service | ✅ 완료 |
| Day3 | GitHub Actions CI / Docker Hub | ✅ 완료 |
| Day4 | ArgoCD GitOps / Continuous Delivery | ✅ 완료 |
| Day5 | Prometheus / Grafana Monitoring | ✅ 완료 |
| Day6 | DevSecOps Security | ✅ 완료 |
| Day7 | Documentation & Portfolio | ⚪ 예정 |

---

# 프로젝트 아키텍처

> 프로젝트 완료 후 draw.io Architecture Diagram을 추가할 예정입니다.

```text
Developer

↓

Git Push

↓

GitHub Repository

↓

GitHub Actions (CI)

↓

Docker Build

↓

Trivy Security Scan

↓

Security Gate

↓

Docker Hub

↓

ArgoCD (GitOps CD)

↓

Kubernetes (Minikube)

        │

 ┌──────┴─────────────┐
 │                    │

Application       Monitoring

 │                    │

Deployment      Node Exporter

 │              kube-state-metrics

Pod (Flask)            │

        └──────────────┘

               │

          Prometheus

               │

           Grafana

               │

      Monitoring Dashboard
```

---

# 프로젝트 디렉터리 구조

```text
aws-k8s-cloud-platform-devsecops/

├── app/
├── k8s/
├── .github/
├── argocd/
├── monitoring/
├── scripts/
├── docs/
├── README.md
├── LICENSE
└── .gitignore
```

---

# 개발 환경

| 항목 | 내용 |
|------|------|
| OS | Ubuntu 24.04 LTS |
| Cloud | AWS EC2 (t3.medium → t3.large) |
| Storage | Amazon EBS 20GB (gp3) |
| Container Runtime | Docker CE |
| Kubernetes | Minikube v1.38.1 |
| CLI | kubectl v1.36 |
| IDE | VS Code Remote SSH |
| SCM | Git / GitHub |
| CI | GitHub Actions |
| Git Workflow | Feature Branch Strategy |
| Security Scan | Trivy v0.72.0 |
| CNI | Calico |

---

# DAY1

## 구현 목표

- AWS EC2(Ubuntu) 환경 구축
- Docker Engine 설치
- Docker 공식 Repository 구성
- Flask API 개발
- Docker Image 생성
- Docker Container 실행
- Flask API 외부 접속 확인

---

## 구현 결과

✅ AWS EC2 생성

✅ GitHub Repository 생성

✅ Remote SSH 환경 구축

✅ Docker 공식 Repository 등록

✅ Docker Engine 설치

✅ Docker 권한 설정

✅ Flask API 개발

✅ Docker Image 생성

✅ Docker Container 실행

✅ Flask API 외부 접속 성공

---

## 주요 구현 결과

![Docker Engine Installation](docs/screenshots/day1/08-docker-engine-installation.jpg)

![Flask Container Running](docs/screenshots/day1/15-flask-container-running.jpg)

![Flask API Response Success](docs/screenshots/day1/17-flask-api-response-success.jpg)

---

## Git Commit

```text
feat(init): initialize project structure and documentation

feat(day1): add flask api and dockerfile
```

---

## DAY1 회고

Docker 설치부터 Flask API 컨테이너 실행까지의 전체 과정을 직접 구축하였다.

Docker 공식 Repository를 사용하여 최신 Docker Engine을 설치하였으며, Docker Permission 문제를 해결하면서 Linux Group Permission 구조를 함께 이해하였다.

또한 Remote SSH 기반 개발 환경을 구축하여 로컬 Windows와 EC2를 GitHub를 중심으로 연동하는 개발 환경을 구성하였다.



# DAY2

## 구현 목표

- GitHub SSH 인증 전환
- Feature Branch 전략 적용
- Minikube 설치
- kubectl 설치
- Kubernetes Cluster 구축
- Deployment 생성
- Service(NodePort) 생성
- Flask API를 Kubernetes Pod 환경으로 이전
- Kubernetes Self-Healing 검증

---

## 구현 결과

✅ GitHub SSH 인증 전환

✅ Feature Branch 전략 적용

✅ Minikube 설치

✅ kubectl 설치

✅ AWS EBS 20GB 온라인 확장

✅ Linux FileSystem 확장

✅ Kubernetes Cluster 구축

✅ Node Ready 확인

✅ Deployment 생성

✅ ReplicaSet 생성

✅ Pod 생성

✅ Service(NodePort) 생성

✅ Kubernetes Self-Healing 확인

✅ Kubernetes Service를 통한 Flask API 응답 확인

✅ Kubernetes ImagePull 오류 해결

## 주요 구현 결과

![Kubernetes Cluster Created](docs/screenshots/day2/10-kubernetes-cluster-created.jpg)

![Kubernetes Node Ready](docs/screenshots/day2/11-kubernetes-node-ready.jpg)

![Kubernetes Pod Running](docs/screenshots/day2/14-kubernetes-pod-running.jpg)

![Kubernetes Service Flask Response](docs/screenshots/day2/15-kubernetes-service-flask-response.jpg)

## Git Commit

```text
feat(day2): build kubernetes deployment and service
```

## DAY2 회고

Docker 환경에서 실행되던 Flask 애플리케이션을 Kubernetes 환경으로 이전하였다.

Minikube 기반 Kubernetes Cluster를 구축하고 Deployment, ReplicaSet, Pod, Service를 직접 구성하였다.

또한 AWS EBS 온라인 확장과 Linux 파일시스템 확장을 경험하였으며, ImagePull 오류를 해결하면서 Docker Image와 Kubernetes 이미지 관리 방식의 차이를 이해할 수 있었다.


# DAY3

## 구현 목표

- GitHub Actions CI Pipeline 구축
- Docker Hub Repository 생성
- GitHub Secrets 등록
- Docker Image 자동 Build
- Docker Image 자동 Push
- Docker Hub Image 검증

---

## 구현 결과

✅ Docker Hub Repository 생성

✅ GitHub Secrets 등록

✅ GitHub Actions Workflow 작성

✅ Docker Build 자동화

✅ Docker Hub Push 성공

✅ Docker Pull 검증

✅ Docker Container 실행 검증

✅ GitHub Hosted Runner 기반 CI Pipeline 검증



## CI Pipeline

```text
Developer

↓

Git Push

↓

GitHub Repository

↓

GitHub Actions

↓

Docker Build

↓

Docker Push

↓

Docker Hub

↓

Image Validation
```



## 주요 구현 결과

![GitHub Actions Workflow Success](docs/screenshots/day3/14-github-actions-workflow-success.jpg)

![GitHub Actions Job Result](docs/screenshots/day3/15-github-actions-job-result.jpg)

![Docker Hub Image Pushed](docs/screenshots/day3/16-dockerhub-image-pushed.jpg)

![Docker Hub Image Pull Validation](docs/screenshots/day3/17-dockerhub-image-pull-validation.jpg)

## Git Commit

```text
feat(day3): configure github actions ci pipeline
docs(day3): update documentation
```


## DAY3 회고

GitHub Actions 기반 CI Pipeline을 구축하여 Git Push만으로 Docker Image Build와 Docker Hub Push가 자동으로 수행되는 환경을 구성하였다. 또한 Docker Hub에서 이미지를 다시 Pull하여 컨테이너 실행까지 검증함으로써 CI 결과물이 실제 운영 가능한 상태임을 확인하였다.


# DAY4

## 구현 목표

- ArgoCD 설치
- Git Repository 연동
- GitOps 기반 Continuous Delivery(CD) 구축
- Kubernetes Application 생성
- Manual Sync 검증
- Auto Sync 검증
- Git 변경 시 Kubernetes 자동 반영 검증

---

## 구현 결과

✅ ArgoCD 설치

✅ ArgoCD Dashboard 구성

✅ Git Repository 연동

✅ Kubernetes Application 생성

✅ Manual Sync 검증

✅ Auto Sync 구성

✅ Git 변경 자동 감지

✅ Kubernetes Deployment 자동 변경

✅ Replica 변경 자동 반영 검증

---

## GitOps Architecture

```text
Developer

↓

Git Push

↓

GitHub Repository

↓

GitHub Actions

↓

Docker Hub

↓

ArgoCD

↓

Sync

↓

Deployment

↓

ReplicaSet

↓

Pod
```

---

## 주요 구현 결과

![ArgoCD Installed](docs/screenshots/day4/02-argocd-installed.jpg)

![ArgoCD Login](docs/screenshots/day4/07-argocd-login-page.jpg)

![ArgoCD Dashboard](docs/screenshots/day4/09-argocd-dashboard.jpg)

![Git Repository Connected](docs/screenshots/day4/10-git-repository-connected.jpg)

![Application Created](docs/screenshots/day4/11-application-created.jpg)

![Manual Sync Success](docs/screenshots/day4/12-manual-sync-success.jpg)

![Auto Sync Enabled](docs/screenshots/day4/18-auto-sync-enabled.jpg)

![GitOps Sync Completed](docs/screenshots/day4/17-gitops-sync-completed.jpg)

![Kubernetes Pods Auto Updated](docs/screenshots/day4/19-kubernetes-pods-auto-updated.jpg)

---

## Git Commit

```text
feat(day4): implement argocd gitops cd pipeline
```

---

## DAY4 회고

ArgoCD를 구축하여 Git Repository를 Single Source of Truth로 사용하는 GitOps 기반 Continuous Delivery 환경을 구현하였다.

GitHub Repository와 Kubernetes Cluster를 연결하고 Kubernetes Application을 생성하여 Manual Sync와 Auto Sync를 모두 검증하였다.

Git Manifest 변경 시 Kubernetes Deployment와 Pod가 자동으로 변경되는 과정을 직접 확인하면서 GitOps 기반 운영 방식의 동작 원리를 이해할 수 있었다.

또한 Target Revision을 Feature Branch로 변경하여 Git Branch별 GitOps 운영 방식을 검증하였으며, ArgoCD의 Desired State와 Actual State 동기화 과정을 직접 확인하였다.


# DAY5

## 구현 목표

- Monitoring Namespace 생성
- Helm 설치
- Prometheus 구축
- Grafana 구축
- Node Exporter 구축
- kube-state-metrics 구축
- Kubernetes Monitoring 구축
- Grafana Dashboard 검증

---

## 구현 결과

✅ Monitoring Namespace 생성

✅ Helm 설치

✅ Prometheus Community Repository 등록

✅ kube-prometheus-stack 설치

✅ Prometheus 구축

✅ Grafana 구축

✅ Prometheus Operator 구축

✅ Node Exporter 구축

✅ kube-state-metrics 구축

✅ Kubernetes Cluster Monitoring

✅ Kubernetes Node Monitoring

✅ Grafana Dashboard 검증

✅ Kubernetes API Server 장애 해결

---

## Monitoring Architecture

```text
             Kubernetes Cluster

          ┌────────┴────────┐
          │                 │

     Linux Node      Kubernetes API

          │                 │

   Node Exporter   kube-state-metrics

          └────────┬────────┘

                   │

              Prometheus

                   │

               Grafana

                   │

              Dashboard

                   │

              Administrator
```

---

## 주요 구현 결과

![Monitoring Pods Ready](docs/screenshots/day5/10-monitoring-pods-ready.jpg)

![Grafana Dashboard](docs/screenshots/day5/18-grafana-dashboard.jpg)

![Kubernetes Cluster Dashboard](docs/screenshots/day5/19-kubernetes-cluster-dashboard.jpg)

![Kubernetes Node Dashboard](docs/screenshots/day5/20-kubernetes-node-dashboard.jpg)

![Monitoring Final Verification](docs/screenshots/day5/21-monitoring-final-verification.jpg)

---

## Git Commit

```text
feat(day5): implement kubernetes monitoring platform

docs(day5): update monitoring documentation
```

---

## DAY5 회고

Prometheus와 Grafana를 이용하여 Kubernetes Monitoring 플랫폼을 구축하였다.

Node Exporter와 kube-state-metrics를 이용해 Kubernetes Cluster와 Node의 상태를 실시간으로 수집하고 Grafana Dashboard를 통해 시각화하였다.

또한 Monitoring Stack 구축 과정에서 Kubernetes API Server 장애를 직접 분석하고 EC2 인스턴스를 증설하여 문제를 해결하면서 실제 운영 환경에서 발생할 수 있는 장애 대응 경험을 수행하였다.

이를 통해 구축(Build) 중심의 프로젝트를 운영(Operation) 단계까지 확장할 수 있었다.

---

# DAY6

## 구현 목표

- Trivy 설치
- Docker Image 취약점 분석
- GitHub Actions Security Scan
- Security Gate 적용
- Kubernetes Secret 적용
- ConfigMap 적용
- NetworkPolicy 적용
- DevSecOps 보안 자동화 구축

---


## 구현 결과

✅ Trivy 설치

✅ Docker Image 취약점 분석

✅ GitHub Actions Security Scan

✅ Security Gate 적용

✅ HIGH / CRITICAL 취약점 차단

✅ GitHub Actions Workflow 차단 검증

✅ Kubernetes Secret 적용

✅ ConfigMap 적용

✅ NetworkPolicy 적용

✅ Calico CNI 기반 NetworkPolicy 검증

✅ DevSecOps 보안 자동화 구축

---

## DevSecOps Architecture

```text
Developer

↓

Git Push

↓

GitHub Repository

↓

GitHub Actions

↓

Docker Build

↓

Trivy Scan

↓

Security Gate

↓

Docker Hub

↓

ArgoCD

↓

Kubernetes

        │

Secret

ConfigMap

NetworkPolicy

↓

Pod (Flask)
```
---

## 주요 구현 결과

![Trivy Image Scan Result](docs/screenshots/day6/09-trivy-image-scan-result.jpg)

![Security Gate Blocked Workflow](docs/screenshots/day6/18-trivy-security-gate-blocked-workflow.jpg)

![Secret Environment Variable Verified](docs/screenshots/day6/28-secret-environment-variable-verified.jpg)

![ConfigMap Environment Variable Verified](docs/screenshots/day6/34-configmap-environment-variable-verified.jpg)

![NetworkPolicy Connection Success](docs/screenshots/day6/41-approved-client-networkpolicy-connection-success.jpg)

---

## Git Commit

```text
feat(day6): implement devsecops security automation
```
---

## DAY6 회고

DAY6에서는 DevSecOps 관점에서 Kubernetes 보안 자동화 환경을 구축하였다.

Trivy를 이용하여 Docker Image 취약점을 분석하고 GitHub Actions에 Security Scan과 Security Gate를 추가하여 HIGH 및 CRITICAL 취약점이 존재하는 이미지는 자동으로 배포되지 않도록 구성하였다.

또한 Kubernetes Secret과 ConfigMap을 적용하여 애플리케이션 설정과 민감한 정보를 분리하였으며, NetworkPolicy를 이용하여 Pod 간 통신을 최소 권한 원칙에 따라 제어하였다.

특히 Calico CNI를 적용하여 NetworkPolicy가 실제로 트래픽을 차단하고 허용하는 과정을 직접 검증함으로써 단순한 리소스 생성이 아닌 보안 정책의 실제 동작까지 확인하였다.

또한 NetworkPolicy는 Kubernetes만으로 동작하는 것이 아니라 Calico CNI가 실제 패킷을 제어한다는 점을 직접 검증하면서 Kubernetes 네트워크 보안 구조를 이해할 수 있었다.

이를 통해 기존 CI/CD 파이프라인에 보안(Security)을 통합한 DevSecOps 환경을 완성하였다.


# 현재까지 구현 흐름

```text
DAY1

AWS EC2

↓

Docker

↓

Flask

────────────────────────

DAY2

Docker

↓

Kubernetes

↓

Deployment

↓

Service

────────────────────────

DAY3

Git Push

↓

GitHub Actions

↓

Docker Hub

↓

Image Validation

────────────────────────

DAY4

Git Push

↓

GitHub Actions

↓

Docker Hub

↓

ArgoCD Auto Sync

↓

Deployment

↓

ReplicaSet

↓

Pod

────────────────────────

DAY5

Pod

        │

 ┌──────┴──────┐
 │             │

Node Exporter

kube-state-metrics

        │

Prometheus

        │

Grafana

        │

Monitoring Dashboard

────────────────────────

DAY6

Git Push

↓

GitHub Actions

↓

Trivy Security Scan

↓

Security Gate

↓

Docker Hub

↓

ArgoCD

↓

Kubernetes

↓

Secret

↓

ConfigMap

↓

NetworkPolicy


```


# Next Step

DAY7에서는 다음 내용을 진행할 예정입니다.

- README 최종 정리
- Master Document v1.6 작성
- DAY6.md 작성
- 면접 예상 질문 정리
- 프로젝트 최종 리팩토링
