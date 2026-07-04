# DAY2 - Kubernetes 기반 Cloud Platform 구축

---

# 1. DAY2 목표

DAY2의 목표는 Docker 환경에서 실행 중인 Flask 애플리케이션을 Kubernetes 환경으로 이전하고, Minikube 기반 Kubernetes Cluster를 직접 구축하는 것이다.

또한 Deployment와 Service를 이용하여 컨테이너를 오케스트레이션하고, Pod의 Self-Healing 기능을 직접 검증하는 것을 목표로 한다.

추가로 GitHub SSH 인증 방식 적용, Feature Branch 운영 전략 도입, AWS EBS 온라인 확장 등을 통해 실제 운영 환경과 유사한 Kubernetes 개발 환경을 구축하는 것을 목표로 한다.

---

# 2. DAY2 완료 목표

- GitHub SSH 인증 전환
- Feature Branch 전략 적용
- Minikube 설치
- kubectl 설치
- AWS EBS 20GB 온라인 확장
- Linux FileSystem 확장
- Kubernetes Cluster 구축
- Deployment 생성
- ReplicaSet 생성
- Pod 생성
- Service(NodePort) 생성
- Flask API Kubernetes 이전
- Kubernetes Self-Healing 검증

---

# 3. 구축 환경

| 항목 | 내용 |
|------|------|
| Cloud | AWS EC2 (t3.medium) |
| OS | Ubuntu 24.04 LTS |
| Container Runtime | Docker CE |
| Kubernetes | Minikube v1.38.1 |
| CLI | kubectl v1.36 |
| Storage | Amazon EBS 20GB (gp3) |
| IDE | VS Code Remote SSH |
| SCM | Git / GitHub (Feature Branch Strategy) |

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

Minikube

        │

Kubernetes Cluster

        │

Deployment

        │

ReplicaSet

        │

Pod

        │

Service (NodePort)

        │

Flask API
```

---

# 5. DAY2에서 구현한 기능

- GitHub SSH 인증 전환
- Feature Branch 전략 적용
- Minikube 설치
- kubectl 설치
- AWS EBS 20GB 온라인 확장
- Linux FileSystem 확장
- Kubernetes Cluster 구축
- Deployment 생성
- ReplicaSet 생성
- Pod 생성
- Service(NodePort) 생성
- Flask API Kubernetes 이전
- Kubernetes Self-Healing 검증

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
│   ├── deployment.yaml
│   └── service.yaml
│
├── argocd
├── monitoring
├── docs
│
└── README.md
```

---

# 7. 구축 과정

DAY2에서는 Docker 환경에서 실행 중인 Flask 애플리케이션을 Kubernetes 환경으로 이전하였다.

GitHub SSH 인증 방식을 적용하고 Feature Branch 기반 Git 운영 전략을 도입하였으며, Minikube와 kubectl을 이용하여 Kubernetes Cluster를 구축하였다.

또한 Deployment와 Service를 생성하여 Flask API를 Kubernetes Pod 환경에서 실행하였고, Pod 삭제를 통해 Kubernetes의 Self-Healing 기능을 직접 검증하였다.

구축 과정에서 AWS EBS 용량 부족 문제와 Kubernetes ImagePull 오류를 해결하며 실제 운영 환경에서 발생할 수 있는 문제 해결 경험도 함께 수행하였다.


## 7-1. GitHub SSH 인증 전환

### 배경

DAY1에서는 GitHub Personal Access Token(PAT)을 이용하여 GitHub Repository와 연동하였다.

PAT 방식은 Push 시 인증 정보를 관리해야 하므로 장기적인 프로젝트 운영에는 불편한 점이 있었다.

DAY2부터는 보다 안전하고 편리한 Git 운영을 위해 SSH Key 기반 인증 방식으로 변경하였다.

---

### 목적

GitHub와 EC2 간의 인증 방식을 SSH Key 기반으로 변경하여 안전하고 효율적인 Git 개발 환경을 구축한다.

---

### 사용 명령어

```bash
ssh-keygen -t ed25519 -C "GitHub Email"

cat ~/.ssh/id_ed25519.pub

ssh -T git@github.com

git remote set-url origin git@github.com:Eom-Jin-Ho/aws-k8s-cloud-platform-devsecops.git

git fetch
```

---

### 실행 결과

SSH Key를 생성한 후 GitHub에 Public Key를 등록하였다.

이후 Git Remote를 HTTPS에서 SSH 방식으로 변경하였으며 `ssh -T`와 `git fetch`를 통해 정상적으로 인증되는 것을 확인하였다.

---

### 캡처

![alt text](<1. ssh -T.jpg>)

![alt text](<2. git remote -v.jpg>)



## 7-2. Feature Branch 전략 적용

### 배경

DAY1에서는 main 브랜치에서 직접 개발을 진행하였다.

그러나 실제 개발 환경에서는 기능 단위로 Branch를 생성한 후 Merge하는 방식이 일반적이므로 DAY2부터 Feature Branch 전략을 적용하였다.

---

### 목적

기능별 개발 이력을 분리하고 안정적인 Git Workflow를 구축한다.

---

### 사용 명령어

```bash
git checkout -b feature/day2-kubernetes

git push -u origin feature/day2-kubernetes
```

---

### 실행 결과

DAY2 작업을 위한 `feature/day2-kubernetes` 브랜치를 생성하였다.

이후 모든 Kubernetes 관련 개발은 Feature Branch에서 진행하고, 문서 작성 완료 후 Main Branch로 Merge하는 방식으로 운영하였다.

---

### 캡처

![alt text](<3. feature branch.jpg>)

![alt text](<4. git branch.jpg>)

![alt text](<5. git push -u origin feature.jpg>)


## 7-3. Minikube 설치

### 배경

Docker 환경은 구축되었지만 Kubernetes Cluster는 아직 존재하지 않는 상태였다.

Kubernetes를 직접 구축하고 운영 원리를 학습하기 위해 Minikube를 설치하였다.

관리형 Kubernetes 서비스(Amazon EKS)를 바로 사용하는 대신 단일 Node 기반의 Minikube 환경을 구성하여 Kubernetes의 핵심 동작 방식을 먼저 이해하는 것을 목표로 하였다.

---

### 목적

Minikube를 설치하여 Kubernetes Cluster를 구축할 수 있는 기반 환경을 구성한다.

---

### 사용 명령어

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

sudo install minikube-linux-amd64 /usr/local/bin/minikube

minikube version
```

---

### 실행 결과

Minikube를 정상적으로 설치하였으며 Version 정보를 통해 설치가 정상적으로 완료된 것을 확인하였다.

---

### 캡처

![alt text](<6. Minikube 설치 및 Version 확인.jpg>)



## 7-4. kubectl 설치

### 배경

Minikube는 Kubernetes Cluster를 생성하는 도구이며, 실제 Kubernetes 리소스를 생성하고 관리하기 위해서는 kubectl이 필요하다.

kubectl은 Kubernetes API Server와 통신하여 Pod, Deployment, Service 등의 리소스를 관리하는 공식 CLI 도구이다.

---

### 목적

Kubernetes Cluster를 제어하기 위한 kubectl CLI를 설치한다.

---

### 사용 명령어

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

chmod +x kubectl

sudo mv kubectl /usr/local/bin/

kubectl version --client
```

---

### 실행 결과

kubectl 설치가 완료되었으며 Client Version을 통해 정상적으로 설치된 것을 확인하였다.

---

### 캡처

![alt text](<7. kubectl 설치 및 Version 확인.jpg>)


## 7-5. AWS EBS 20GB 온라인 확장

### 배경

Minikube Cluster를 생성하는 과정에서 `No space left on device` 오류가 발생하였다.

확인 결과 EC2에 연결된 Amazon EBS의 용량이 8GB로 설정되어 있었으며 Kubernetes 환경을 운영하기에는 저장 공간이 부족하였다.

향후 GitHub Actions, ArgoCD, Prometheus, Grafana 등을 추가로 구축할 예정이므로 EBS 용량을 확장하기로 결정하였다.

---

### 목적

Amazon EBS 용량을 8GB에서 20GB로 확장하여 Kubernetes 운영에 필요한 저장 공간을 확보한다.

---

### 수행 내용

- Amazon EBS Volume 8GB → 20GB 확장
- Linux FileSystem 확장
- Root Partition 용량 확인

---

### 실행 결과

AWS 콘솔에서 EBS Volume을 20GB로 확장한 후 Linux FileSystem을 확장하여 Root Partition이 정상적으로 20GB에 가깝게 증가한 것을 확인하였다.

---

### 캡처

![alt text](<8. AWS EBS 20GB 확장.jpg>)

![alt text](<9. Linux 파일시스템 확장 완료.jpg>)


## 7-6. Kubernetes Cluster 구축

### 배경

Minikube와 kubectl 설치가 완료되었으므로 Kubernetes Cluster를 생성하였다.

Cluster는 Kubernetes의 가장 기본적인 실행 환경이며, 이후 생성되는 모든 Pod, Deployment, Service는 Cluster 내부에서 관리된다.

---

### 목적

Minikube 기반 Kubernetes Cluster를 생성하고 정상적으로 동작하는지 확인한다.

---

### 사용 명령어

```bash
minikube start --driver=docker

kubectl get nodes
```

---

### 실행 결과

Minikube를 이용하여 Kubernetes Cluster를 생성하였다.

Cluster 생성이 완료된 후 `kubectl get nodes` 명령을 통해 Control Plane Node가 `Ready` 상태인 것을 확인하였다.

이를 통해 Kubernetes API Server와 Control Plane이 정상적으로 동작하는 것을 검증하였다.

---

### 캡처

![alt text](<10. Kubernetes Cluster 생성 성공.jpg>)

![alt text](<11. Kubernetes Node Ready 확인.jpg>)


## 7-7. Deployment 생성

### 배경

Kubernetes에서는 Container를 직접 실행하지 않고 Deployment를 통해 Pod를 생성하고 관리한다.

Deployment는 원하는 Pod 개수를 유지하며 장애가 발생했을 때 자동으로 새로운 Pod를 생성하는 역할을 수행한다.

---

### 목적

Deployment를 생성하여 Flask 애플리케이션을 Kubernetes Pod 환경에서 실행한다.

---

### 사용 명령어

```bash
kubectl apply -f deployment.yaml

kubectl get deployments

kubectl get pods
```

---

### 실행 결과

Deployment를 생성하여 ReplicaSet과 Pod가 자동으로 생성되는 것을 확인하였다.

초기에는 Docker Image를 Minikube가 인식하지 못하여 `ErrImageNeverPull` 오류가 발생하였지만 Docker Image를 Minikube에 등록한 후 Pod가 정상적으로 Running 상태가 되었다.

---

### 캡처

![alt text](<13. Kubernetes ImagePull 오류 발생.jpg>)

![alt text](<14. Kubernetes Pod Running 확인.jpg>)

## 7-8. Service(NodePort) 생성

### 배경

Pod는 생성 및 삭제될 때마다 IP 주소가 변경될 수 있으므로 외부에서 직접 접근하는 것은 적절하지 않다.

이를 해결하기 위해 Service를 생성하여 Pod 앞단에 고정된 접근 지점을 구성하였다.

이번 프로젝트에서는 NodePort 방식을 이용하여 Flask API를 Service를 통해 접근하도록 구성하였다.

---

### 목적

NodePort Service를 생성하여 Pod와 외부 요청을 연결한다.

---

### 사용 명령어

```bash
kubectl apply -f service.yaml

kubectl get svc

curl http://192.168.49.2:30080
```

---

### 실행 결과

NodePort Service가 정상적으로 생성되었으며 EC2 내부에서 curl 명령을 이용하여 Service를 통해 Flask API가 정상적으로 응답하는 것을 확인하였다.

외부 브라우저를 통한 접근은 EC2와 Minikube(Docker Driver) 환경 특성상 추가적인 포트 포워딩 또는 Ingress 구성이 필요하므로 이후 단계에서 진행할 예정이다.

---

### 캡처

![alt text](<15. Kubernetes Service 및 Flask 응답 확인.jpg>)

## 7-9. Kubernetes Self-Healing 검증

### 배경

Kubernetes의 가장 큰 특징 중 하나는 Self-Healing 기능이다.

Pod가 비정상적으로 종료되거나 삭제되더라도 Deployment가 원하는 Replica 수를 유지하기 위해 새로운 Pod를 자동으로 생성한다.

---

### 목적

Pod를 직접 삭제하여 Kubernetes의 Self-Healing 기능이 정상적으로 동작하는지 확인한다.

---

### 사용 명령어

```bash
kubectl delete pod --all

kubectl get pods
```

---

### 실행 결과

기존 Pod를 모두 삭제한 후 Deployment가 새로운 Pod를 자동으로 생성하는 것을 확인하였다.

새롭게 생성된 Pod가 Running 상태가 되면서 Kubernetes의 Self-Healing 기능이 정상적으로 동작하는 것을 검증하였다.

---

### 결과 분석

Deployment는 ReplicaSet을 통해 원하는 Pod 개수를 지속적으로 유지한다.

따라서 사용자가 Pod를 직접 삭제하더라도 ReplicaSet이 이를 감지하여 새로운 Pod를 자동으로 생성한다.

이를 통해 Kubernetes가 장애 발생 시 서비스를 지속적으로 유지할 수 있음을 확인하였다.


# 8. 핵심 기술 이해

---

## 8-1. Kubernetes란?

### Kubernetes의 정의

Kubernetes(K8s)는 컨테이너 기반 애플리케이션을 자동으로 배포(Deployment), 확장(Scaling), 복구(Self-Healing)하기 위한 컨테이너 오케스트레이션(Container Orchestration) 플랫폼이다.

Google에서 개발하였으며 현재는 CNCF(Cloud Native Computing Foundation)에서 관리하는 오픈소스 프로젝트이다.

---

### Kubernetes를 사용하는 이유

Docker만으로도 컨테이너를 실행할 수 있지만 운영 환경에서는 수십 개 이상의 컨테이너를 관리해야 한다.

Kubernetes는 이러한 컨테이너를 자동으로 관리하고 장애 발생 시 자동 복구, 부하 분산, 무중단 배포 등을 지원한다.

---

### 이번 프로젝트에서 Kubernetes 역할

DAY2에서는 Minikube 기반 Kubernetes Cluster를 구축하고 Flask API를 Pod 형태로 실행하였다.

Deployment와 Service를 이용하여 애플리케이션을 관리하고 Self-Healing 기능을 직접 검증하였다.

---

### Kubernetes 구조

```text
Developer

↓

kubectl

↓

Kubernetes API Server

↓

Deployment

↓

ReplicaSet

↓

Pod

↓

Container
```

---

### 학습 포인트

- Kubernetes는 Container를 직접 관리하지 않는다.
- Deployment를 통해 Pod를 생성하고 관리한다.
- 장애가 발생하면 자동으로 Pod를 복구한다.
- Service를 통해 안정적인 네트워크를 제공한다.


## 8-2. Minikube란?

### Minikube의 정의

Minikube는 단일 Node 기반 Kubernetes Cluster를 로컬 환경에서 실행할 수 있도록 제공하는 도구이다.

학습 및 개발 환경에서 Kubernetes를 직접 구축하고 테스트하기 위해 가장 많이 사용된다.

---

### Minikube를 사용하는 이유

Amazon EKS와 같은 관리형 Kubernetes 서비스를 사용하기 전에 Kubernetes의 내부 동작 원리를 직접 이해하기 위해 사용하였다.

---

### 이번 프로젝트에서 Minikube 역할

DAY2에서는 Docker Driver 기반으로 Minikube를 설치하고 Kubernetes Cluster를 구축하였다.

향후 GitHub Actions, ArgoCD, Prometheus, Grafana 등을 동일한 Cluster 환경에서 운영할 예정이다.

---

### 학습 포인트

- Minikube는 Kubernetes Cluster를 생성한다.
- kubectl은 Minikube가 생성한 Cluster를 제어한다.
- Minikube는 학습 환경에 적합하다.


## 8-3. Node란?

### Node의 정의

Node는 Kubernetes에서 Pod가 실제로 실행되는 서버이다.

물리 서버 또는 가상 서버가 Node 역할을 수행하며 하나의 Cluster에는 여러 개의 Node가 존재할 수 있다.

---

### 이번 프로젝트에서 Node

이번 프로젝트는 Minikube 기반 단일 Node Cluster를 구축하였다.

`kubectl get nodes` 명령을 통해 Node가 Ready 상태인 것을 확인하였다.

---

### 학습 포인트

- Node는 Pod를 실행하는 서버이다.
- Cluster는 하나 이상의 Node로 구성된다.
- Minikube는 단일 Node Cluster이다.


## 8-4. Pod란?

### Pod의 정의

Pod는 Kubernetes에서 애플리케이션을 실행하는 가장 작은 단위이다.

하나 이상의 Container를 포함할 수 있으며 동일한 네트워크와 Storage를 공유한다.

---

### Pod를 사용하는 이유

Kubernetes는 Container를 직접 관리하지 않고 Pod를 관리한다.

Container는 항상 Pod 내부에서 실행된다.

---

### 이번 프로젝트에서 Pod

Deployment를 생성하면서 Flask Container가 포함된 Pod가 자동으로 생성되었다.

Pod가 삭제되면 Deployment에 의해 새로운 Pod가 자동 생성되는 것을 확인하였다.

---

### 학습 포인트

- Pod는 Kubernetes의 최소 실행 단위이다.
- Pod 내부에서 Container가 실행된다.
- Pod는 직접 생성하기보다 Deployment를 이용하는 것이 일반적이다.


## 8-5. Deployment란?

### Deployment의 정의

Deployment는 Kubernetes에서 Pod를 생성하고 관리하는 Controller이다.

원하는 Pod 개수를 유지하고 새로운 버전 배포 및 장애 복구를 자동으로 수행한다.

---

### 이번 프로젝트에서 Deployment

Flask API를 실행하기 위해 Deployment를 생성하였다.

Deployment는 ReplicaSet을 생성하고 ReplicaSet은 Pod를 생성하였다.

---

### Deployment 구조

```text
Deployment

↓

ReplicaSet

↓

Pod

↓

Container
```

---

### 학습 포인트

- Deployment는 Pod를 직접 생성하지 않는다.
- ReplicaSet을 생성하여 Pod를 관리한다.
- 운영 환경에서는 Pod보다 Deployment를 사용하는 것이 일반적이다.


## 8-6. ReplicaSet이란?

### ReplicaSet의 정의

ReplicaSet은 Deployment가 원하는 Pod 개수를 유지하도록 관리하는 Controller이다.

Pod가 삭제되거나 장애가 발생하면 새로운 Pod를 자동으로 생성한다.

---

### 이번 프로젝트에서 ReplicaSet

Deployment 생성 시 ReplicaSet이 자동으로 생성되었으며 Pod를 삭제한 후 새로운 Pod를 자동 생성하는 것을 확인하였다.

---

### 학습 포인트

- ReplicaSet은 Pod 개수를 유지한다.
- Deployment가 ReplicaSet을 생성한다.
- Self-Healing 기능은 ReplicaSet을 통해 동작한다.


## 8-7. Service란?

### Service의 정의

Service는 Kubernetes에서 Pod를 외부 또는 다른 Pod가 안정적으로 접근할 수 있도록 제공하는 네트워크 리소스이다.

Pod는 생성되거나 삭제될 때마다 IP 주소가 변경될 수 있기 때문에 Pod에 직접 접근하는 것은 적절하지 않다.

Service는 이러한 Pod 앞단에서 고정된 접근 지점을 제공하여 항상 동일한 방식으로 애플리케이션에 접근할 수 있도록 한다.

---

### Service를 사용하는 이유

Pod는 일시적인(Temporary) 리소스이므로 장애 복구나 재배포 과정에서 IP 주소가 변경될 수 있다.

Service는 Label Selector를 이용하여 현재 실행 중인 Pod와 자동으로 연결되므로 Pod가 변경되어도 서비스는 계속 유지된다.

---

### 이번 프로젝트에서 Service 역할

Deployment를 통해 생성된 Flask Pod 앞단에 NodePort Service를 생성하였다.

Service를 통해 Pod와 독립적인 접근 지점을 구성하였으며 EC2 내부에서 curl 명령을 이용하여 Flask API가 정상적으로 응답하는 것을 확인하였다.

---

### Service 구조

```text
Browser

↓

Service

↓

Pod

↓

Container
```

---

### 학습 포인트

- Service는 Pod의 고정된 접근 지점을 제공한다.
- Service는 Pod IP 변경과 관계없이 동일한 방식으로 접근할 수 있다.
- Service는 Label Selector를 이용하여 Pod와 연결된다.


## 8-8. NodePort란?

### NodePort의 정의

NodePort는 Kubernetes Service의 한 종류로 Cluster 외부에서 Node의 특정 포트를 통해 Pod에 접근할 수 있도록 제공하는 방식이다.

NodePort는 기본적으로 30000~32767 범위의 포트를 사용한다.

---

### NodePort를 사용하는 이유

개발 및 테스트 환경에서는 LoadBalancer를 사용할 수 없는 경우가 많다.

Minikube 환경에서는 NodePort를 이용하여 Service를 외부에 노출할 수 있도록 구성하였다.

---

### 이번 프로젝트에서 NodePort

Flask API를 Service를 통해 접근할 수 있도록 NodePort Service를 생성하였다.

EC2 내부에서는 curl 명령을 이용하여 Service를 통한 정상 응답을 확인하였으며, 외부 브라우저 접근은 이후 Ingress 구성 단계에서 진행할 예정이다.
---

### NodePort 구조

```text
Browser

↓

NodePort

↓

Service

↓

Pod

↓

Container
```

---

### 학습 포인트

- NodePort는 외부에서 Kubernetes Service로 접근하기 위한 방식이다.
- Service는 NodePort를 통해 Pod와 연결된다.
- 운영 환경에서는 NodePort보다 LoadBalancer 또는 Ingress를 주로 사용한다.


## 8-9. kubectl이란?

### kubectl의 정의

kubectl은 Kubernetes Cluster를 관리하기 위한 공식 Command Line Interface(CLI)이다.

kubectl은 Kubernetes API Server와 통신하여 Deployment, Pod, Service 등의 리소스를 생성, 조회, 수정 및 삭제할 수 있다.

---

### 이번 프로젝트에서 kubectl 역할

DAY2에서는 kubectl을 이용하여 Kubernetes Cluster 상태를 확인하고 Deployment와 Service를 생성하였다.

또한 Pod 상태를 확인하고 Self-Healing 기능을 검증하는 과정에서도 kubectl을 사용하였다.

---

### 주요 사용 명령어

```bash
kubectl get nodes

kubectl get pods

kubectl get deployments

kubectl get svc

kubectl apply -f deployment.yaml

kubectl apply -f service.yaml
```

---

### 학습 포인트

- kubectl은 Kubernetes Cluster를 관리하는 CLI이다.
- kubectl은 Kubernetes API Server와 통신한다.
- 대부분의 Kubernetes 리소스 관리는 kubectl을 통해 수행한다.


## 8-10. Self-Healing이란?

### Self-Healing의 정의

Self-Healing은 Kubernetes에서 장애가 발생한 Pod를 자동으로 복구하는 기능이다.

Deployment는 ReplicaSet을 통해 원하는 Pod 개수를 유지하며 Pod가 삭제되거나 비정상 종료되면 새로운 Pod를 자동으로 생성한다.

---

### 이번 프로젝트에서 Self-Healing 검증

Deployment를 생성한 후 실행 중인 Pod를 직접 삭제하였다.

Pod 삭제 이후 ReplicaSet이 새로운 Pod를 자동 생성하였으며 Running 상태가 되는 것을 확인하였다.

이를 통해 Kubernetes의 Self-Healing 기능이 정상적으로 동작하는 것을 검증하였다.

---

### Self-Healing 구조

```text
Pod 삭제

↓

ReplicaSet 감지

↓

새로운 Pod 생성

↓

Running
```

---

### 학습 포인트

- Self-Healing은 ReplicaSet이 수행한다.
- Deployment는 원하는 Pod 개수를 항상 유지한다.
- 운영 환경에서는 장애가 발생해도 서비스가 지속될 수 있도록 지원한다.


# 9. 문제 해결 (Problem Solving)

DAY2를 진행하면서 Kubernetes Cluster 구축 과정에서 여러 문제가 발생하였다.

각 문제에 대해 원인을 분석하고 해결 과정을 정리하였다.

실제 운영 환경에서도 충분히 발생할 수 있는 문제였으며, 문제를 해결하는 과정에서 Kubernetes뿐 아니라 AWS 인프라와 Linux 파일시스템에 대한 이해를 높일 수 있었다.

---

## 9-1. Minikube Cluster 생성 실패

### 문제

Minikube Cluster 생성 과정에서 아래와 같은 오류가 발생하였다.

```text
No space left on device
```

---

### 원인 분석

초기에는 단순히 Linux 파일시스템 용량 부족으로 판단하였다.

그러나 `df -h`, `df -i`, `docker system df` 등을 확인한 결과 Docker Image와 Inode 사용량에는 문제가 없었다.

추가 분석 결과 EC2에 연결된 Amazon EBS Volume이 8GB로 구성되어 있었으며 Kubernetes Cluster와 향후 구축 예정인 GitHub Actions, ArgoCD, Prometheus 등을 운영하기에는 저장 공간이 부족한 상태였다.

---

### 해결 과정

AWS Console에서 Amazon EBS Volume을 8GB에서 20GB로 온라인 확장하였다.

이후 Linux에서 Partition과 FileSystem을 확장하여 Root Volume을 정상적으로 증가시켰다.

확장 완료 후 Minikube Cluster를 다시 생성하여 정상적으로 구축되는 것을 확인하였다.

---

### 결과

Kubernetes Cluster가 정상적으로 생성되었으며 향후 DevSecOps 환경을 구축하기 위한 충분한 저장 공간을 확보하였다.


## 9-2. Kubernetes ImagePull 오류

### 문제

Deployment 생성 후 Pod 상태가 아래와 같은 오류를 표시하였다.

```text
ErrImageNeverPull
```

---

### 원인 분석

Deployment에서는 `imagePullPolicy: Never`를 사용하도록 설정하였다.

그러나 Docker에서 생성한 Flask Image가 Minikube 내부 Image 저장소에 존재하지 않았기 때문에 Pod를 생성하지 못하였다.

---

### 해결 과정

Docker에서 생성한 Flask Image를 Minikube Image 저장소에 등록하였다.

```bash
minikube image load flask-api:v1

kubectl delete pod --all
```

이후 기존 Pod를 삭제하여 Deployment가 새로운 Pod를 생성하도록 하였으며 정상적으로 Running 상태가 되는 것을 확인하였다.

---

### 결과

Flask Docker Image를 이용하여 Kubernetes Pod가 정상적으로 생성되었으며 Deployment가 정상적으로 동작하는 것을 확인하였다.


## 9-3. Git Branch 운영 문제

### 문제

DAY2 작업을 진행하면서 Feature Branch를 생성하였으나 EC2의 Main Branch가 최신 상태가 아니었기 때문에 Windows와 EC2 간 문서 버전이 서로 달라지는 문제가 발생하였다.

---

### 원인 분석

Feature Branch를 생성하기 전에 EC2에서 Main Branch를 최신 상태로 동기화하지 않았다.

그 결과 오래된 Main Branch를 기준으로 Feature Branch가 생성되었고 Windows에서 Branch를 변경하는 과정에서 최신 문서가 보이지 않는 문제가 발생하였다.

---

### 해결 과정

Main Branch의 최신 문서를 Feature Branch로 다시 가져와 동기화하였다.

또한 프로젝트 운영 절차를 개선하여 Feature Branch 생성 전 Main Branch를 최신 상태로 유지하도록 Git 운영 전략을 수정하였다.

---

### 결과

Windows와 EC2가 동일한 Git 상태를 유지하게 되었으며 이후 문서 작성과 코드 관리가 정상적으로 수행되었다.


# 10. DAY2 회고

DAY2에서는 Docker 환경에서 실행 중이던 Flask 애플리케이션을 Kubernetes 환경으로 이전하는 작업을 수행하였다.

Minikube 기반 Kubernetes Cluster를 직접 구축하고 Deployment, ReplicaSet, Pod, Service를 구성하면서 Kubernetes의 기본 동작 원리를 이해할 수 있었다.

특히 Pod를 직접 삭제한 후 Deployment와 ReplicaSet이 새로운 Pod를 자동으로 생성하는 과정을 확인하면서 Kubernetes의 Self-Healing 기능을 직접 검증할 수 있었다.

또한 구축 과정에서 Amazon EBS 저장 공간 부족 문제와 Kubernetes ImagePull 오류를 해결하면서 단순한 설치를 넘어 실제 운영 환경에서 발생할 수 있는 문제를 분석하고 해결하는 경험을 쌓을 수 있었다.

GitHub SSH 인증 전환과 Feature Branch 기반 Git 운영 전략도 함께 적용하여 프로젝트 운영 환경을 실제 개발 환경과 유사하게 개선하였다.

---

## 잘된 점

- Kubernetes Cluster를 정상적으로 구축하였다.
- Deployment, ReplicaSet, Pod, Service의 관계를 직접 확인하였다.
- Kubernetes Self-Healing 기능을 검증하였다.
- AWS EBS 온라인 확장을 경험하였다.
- GitHub Feature Branch 기반 개발 환경을 구축하였다.

---

## 아쉬운 점

- Kubernetes Image 관리 방식에 대한 이해가 부족하여 ImagePull 오류가 발생하였다.
- EC2와 Windows 간 Git Branch 동기화 과정에서 문서 버전이 일시적으로 맞지 않는 문제가 발생하였다.
- Minikube(NodePort) 환경에서는 외부 브라우저 접근 방식이 일반 Kubernetes 운영 환경과 다르다는 점을 뒤늦게 확인하였다.

---

## 개선할 점

- Docker Image 관리 방식을 보다 체계적으로 이해한다.
- Git Branch 생성 전 Main Branch를 항상 최신 상태로 유지한다.
- DAY3에서는 GitHub Actions를 이용하여 Docker Image Build와 Docker Hub Push를 자동화한다.
- 이후 ArgoCD를 이용하여 GitOps 기반 자동 배포 환경을 구축한다.

---

## DAY2 핵심 성과

- GitHub SSH 인증 전환 완료
- Feature Branch 전략 적용 완료
- Kubernetes Cluster 구축 완료
- Deployment / ReplicaSet / Pod 구성 완료
- Service(NodePort) 구성 완료
- Kubernetes Self-Healing 검증 완료
- AWS EBS 온라인 확장 완료
- Kubernetes ImagePull 오류 해결


# 11. DAY3 계획

DAY3에서는 GitHub Actions를 이용하여 CI(Continuous Integration) 환경을 구축할 예정이다.

코드 변경 시 Docker Image를 자동으로 Build하고 Docker Hub로 Push하는 자동화 파이프라인을 구성하여 수동으로 수행하던 Docker Build 과정을 자동화하는 것을 목표로 한다.

또한 이후 ArgoCD를 이용한 GitOps 기반 자동 배포 환경으로 확장하기 위한 기반을 구성할 예정이다.

---

## DAY3 목표

- GitHub Actions 기반 CI Pipeline 구축
- Docker Image 자동 Build
- Docker Hub 자동 Push
- Kubernetes 자동 배포 기반 구성

---

## DAY3 완료 목표

- GitHub Actions Workflow 구축 완료
- Docker Image 자동 Build 성공
- Docker Hub 자동 Push 성공
- GitHub Push 시 CI Pipeline 자동 실행 확인