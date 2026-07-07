# DAY4 - ArgoCD 기반 GitOps Continuous Delivery 구축

---

# 1. DAY4 목표

DAY4의 목표는 ArgoCD를 이용하여 GitOps(Git Operations) 기반 Continuous Delivery(CD) 환경을 구축하는 것이다.

DAY3에서는 GitHub Actions를 이용하여 Docker Image를 자동으로 Build하고 Docker Hub에 Push하는 CI(Continuous Integration) 환경을 구축하였다.

DAY4에서는 GitHub Repository를 Single Source of Truth로 사용하는 GitOps 운영 방식을 적용하여 Git 변경 사항을 Kubernetes Cluster에 자동으로 반영하는 Continuous Delivery 환경을 구축하는 것을 목표로 한다.

또한 Manual Sync와 Auto Sync를 모두 검증하고, Git Manifest 변경이 Kubernetes Deployment와 Pod에 자동으로 반영되는 과정을 직접 확인하여 GitOps 운영 원리를 이해하는 것을 목표로 한다.

---

# 2. DAY4 완료 목표

- ArgoCD Namespace 생성
- ArgoCD 설치
- ArgoCD Dashboard 구성
- Git Repository 연동
- Kubernetes Application 생성
- Manual Sync 검증
- Auto Sync 활성화
- Git 변경 자동 감지
- Kubernetes Deployment 자동 변경
- Replica 변경 자동 반영 검증
- GitOps 기반 Continuous Delivery 구축

---

# 3. 구축 환경

| 항목 | 내용 |
|------|------|
| Cloud | AWS EC2 (t3.medium) |
| OS | Ubuntu 24.04 LTS |
| Container Runtime | Docker CE |
| Kubernetes | Minikube v1.38.1 |
| GitOps | ArgoCD v3.4.4 |
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

GitHub Actions (CI)

        │

Docker Hub

        │

ArgoCD (GitOps CD)

        │

Kubernetes (Minikube)

        │

Deployment

        │

ReplicaSet

        │

Pod

        │

Flask API
```

---

# 5. DAY4에서 구현한 기능

- Git Main Branch 최신화
- Feature Branch 생성
- ArgoCD Namespace 생성
- ArgoCD 설치
- ArgoCD Dashboard 구성
- Git Repository 연동
- Kubernetes Application 생성
- Manual Sync 검증
- Auto Sync 활성화
- Git 변경 자동 감지
- Kubernetes Deployment 자동 변경
- Replica 변경 자동 반영 검증
- GitOps 기반 Continuous Delivery 구축

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
│   ├── deployment.yaml
│   └── service.yaml
│
├── argocd
│
├── monitoring
│
├── docs
│
└── README.md
```

---

# 7. 구축 과정

DAY4에서는 GitHub Actions를 통해 구축한 CI 환경을 기반으로 ArgoCD를 설치하고 GitOps 기반 Continuous Delivery(CD) 환경을 구축하였다.

Git Repository를 Single Source of Truth로 사용하는 GitOps 운영 방식을 적용하여 Git 변경 사항이 Kubernetes Cluster에 자동으로 반영되는 환경을 구성하였다.

또한 Manual Sync와 Auto Sync를 모두 검증하고, Git Manifest 변경이 Kubernetes Deployment와 Pod에 자동으로 반영되는 과정을 직접 확인하였다.

구축 과정은 실제 수행 순서에 따라 작성하였으며 각 단계마다 수행 목적, 사용 명령어, 결과 및 실무적인 고려사항을 함께 정리하였다.

---

## 7-1. ArgoCD Namespace 생성

### 배경

ArgoCD는 Kubernetes Cluster 내부에서 여러 개의 Pod와 Service를 이용하여 동작하는 GitOps 플랫폼이다.

기존 Flask 애플리케이션은 default Namespace에서 실행되고 있었으며, 운영 플랫폼인 ArgoCD와 애플리케이션을 분리하여 관리하기 위해 별도의 Namespace를 생성하였다.

실무에서도 ArgoCD, Prometheus, Grafana와 같은 운영 플랫폼은 전용 Namespace에서 관리하는 것이 일반적이다.

---

### 목적

ArgoCD를 위한 전용 Namespace를 생성하여 운영 리소스와 애플리케이션 리소스를 분리한다.

---

### Why?

Namespace는 Kubernetes Cluster 내부에서 리소스를 논리적으로 분리하는 기능을 제공한다.

운영 플랫폼과 애플리케이션을 동일한 Namespace에서 관리하면 리소스 식별이 어려워지고 운영 및 유지보수가 복잡해질 수 있다.

이번 프로젝트에서는 ArgoCD를 독립적인 Namespace에서 운영함으로써 실제 운영 환경과 유사한 구조를 구성하였다.

---

### 사용 명령어

```bash
kubectl create namespace argocd

kubectl get namespace
```

---

### 명령어 설명

| 명령어 | 설명 |
|---------|------|
| `kubectl create namespace argocd` | argocd Namespace 생성 |
| `kubectl get namespace` | 생성된 Namespace 확인 |

---

### 실행 결과

argocd Namespace가 정상적으로 생성되었으며 Status가 Active 상태인 것을 확인하였다.

이를 통해 ArgoCD를 설치하기 위한 독립된 Kubernetes Namespace 구성이 완료되었다.

---

### 결과 분석

Kubernetes는 Namespace 단위로 리소스를 구분하여 관리한다.

ArgoCD 전용 Namespace를 생성함으로써 이후 설치되는 Deployment, Service, Secret, ConfigMap 등의 리소스를 운영 플랫폼 전용 영역에서 관리할 수 있게 되었다.

---

### 학습 포인트

- Namespace는 Kubernetes 리소스를 논리적으로 분리한다.
- 운영 플랫폼과 애플리케이션은 별도 Namespace에서 운영하는 것이 일반적이다.
- Namespace를 이용하면 리소스 관리와 유지보수가 용이해진다.

---

### 캡처

![ArgoCD Namespace 생성](docs/screenshots/day4/01-argocd-namespace-created.jpg)

---

### 실무 TIP

실무에서는 default Namespace를 최소한으로 사용하고, 운영 목적에 따라 별도의 Namespace를 생성하여 관리하는 것이 일반적이다.

예를 들어 ArgoCD, Prometheus, Grafana, Istio 등은 각각 독립된 Namespace에서 운영하는 경우가 많다.

---

### 운영 시 고려사항

Namespace는 보안 정책(RBAC), ResourceQuota, NetworkPolicy 등을 적용하는 기본 단위이므로 프로젝트 초기 단계에서 역할에 맞게 구분하는 것이 중요하다.


## 7-2. ArgoCD 설치

### 배경

ArgoCD는 Kubernetes 환경에서 GitOps 기반 Continuous Delivery(CD)를 제공하는 대표적인 오픈소스 플랫폼이다.

Git Repository를 Single Source of Truth로 사용하며 Kubernetes Cluster의 현재 상태(Actual State)와 Git Repository의 원하는 상태(Desired State)를 지속적으로 비교하여 자동으로 동기화하는 기능을 제공한다.

이번 프로젝트에서는 GitHub Actions를 이용한 CI 환경을 기반으로 GitOps 기반 CD 환경을 구축하기 위해 ArgoCD를 설치하였다.

---

### 목적

ArgoCD를 Kubernetes Cluster에 설치하여 Git Repository 기반 Continuous Delivery 환경을 구축한다.

---

### Why?

DAY3에서는 GitHub Actions를 이용하여 Docker Image를 자동으로 Build하고 Docker Hub에 Push하는 CI 환경을 구축하였다.

그러나 Docker Image가 생성되더라도 Kubernetes Deployment는 여전히 관리자가 직접 수정하거나 `kubectl apply`를 수행해야 한다.

GitOps 환경에서는 Git Repository만 변경하면 ArgoCD가 이를 감지하여 Kubernetes Cluster를 자동으로 원하는 상태로 유지한다.

이를 통해 사람이 직접 Kubernetes를 수정하지 않고 Git을 중심으로 운영하는 Declarative Infrastructure 환경을 구성할 수 있다.

---

### 사용 명령어

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

---

### 명령어 설명

| 명령어 | 설명 |
|---------|------|
| `kubectl apply` | Kubernetes Resource 생성 및 적용 |
| `-n argocd` | argocd Namespace에 설치 |
| `-f` | Manifest 파일 지정 |
| `install.yaml` | ArgoCD 공식 설치 Manifest |

---

### 실행 결과

ArgoCD 공식 Manifest를 이용하여 Deployment, Service, ConfigMap, Secret 등 ArgoCD 구성 요소가 Kubernetes Cluster에 정상적으로 생성되었다.

이후 ArgoCD 관련 Pod가 생성되기 시작하였으며 GitOps 플랫폼을 운영하기 위한 기반 환경이 구성되었다.

---

### 결과 분석

ArgoCD는 하나의 Pod로 구성되는 애플리케이션이 아니라 여러 개의 Kubernetes Resource를 조합하여 동작하는 플랫폼이다.

공식 Manifest를 적용하면 필요한 Deployment, Service, Secret, ConfigMap, RBAC 등이 한 번에 생성되므로 복잡한 설치 과정을 단순화할 수 있다.

이번 프로젝트에서는 ArgoCD 공식 Manifest를 사용하여 안정적이고 표준화된 설치 방식을 적용하였다.

---

### 학습 포인트

- ArgoCD는 GitOps 기반 Continuous Delivery 플랫폼이다.
- 공식 Manifest를 이용하면 모든 구성 요소를 한 번에 설치할 수 있다.
- ArgoCD는 Deployment, Service, Secret, ConfigMap 등 여러 Kubernetes Resource로 구성된다.
- Git Repository를 Single Source of Truth로 사용하는 운영 방식을 제공한다.

---

### 캡처

![ArgoCD 설치](docs/screenshots/day4/02-argocd-installed.jpg)

---

### 실무 TIP

실무에서는 Helm Chart 또는 ArgoCD Operator를 이용하여 설치하는 경우도 많지만, 학습 및 검증 환경에서는 공식 Manifest를 사용하는 것이 가장 간단하고 표준적인 방법이다.

또한 공식 Manifest는 ArgoCD 버전에 맞춰 지속적으로 관리되므로 안정적인 설치가 가능하다.

---

### 운영 시 고려사항

ArgoCD 설치 후에는 Pod가 모두 Running 상태가 될 때까지 충분히 대기해야 한다.

설치 직후에는 `ContainerCreating`, `Pending`, `Init` 상태가 나타날 수 있으며, 모든 핵심 Pod가 Running 상태가 되어야 정상적으로 Dashboard와 GitOps 기능을 사용할 수 있다.


## 7-3. ArgoCD Pod 확인

### 배경

ArgoCD 설치가 완료되었다고 해서 즉시 사용할 수 있는 것은 아니다.

Kubernetes는 Deployment를 생성한 이후 필요한 Pod를 순차적으로 생성하며, 각 Pod가 정상적으로 실행(Running) 상태가 되어야 GitOps 플랫폼이 정상적으로 동작한다.

따라서 설치 완료 이후 ArgoCD의 모든 Pod가 정상적으로 실행되고 있는지 확인하는 과정이 필요하였다.

---

### 목적

ArgoCD를 구성하는 모든 Pod가 정상적으로 생성되고 Running 상태인지 확인한다.

---

### Why?

ArgoCD는 여러 개의 Pod가 서로 협력하여 하나의 GitOps 플랫폼을 구성한다.

만약 일부 Pod가 실행되지 않거나 CrashLoopBackOff 상태가 발생하면 Git Repository 연동, Application 생성, Sync 등의 기능이 정상적으로 동작하지 않는다.

따라서 Dashboard에 접속하기 전에 모든 핵심 Pod가 정상적으로 실행되는지 확인하는 것이 중요하다.

---

### 사용 명령어

```bash
kubectl get pods -n argocd
```

---

### 명령어 설명

| 명령어 | 설명 |
|---------|------|
| `kubectl get pods` | 현재 실행 중인 Pod 조회 |
| `-n argocd` | argocd Namespace 내부 Pod 조회 |

---

### 실행 결과

ArgoCD를 구성하는 모든 Pod가 정상적으로 생성되었으며 Running 상태인 것을 확인하였다.

대표적으로 다음과 같은 Pod가 생성되었다.

- argocd-server
- argocd-repo-server
- argocd-application-controller
- argocd-applicationset-controller
- argocd-dex-server
- argocd-notifications-controller
- argocd-redis

---

### 결과 분석

ArgoCD는 하나의 Pod가 아닌 여러 개의 구성 요소로 이루어진 플랫폼이다.

각 Pod는 서로 다른 역할을 수행하며 함께 GitOps 기능을 제공한다.

예를 들어 Repository Server는 Git Repository와 통신하고, Application Controller는 Kubernetes 상태를 지속적으로 비교하며, Server는 Web UI를 제공한다.

모든 Pod가 Running 상태가 되어야 ArgoCD를 정상적으로 사용할 수 있다.

---

### 학습 포인트

- ArgoCD는 여러 개의 Pod로 구성된다.
- 각 Pod는 서로 다른 역할을 수행한다.
- Running 상태가 되어야 GitOps 기능을 사용할 수 있다.
- Dashboard 접속 전에 Pod 상태를 먼저 확인하는 것이 좋다.

---

### 캡처

![ArgoCD Installed](docs/screenshots/day4/02-argocd-installed.jpg)

---

### 실무 TIP

실무에서는 설치 직후 `kubectl get pods -n argocd -w` 명령을 사용하여 Pod 상태를 실시간으로 확인하는 경우가 많다.

CrashLoopBackOff, ImagePullBackOff, Pending 등의 상태가 발생하면 Dashboard 접속 전에 원인을 먼저 분석해야 한다.

---

### 운영 시 고려사항

ArgoCD의 일부 Pod만 실행되더라도 Dashboard가 정상적으로 동작하지 않거나 Git Repository와의 통신이 실패할 수 있다.

특히 `argocd-server`, `argocd-repo-server`, `argocd-application-controller`는 GitOps의 핵심 구성 요소이므로 항상 정상 상태를 유지해야 한다.




## 7-4. ArgoCD Server NodePort 구성

### 배경

ArgoCD 설치가 완료되었지만 기본적으로 `argocd-server` Service는 `ClusterIP` 타입으로 생성된다.

ClusterIP는 Kubernetes Cluster 내부에서만 접근 가능한 Service이므로 외부 브라우저에서는 ArgoCD Dashboard에 접근할 수 없다.

이번 프로젝트에서는 ArgoCD Web UI를 이용하여 Git Repository를 연동하고 GitOps 기능을 검증해야 하므로 외부에서 접근 가능한 Service 형태로 변경하는 과정이 필요하였다.

---

### 목적

ArgoCD Dashboard를 외부 브라우저에서 접근할 수 있도록 `argocd-server` Service를 NodePort 방식으로 변경한다.

---

### Why?

Kubernetes Service는 여러 가지 타입을 제공한다.

대표적으로 다음과 같은 방식이 존재한다.

```text
ClusterIP

↓

NodePort

↓

LoadBalancer

↓

Ingress
```

기본적으로 ArgoCD는 `ClusterIP` 타입으로 설치된다.

그러나 ClusterIP는 Kubernetes 내부 Pod 간 통신을 위한 Service이므로 외부 PC에서는 접근할 수 없다.

이번 프로젝트는 Minikube 기반 단일 Node Cluster 환경에서 GitOps를 검증하는 것이 목적이므로 외부 접근이 가능한 NodePort 방식을 적용하였다.

---

### 사용 명령어

```bash
kubectl patch svc argocd-server \
-n argocd \
-p '{"spec":{"type":"NodePort"}}'

kubectl get svc -n argocd
```

---

### 명령어 설명

| 명령어 | 설명 |
|---------|------|
| `kubectl patch` | 기존 Kubernetes Resource 수정 |
| `svc argocd-server` | argocd-server Service 수정 |
| `-n argocd` | argocd Namespace 지정 |
| `type: NodePort` | Service Type을 NodePort로 변경 |
| `kubectl get svc` | 변경된 Service 확인 |

---

### 실행 결과

`argocd-server` Service가 기존 ClusterIP에서 NodePort로 변경된 것을 확인하였다.

또한 Kubernetes가 자동으로 NodePort를 할당하여 외부 접근을 위한 포트가 생성되었다.

---

### 결과 분석

NodePort를 적용함으로써 Kubernetes Node의 특정 포트를 통해 ArgoCD Dashboard에 접근할 수 있는 환경이 구성되었다.

다만 Minikube(Docker Driver) 환경에서는 NodePort가 EC2 Public Interface에 직접 바인딩되지 않는 특성이 있으므로 이후 별도의 접근 검증을 수행하였다.

---

### 학습 포인트

- ClusterIP는 Kubernetes 내부 통신 전용 Service이다.
- NodePort는 외부에서 Kubernetes Service에 접근하기 위한 방식이다.
- NodePort는 기본적으로 30000~32767 범위의 포트를 사용한다.
- Service Type은 Patch를 이용하여 변경할 수 있다.

---

### 캡처

![ArgoCD NodePort 구성](docs/screenshots/day4/03-argocd-nodeport-configured.jpg)

---

### 실무 TIP

실무에서는 NodePort를 직접 사용하는 경우는 많지 않다.

일반적으로 Ingress Controller와 LoadBalancer를 이용하여 외부 서비스를 구성한다.

NodePort는 학습 환경이나 테스트 환경에서 가장 많이 사용하는 Service 방식이다.

---

### 운영 시 고려사항

NodePort를 생성하더라도 AWS Security Group이나 방화벽에서 해당 포트를 허용하지 않으면 외부에서는 접근할 수 없다.

따라서 Kubernetes 설정과 클라우드 네트워크 설정을 함께 확인하는 것이 중요하다.


## 7-5. AWS Security Group 구성

### 배경

ArgoCD Server를 NodePort 방식으로 변경하였지만 외부 브라우저에서는 Dashboard에 접근할 수 없었다.

확인 결과 Kubernetes 내부에서는 NodePort가 정상적으로 생성되었지만 AWS Security Group에서 해당 포트를 허용하지 않아 외부 요청이 EC2까지 전달되지 못하는 상태였다.

따라서 Kubernetes 설정뿐만 아니라 AWS 네트워크 설정도 함께 구성하는 과정이 필요하였다.

---

### 목적

AWS Security Group에서 ArgoCD NodePort를 허용하여 외부 브라우저에서 ArgoCD Dashboard에 접근할 수 있는 환경을 구성한다.

---

### Why?

NodePort는 Kubernetes Cluster 내부에서 외부 접근을 위한 포트를 생성하는 기능이다.

그러나 AWS EC2는 Security Group을 이용하여 네트워크 접근을 제어하므로 Kubernetes에서 NodePort를 생성하더라도 AWS에서 해당 포트를 허용하지 않으면 외부에서는 접근할 수 없다.

즉 Kubernetes Networking과 AWS Networking은 서로 독립적으로 동작한다.

이번 프로젝트에서는 Kubernetes NodePort와 AWS Security Group을 함께 구성하여 외부 접근이 가능하도록 하였다.

---

### 수행 내용

AWS EC2 Security Group의 Inbound Rule에 ArgoCD NodePort(TCP 30965)를 추가하였다.

외부 접근은 테스트 목적이므로 현재 사용 중인 Public IP(My IP)만 허용하여 최소 권한 원칙을 적용하였다.

---

### 실행 결과

AWS Security Group에서 NodePort가 정상적으로 허용되었으며 EC2까지 네트워크 요청이 전달될 수 있는 환경이 구성되었다.

---

### 결과 분석

NodePort를 생성하는 것만으로는 외부 접근이 가능하지 않다.

클라우드 환경에서는 Security Group 또는 방화벽 정책이 함께 적용되므로 Kubernetes 설정과 클라우드 네트워크 정책을 모두 확인해야 한다.

이번 프로젝트에서는 AWS Security Group 설정을 추가하여 Kubernetes NodePort를 외부에서 사용할 수 있는 기반을 구성하였다.

---

### 학습 포인트

- Kubernetes NodePort와 AWS Security Group은 서로 다른 계층에서 동작한다.
- NodePort를 생성하더라도 Security Group에서 허용하지 않으면 외부 접근은 불가능하다.
- 클라우드 환경에서는 Kubernetes 설정과 네트워크 정책을 함께 구성해야 한다.
- 최소 권한 원칙에 따라 필요한 포트와 IP만 허용하는 것이 좋다.

---

### 캡처

![AWS Security Group NodePort 허용](docs/screenshots/day4/04-security-group-nodeport-opened.jpg)

---

### 실무 TIP

운영 환경에서는 NodePort 전체 범위를 개방하기보다 필요한 포트만 허용하는 것이 보안상 유리하다.

또한 Source를 `0.0.0.0/0`으로 개방하기보다는 관리자가 사용하는 Public IP 또는 Bastion Host만 허용하는 것이 일반적이다.

---

### 운영 시 고려사항

AWS Security Group은 Stateful Firewall이므로 Inbound Rule만 허용하면 응답 패킷은 자동으로 허용된다.

다만 기업 환경에서는 Security Group뿐만 아니라 Network ACL, Firewall, VPN 정책 등이 함께 적용될 수 있으므로 전체 네트워크 경로를 함께 확인하는 것이 중요하다.


## 7-6. NodePort 내부 검증

### 배경

AWS Security Group에서 ArgoCD NodePort를 허용한 이후에도 EC2 Public IP를 이용한 Dashboard 접속은 정상적으로 이루어지지 않았다.

처음에는 Security Group 설정 문제로 판단하였으나, Kubernetes 내부에서 NodePort가 정상적으로 동작하는지 확인하기 위해 추가적인 검증을 수행하였다.

이를 통해 문제의 원인이 Kubernetes Service가 아닌 Minikube(Docker Driver)의 네트워크 구조에 있다는 것을 확인하였다.

---

### 목적

NodePort가 Kubernetes 내부에서는 정상적으로 동작하는지 확인하고 외부 접근 실패의 원인을 분석한다.

---

### Why?

NodePort는 Kubernetes Node의 특정 포트를 통해 외부 접근을 제공하는 Service이다.

그러나 Minikube는 Docker Driver를 사용할 경우 별도의 Docker Network 내부에서 Kubernetes Node를 실행한다.

따라서 NodePort가 정상적으로 생성되더라도 EC2 Public Interface에 직접 바인딩되지 않을 수 있다.

이번 프로젝트에서는 NodePort 자체의 정상 동작 여부를 먼저 검증한 후 외부 접근 실패 원인을 분석하였다.

---

### 사용 명령어

```bash
minikube ip

curl -k https://$(minikube ip):30965

minikube service argocd-server -n argocd --url
```

---

### 명령어 설명

| 명령어 | 설명 |
|---------|------|
| `minikube ip` | Minikube 내부 Node IP 확인 |
| `curl -k` | NodePort HTTPS 응답 확인(Self-Signed Certificate 허용) |
| `minikube service --url` | Minikube Service 접근 URL 확인 |

---

### 실행 결과

Minikube 내부 IP에서는 ArgoCD Dashboard가 정상적으로 응답하는 것을 확인하였다.

또한 `minikube service` 명령을 통해 Service URL이 정상적으로 생성되는 것을 확인하였다.

이를 통해 NodePort 자체는 정상적으로 동작하고 있으며 외부 접근 문제는 Minikube Docker Driver의 네트워크 구조에서 발생한 것임을 확인하였다.

---

### 결과 분석

Kubernetes Service와 NodePort에는 문제가 없었다.

문제는 Minikube가 Docker Driver 기반으로 동작하면서 NodePort를 EC2 Public Interface가 아닌 Docker Network 내부에 바인딩하는 구조였다.

따라서 AWS Security Group을 허용하더라도 외부 브라우저에서는 직접 접근할 수 없었으며 이후 `kubectl port-forward`를 이용하여 Dashboard 접근을 검증하였다.

---

### 학습 포인트

- NodePort가 정상적으로 생성되었다고 해서 외부 접근이 항상 가능한 것은 아니다.
- Minikube Docker Driver는 Docker Network 내부에서 Kubernetes Node를 실행한다.
- NodePort 자체와 클라우드 네트워크는 별도로 확인해야 한다.
- 내부 검증을 통해 문제의 위치를 정확하게 분석하는 것이 중요하다.

---

### 캡처

![NodePort 내부 검증](docs/screenshots/day4/05-argocd-nodeport-internal-access-verified.jpg)

---

### 실무 TIP

운영 환경에서는 NodePort 대신 Ingress Controller 또는 LoadBalancer를 사용하는 것이 일반적이다.

Minikube는 학습 환경이므로 Docker Driver의 네트워크 특성을 이해하는 것이 중요하다.

---

### 운영 시 고려사항

NodePort 접근 문제가 발생하면 Kubernetes Service 문제인지, 클라우드 네트워크 문제인지, Container Network 문제인지를 단계적으로 확인해야 한다.

이번 프로젝트에서는 내부 검증을 먼저 수행하여 문제 범위를 Minikube Docker Driver 네트워크로 한정할 수 있었다.


## 7-7. kubectl port-forward 구성

### 배경

NodePort가 Kubernetes 내부에서는 정상적으로 동작하는 것을 확인하였지만 EC2 Public IP를 이용한 직접 접근은 여전히 불가능하였다.

원인을 분석한 결과 Minikube(Docker Driver)가 NodePort를 Docker Network 내부에 바인딩하는 구조를 사용하기 때문이라는 것을 확인하였다.

Git Repository 연동과 GitOps 기능을 검증하기 위해서는 ArgoCD Dashboard 접근이 반드시 필요하였으므로 임시 접근 방법을 구성하였다.

---

### 목적

ArgoCD Dashboard에 접근하기 위해 Kubernetes Service와 EC2 외부 포트를 연결한다.

---

### Why?

`kubectl port-forward`는 Kubernetes Resource(Pod 또는 Service)의 포트를 로컬 또는 지정한 네트워크 인터페이스로 전달하는 기능이다.

이번 프로젝트에서는 NodePort를 이용한 직접 접근이 불가능한 Minikube(Docker Driver) 환경이므로 `kubectl port-forward`를 이용하여 EC2의 8080 포트를 ArgoCD Server와 연결하였다.

이를 통해 별도의 Ingress나 LoadBalancer를 구성하지 않고도 Dashboard를 이용한 GitOps 검증이 가능하도록 구성하였다.

---

### 사용 명령어

```bash
kubectl port-forward -n argocd svc/argocd-server 8080:443 --address 0.0.0.0
```

---

### 명령어 설명

| 명령어 | 설명 |
|---------|------|
| `kubectl port-forward` | Kubernetes Resource와 Local Port 연결 |
| `-n argocd` | argocd Namespace 지정 |
| `svc/argocd-server` | argocd-server Service 선택 |
| `8080:443` | EC2 8080 포트를 Service 443 포트와 연결 |
| `--address 0.0.0.0` | 모든 네트워크 인터페이스에서 접근 허용 |

---

### 실행 결과

ArgoCD Service의 HTTPS 포트가 EC2의 8080 포트와 연결되었으며 외부 브라우저에서 Dashboard에 정상적으로 접근할 수 있는 환경이 구성되었다.

---

### 결과 분석

`kubectl port-forward`는 Service를 직접 외부에 노출하는 것이 아니라 Kubernetes API Server를 통해 지정한 Resource와 임시 연결을 생성한다.

이번 프로젝트에서는 Minikube(Docker Driver)의 네트워크 제약을 우회하여 Dashboard 접근을 성공적으로 검증하였다.

이를 통해 Git Repository 연동과 Manual Sync, Auto Sync를 포함한 GitOps 기능을 정상적으로 테스트할 수 있었다.

---

### 학습 포인트

- `kubectl port-forward`는 Kubernetes Resource와 Local Port를 연결하는 기능이다.
- Pod뿐 아니라 Service도 Port Forward 대상이 될 수 있다.
- Minikube(Docker Driver) 환경에서는 Dashboard 접근 검증에 자주 사용된다.
- Port Forward는 임시 연결이므로 터미널을 종료하면 연결도 함께 종료된다.

---

### 캡처

![Port Forward 구성](docs/screenshots/day4/06-argocd-port-forward-configured.jpg)

---

### 실무 TIP

실무에서는 `kubectl port-forward`를 운영 환경에서 지속적으로 사용하는 경우는 거의 없다.

주로 장애 분석, 테스트, 임시 접근과 같은 운영 지원 목적으로 활용하며, 일반적인 서비스 공개는 Ingress Controller 또는 LoadBalancer를 이용한다.

---

### 운영 시 고려사항

Port Forward는 테스트와 검증을 위한 임시 연결이므로 운영 서비스 공개 방식으로 사용하는 것은 적절하지 않다.

운영 환경에서는 ALB, NLB, Ingress Controller 등을 이용하여 안정적인 접근 구조를 구성하는 것이 일반적이다.


## 7-8. ArgoCD 로그인

### 배경

ArgoCD 설치가 완료되면 Web Dashboard를 이용하여 Git Repository 등록, Kubernetes Application 생성, Sync 관리 등의 작업을 수행할 수 있다.

ArgoCD는 기본적으로 Web UI를 제공하며 최초 설치 시 관리자 계정(admin)을 자동으로 생성한다.

초기 비밀번호는 Kubernetes Secret에 저장되므로 Dashboard에 로그인하기 위해서는 먼저 Secret에서 Password를 조회하는 과정이 필요하였다.

---

### 목적

ArgoCD Dashboard에 관리자 계정으로 로그인하여 GitOps 환경을 구성한다.

---

### Why?

ArgoCD는 Kubernetes Resource를 관리하는 플랫폼이므로 무단 접근을 방지하기 위해 인증(Authentication)을 수행한다.

초기 설치 시에는 `admin` 계정이 자동 생성되며 Password는 Kubernetes Secret으로 관리된다.

이번 프로젝트에서는 Kubernetes Secret에서 초기 Password를 조회한 후 Dashboard에 로그인하여 Git Repository와 Kubernetes Application을 구성하였다.

---

### 사용 명령어

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
-o jsonpath="{.data.password}" | base64 -d
```

---

### 명령어 설명

| 명령어 | 설명 |
|---------|------|
| `kubectl get secret` | Kubernetes Secret 조회 |
| `argocd-initial-admin-secret` | ArgoCD 초기 관리자 Password 저장 Secret |
| `jsonpath` | Password 값만 추출 |
| `base64 -d` | Base64 인코딩 해제 |

---

### 실행 결과

Kubernetes Secret에서 초기 관리자 Password를 정상적으로 조회하였다.

이후 Username은 `admin`, Password는 조회한 값을 이용하여 ArgoCD Dashboard에 정상적으로 로그인하였다.

---

### 결과 분석

ArgoCD는 Kubernetes Secret을 이용하여 초기 관리자 정보를 관리한다.

Password를 조회한 후 Dashboard에 로그인함으로써 Git Repository 등록, Application 생성, Manual Sync, Auto Sync 등 GitOps 기능을 사용할 수 있는 환경이 구성되었다.

---

### 학습 포인트

- ArgoCD는 기본 관리자 계정을 자동 생성한다.
- 초기 Password는 Kubernetes Secret에 저장된다.
- Secret 값은 Base64로 저장되므로 디코딩 과정이 필요하다.
- Dashboard 로그인 이후 GitOps 관리 기능을 사용할 수 있다.

---

### 캡처

#### 초기 관리자 Password 조회

![ArgoCD Admin Password](docs/screenshots/day4/08-argocd-admin-password.jpg)

#### ArgoCD 로그인 화면

![ArgoCD Login](docs/screenshots/day4/07-argocd-login-page.jpg)

#### ArgoCD Dashboard

![ArgoCD Dashboard](docs/screenshots/day4/09-argocd-dashboard.jpg)

---

### 실무 TIP

운영 환경에서는 초기 관리자 Password를 그대로 사용하는 것이 아니라 최초 로그인 이후 즉시 Password를 변경하거나 SSO(Single Sign-On)를 연동하는 것이 일반적이다.

또한 LDAP, OAuth2, OIDC 등을 이용하여 기업 인증 체계와 연동하는 경우가 많다.

---

### 운영 시 고려사항

Kubernetes Secret은 민감한 정보를 저장하는 Resource이다.

운영 환경에서는 Secret 접근 권한(RBAC)을 최소화하고 Secret을 Git Repository에 직접 저장하지 않도록 관리해야 한다.



## 7-9. Git Repository 등록

### 배경

ArgoCD 설치와 Dashboard 구성이 완료되었지만 아직 어떤 Git Repository를 기준으로 Kubernetes를 관리할 것인지는 정의되지 않은 상태였다.

GitOps는 Git Repository를 Single Source of Truth로 사용하므로 ArgoCD가 지속적으로 감시할 Git Repository를 먼저 등록해야 한다.

이번 프로젝트에서는 GitHub Repository를 ArgoCD에 등록하여 Kubernetes Manifest를 지속적으로 동기화할 수 있는 환경을 구성하였다.

---

### 목적

GitHub Repository를 ArgoCD에 등록하여 Git Manifest를 기준으로 Kubernetes Cluster를 관리할 수 있도록 구성한다.

---

### Why?

GitOps에서는 Kubernetes를 직접 수정하지 않는다.

운영자가 Git Repository를 수정하면 ArgoCD가 Git Repository를 지속적으로 감시(Polling)하면서 변경 사항을 감지하고 Kubernetes Cluster를 원하는 상태로 유지한다.

즉,

Git Repository가 Kubernetes의 기준이 되는 Desired State를 저장하는 역할을 수행한다.

이번 프로젝트에서는 Public GitHub Repository를 사용하였기 때문에 별도의 인증 없이 HTTPS 방식으로 Repository를 등록하였다.

---

### 수행 내용

ArgoCD Dashboard의 Repository 메뉴에서 GitHub Repository를 등록하였다.

등록 정보는 다음과 같다.

| 항목 | 내용 |
|------|------|
| Connection Method | HTTP / HTTPS |
| Repository Type | Git |
| Repository URL | GitHub Repository |
| Authentication | Public Repository (인증 없음) |

Repository 등록이 완료된 이후 Connection Status가 `Successful` 상태인 것을 확인하였다.

---

### 실행 결과

GitHub Repository가 정상적으로 ArgoCD에 등록되었으며 Repository Connection Status가 Successful 상태가 되었다.

이를 통해 ArgoCD가 Git Repository를 지속적으로 감시할 수 있는 환경이 구성되었다.

---

### 결과 분석

Repository 등록 이후 ArgoCD는 Git Repository를 Source Repository로 인식하게 되었다.

다만 Repository만 등록했다고 해서 Kubernetes가 자동으로 관리되는 것은 아니다.

어떤 Manifest를 어떤 Cluster에 배포할 것인지는 Application을 생성하면서 정의하게 된다.

Repository는 GitOps의 Source를 정의하는 과정이며 실제 배포는 Application을 통해 이루어진다.

---

### 학습 포인트

- GitOps는 Git Repository를 Single Source of Truth로 사용한다.
- Repository 등록은 GitOps의 시작 단계이다.
- Repository를 등록해도 즉시 Kubernetes에 배포되지는 않는다.
- 실제 동기화 대상은 Application을 통해 정의한다.

---

### 캡처

![Git Repository Connected](docs/screenshots/day4/10-git-repository-connected.jpg)

---

### 실무 TIP

실무에서는 GitHub뿐 아니라 GitLab, Bitbucket, Azure DevOps Repository 등을 ArgoCD와 연동하여 사용할 수 있다.

또한 Private Repository를 사용하는 경우에는 Personal Access Token(PAT), SSH Key 또는 Repository Credential을 이용하여 인증을 구성한다.

---

### 운영 시 고려사항

운영 환경에서는 Git Repository 접근 권한을 최소 권한 원칙(Principle of Least Privilege)에 따라 관리하는 것이 중요하다.

또한 운영용 Repository와 개발용 Repository를 분리하여 사용하는 것이 일반적이다.


## 7-10. Kubernetes Application 생성

### 배경

GitHub Repository를 ArgoCD에 등록한 이후에도 Kubernetes Cluster에는 아무런 변경이 발생하지 않았다.

Repository는 Git Manifest를 저장하는 공간일 뿐이며, 어떤 Manifest를 어떤 Kubernetes Cluster에 배포할 것인지는 아직 정의되지 않은 상태였다.

GitOps 기반 Continuous Delivery를 수행하기 위해서는 Git Repository와 Kubernetes Cluster를 연결하는 Application을 생성해야 한다.

---

### 목적

GitHub Repository에 저장된 Kubernetes Manifest를 ArgoCD가 관리할 수 있도록 Kubernetes Application을 생성한다.

---

### Why?

ArgoCD는 Repository만 등록한다고 Kubernetes를 자동으로 관리하지 않는다.

Application은 Git Repository의 어느 Branch(Revision)를 사용할 것인지, 어떤 디렉터리(Path)의 Manifest를 사용할 것인지, 그리고 어느 Kubernetes Cluster와 Namespace에 배포할 것인지를 정의하는 핵심 객체이다.

즉 Application은 Git Repository와 Kubernetes Cluster를 연결하는 역할을 수행한다.

이번 프로젝트에서는 `k8s` 디렉터리에 저장된 Deployment와 Service Manifest를 대상으로 Application을 생성하였다.

---

### 수행 내용

ArgoCD Dashboard에서 새로운 Application을 생성하였다.

Application 구성은 다음과 같다.

| 항목 | 내용 |
|------|------|
| Application Name | flask-app |
| Project | default |
| Repository | GitHub Repository |
| Target Revision | feature/day4-argocd |
| Path | k8s |
| Cluster | https://kubernetes.default.svc |
| Namespace | default |

---

### 실행 결과

Application이 정상적으로 생성되었으며 GitHub Repository의 Kubernetes Manifest와 Kubernetes Cluster를 연결하는 GitOps 환경이 구성되었다.

초기 상태에서는 Application이 `Healthy`이면서 `OutOfSync` 상태로 표시되었다.

---

### 결과 분석

Application 생성 직후 Kubernetes Cluster에는 기존에 `kubectl apply`를 이용하여 생성된 Deployment와 Service가 이미 존재하였다.

반면 ArgoCD는 해당 리소스를 처음 관리하기 시작하는 상태였으므로 Git Manifest와 Kubernetes Resource 사이에 Tracking Annotation 차이가 발생하였다.

이로 인해 초기에는 `OutOfSync` 상태가 표시되었으며 이후 Manual Sync를 수행하여 ArgoCD 관리 대상으로 편입하였다.

---

### 학습 포인트

- Repository와 Application은 서로 다른 개념이다.
- Repository는 Git Source를 정의한다.
- Application은 Git Repository와 Kubernetes Cluster를 연결한다.
- Target Revision은 Git Branch를 의미한다.
- Path는 Kubernetes Manifest가 저장된 디렉터리를 의미한다.
- Application이 생성되어야 GitOps가 시작된다.

---

### 캡처

![Application Created](docs/screenshots/day4/11-application-created.jpg)

---

### 실무 TIP

실무에서는 개발(Develop), 스테이징(Staging), 운영(Production) 환경마다 각각 다른 Application을 생성하여 관리하는 경우가 많다.

또한 Target Revision을 `main`, `develop`, `release` 등으로 구분하여 환경별 GitOps 운영 전략을 적용한다.

---

### 운영 시 고려사항

Application 생성 시 Repository URL, Target Revision, Path, Cluster, Namespace 정보를 정확하게 설정해야 한다.

특히 Target Revision을 잘못 설정하면 의도하지 않은 Branch의 Manifest가 Kubernetes Cluster에 반영될 수 있으므로 운영 환경에서는 Branch 관리 정책을 함께 적용하는 것이 중요하다.


## 7-11. Manual Sync 검증

### 배경

Application 생성이 완료된 이후 ArgoCD Dashboard에서는 Application 상태가 `Healthy`이면서 `OutOfSync`로 표시되었다.

Kubernetes Cluster에는 Deployment와 Service가 이미 정상적으로 실행되고 있었지만 ArgoCD는 해당 리소스를 처음 관리하기 시작하는 상태였다.

따라서 Git Repository의 Desired State와 Kubernetes Cluster의 Actual State를 비교하는 과정에서 차이가 발생하였으며 이를 동기화하기 위해 Manual Sync를 수행하였다.

---

### 목적

Git Repository의 Desired State와 Kubernetes Cluster의 Actual State를 일치시켜 ArgoCD가 Kubernetes Resource를 정상적으로 관리할 수 있도록 구성한다.

---

### Why?

GitOps에서는 Git Repository가 항상 기준(Desired State)이 된다.

ArgoCD는 Git Repository와 Kubernetes Cluster를 지속적으로 비교하며 두 상태가 다르면 `OutOfSync` 상태를 표시한다.

이번 프로젝트에서는 기존에 `kubectl apply`를 이용하여 생성한 Deployment와 Service가 이미 존재하고 있었기 때문에 ArgoCD가 처음 관리 대상으로 편입하는 과정에서 OutOfSync 상태가 발생하였다.

Manual Sync를 수행하면 ArgoCD는 Kubernetes Resource를 Git Manifest 기준으로 다시 적용하며 자신의 관리 대상으로 등록한다.

---

### 수행 내용

ArgoCD Dashboard에서 `SYNC` 버튼을 선택한 후 `SYNCHRONIZE`를 실행하였다.

Sync 완료 이후 Application 상태가 `Healthy`와 `Synced` 상태로 변경되는 것을 확인하였다.

---

### 실행 결과

Git Repository의 Manifest와 Kubernetes Cluster가 정상적으로 동기화되었다.

Application 상태는 `Healthy`와 `Synced`로 변경되었으며 이후부터 ArgoCD가 해당 Kubernetes Resource를 정상적으로 관리하는 상태가 되었다.

---

### 결과 분석

Manual Sync는 Git Repository에 저장된 Manifest를 기준으로 Kubernetes Cluster를 원하는 상태(Desired State)로 맞추는 작업이다.

초기에는 Tracking Annotation이 존재하지 않아 OutOfSync 상태가 발생하였지만 Manual Sync 이후 ArgoCD가 해당 Resource를 자신의 관리 대상으로 등록하였다.

이를 통해 GitOps 기반 운영 환경이 정상적으로 구성되었음을 확인하였다.

---

### 학습 포인트

- GitOps에서는 Git Repository가 Desired State가 된다.
- Kubernetes Cluster는 Actual State를 의미한다.
- Desired State와 Actual State가 다르면 OutOfSync가 발생한다.
- Manual Sync는 두 상태를 일치시키는 과정이다.
- 최초 Sync 이후부터 ArgoCD가 Resource를 관리하게 된다.

---

### 캡처

![Manual Sync Success](docs/screenshots/day4/12-manual-sync-success.jpg)

---

### 실무 TIP

운영 환경에서는 새로운 Application을 생성한 이후 최초 한 번 Manual Sync를 수행하는 경우가 많다.

이후 Auto Sync를 활성화하면 Git 변경 사항을 자동으로 Kubernetes Cluster에 반영할 수 있다.

---

### 운영 시 고려사항

Manual Sync는 운영자가 직접 수행하는 방식이므로 승인 절차가 필요한 운영 환경에서 많이 사용된다.

반면 개발 환경에서는 Auto Sync를 활성화하여 Git 변경 사항을 자동으로 반영하는 방식이 일반적이다.


## 7-12. Deployment 변경

### 배경

Manual Sync를 완료한 이후 ArgoCD는 Git Repository와 Kubernetes Cluster를 정상적으로 동기화하는 상태가 되었다.

이제 GitOps 환경이 정상적으로 동작하는지 검증하기 위해 Git Repository의 Kubernetes Manifest를 수정하였다.

이번 프로젝트에서는 Deployment의 Replica 개수를 변경하여 Git 변경 사항이 ArgoCD를 통해 Kubernetes Cluster에 반영되는지를 확인하였다.

---

### 목적

Git Repository의 Deployment Manifest를 수정하여 GitOps 기반 Continuous Delivery 환경이 정상적으로 동작하는지 검증한다.

---

### Why?

GitOps에서는 Kubernetes를 직접 수정하지 않는다.

운영자는 Git Repository만 수정하고 Commit 및 Push를 수행한다.

ArgoCD는 Git Repository를 지속적으로 감시(Polling)하면서 변경 사항을 감지하고 Kubernetes Cluster를 원하는 상태로 유지한다.

이번 프로젝트에서는 Replica 개수를 변경하여 Git Manifest 변경이 Kubernetes Cluster에 자동으로 반영되는지를 확인하였다.

---

### 변경 내용

기존 Deployment Manifest

```yaml
replicas: 3
```

↓

변경

```yaml
replicas: 2
```

---

### 사용 명령어

```bash
git add .

git commit -m "feat(day4): update deployment replicas to 2"

git push origin feature/day4-argocd
```

---

### 명령어 설명

| 명령어 | 설명 |
|---------|------|
| `git add .` | 변경된 파일 Stage 등록 |
| `git commit` | 변경 사항 Commit |
| `git push` | GitHub Repository 반영 |

---

### 실행 결과

Deployment Manifest의 Replica 개수를 3에서 2로 변경한 후 GitHub Repository에 Push를 완료하였다.

Git Repository의 Desired State가 변경되었으며 ArgoCD는 이후 해당 변경 사항을 감지하게 되었다.

---

### 결과 분석

이번 단계에서는 Kubernetes Cluster를 직접 수정하지 않았다.

Deployment Manifest만 수정하여 GitHub Repository에 Push를 수행하였다.

즉, Git Repository만 변경하고 Kubernetes에는 아무 작업도 수행하지 않는 GitOps 운영 방식을 그대로 적용하였다.

이후 ArgoCD가 변경 사항을 감지하면서 Git Repository와 Kubernetes Cluster 간 상태 차이가 발생하였다.

---

### 학습 포인트

- GitOps에서는 Kubernetes를 직접 수정하지 않는다.
- Git Repository가 항상 Desired State가 된다.
- Deployment Manifest 변경은 Git Commit과 Push만 수행한다.
- Kubernetes 변경은 ArgoCD가 수행한다.

---

### 캡처

![Deployment Updated](docs/screenshots/day4/13-deployment-updated.jpg)

---

### 실무 TIP

운영 환경에서는 Replica 변경뿐 아니라 Image Tag 변경, Resource Limit 변경, ConfigMap 수정 등도 동일한 방식으로 Git Repository를 통해 관리한다.

Git 변경 이력이 모두 남기 때문에 변경 추적과 Rollback이 용이하다.

---

### 운영 시 고려사항

Git Repository를 직접 수정하는 것이 Kubernetes 운영의 기준이 되므로 운영 환경에서는 Branch 전략과 Code Review를 함께 적용하여 변경 사항을 관리하는 것이 중요하다.


## 7-13. OutOfSync 확인

### 배경

Deployment Manifest를 수정하여 GitHub Repository에 Push를 완료한 이후 ArgoCD Dashboard에서는 기존 `Healthy`, `Synced` 상태가 `Healthy`, `OutOfSync` 상태로 변경되었다.

이는 Git Repository의 Desired State와 Kubernetes Cluster의 Actual State가 서로 달라졌음을 의미한다.

GitOps 환경에서는 이러한 상태 차이를 ArgoCD가 지속적으로 감지하며 Kubernetes Cluster를 Git Repository의 상태와 동일하게 유지한다.

---

### 목적

Git Repository 변경 사항을 ArgoCD가 정상적으로 감지하는지 확인하고 GitOps의 동작 원리를 검증한다.

---

### Why?

GitOps에서는 Git Repository가 항상 기준(Desired State)이 된다.

반면 Kubernetes Cluster는 현재 실제로 실행되고 있는 상태(Actual State)를 의미한다.

Deployment Manifest를 수정하여 GitHub Repository에는 `replicas: 2`가 저장되었지만 Kubernetes Cluster는 여전히 `replicas: 3` 상태를 유지하고 있었다.

ArgoCD는 Git Repository와 Kubernetes Cluster를 지속적으로 비교하기 때문에 두 상태가 달라지는 순간 `OutOfSync` 상태를 표시한다.

즉, OutOfSync는 오류(Error)가 아니라 Git Repository와 Kubernetes 상태가 서로 다르다는 것을 알려주는 정상적인 GitOps 동작이다.

---

### 수행 내용

Deployment Manifest를 수정한 이후 Git Commit과 Push를 수행하였다.

ArgoCD는 Target Revision(`feature/day4-argocd`)을 기준으로 Git Repository를 감시하고 있었기 때문에 변경 사항을 자동으로 감지하였다.

---

### 실행 결과

Application 상태가 기존

```text
Healthy

Synced
```

에서

```text
Healthy

OutOfSync
```

상태로 변경되는 것을 확인하였다.

이를 통해 Git Repository 변경 사항을 ArgoCD가 정상적으로 감지하고 있음을 확인하였다.

---

### 결과 분석

OutOfSync 상태는 Git Repository의 Desired State와 Kubernetes Cluster의 Actual State가 서로 다른 상태를 의미한다.

이번 프로젝트에서는 Deployment Manifest의 Replica 개수만 변경하였기 때문에 Git Repository와 Kubernetes 사이에 상태 차이가 발생하였다.

ArgoCD는 이러한 차이를 감지하여 Sync가 필요하다는 것을 표시하였으며 이후 Manual Sync 또는 Auto Sync를 통해 두 상태를 다시 동일하게 만들 수 있다.

---

### 학습 포인트

- OutOfSync는 오류가 아니라 GitOps의 정상적인 동작이다.
- Desired State는 Git Repository를 의미한다.
- Actual State는 Kubernetes Cluster를 의미한다.
- Git Repository 변경 사항은 ArgoCD가 지속적으로 감지한다.
- Sync를 수행하면 Desired State와 Actual State가 다시 일치하게 된다.

---

### 캡처

Application이 `Healthy`와 `OutOfSync` 상태가 되는 과정은 매우 짧은 시간 안에 Auto Sync가 수행되어 별도의 스크린샷을 확보하지 못하였다.

이번 프로젝트에서는 Git 변경 사항을 ArgoCD가 정상적으로 감지한 후 Kubernetes Deployment와 Pod가 자동으로 변경되는 결과를 통해 OutOfSync 과정이 정상적으로 수행되었음을 확인하였다.

---

### 실무 TIP

운영 환경에서는 OutOfSync 상태가 발생하면 즉시 Sync하지 않고 변경 내용을 먼저 검토하는 경우가 많다.

특히 Production 환경에서는 승인 절차를 거친 후 Manual Sync를 수행하거나 Auto Sync 정책을 환경별로 다르게 적용하는 것이 일반적이다.

---

### 운영 시 고려사항

OutOfSync 상태가 장시간 유지되는 경우 Git Repository와 Kubernetes Cluster 간 구성 불일치(Configuration Drift)가 발생할 수 있다.

운영 환경에서는 Drift Detection 정책을 통해 OutOfSync 상태를 지속적으로 모니터링하고 필요한 경우 자동 또는 수동으로 동기화를 수행한다.


## 7-14. Auto Sync 구성

### 배경

Manual Sync를 이용하여 Git Repository와 Kubernetes Cluster를 동기화하는 과정까지 검증하였다.

그러나 GitOps의 핵심은 운영자가 직접 Sync 버튼을 누르는 것이 아니라 Git Repository 변경 사항을 자동으로 Kubernetes Cluster에 반영하는 것이다.

이번 프로젝트에서는 Auto Sync 기능을 활성화하여 Git Push만으로 Kubernetes Deployment와 Pod가 자동으로 변경되는 환경을 구성하였다.

---

### 목적

ArgoCD의 Auto Sync 기능을 활성화하여 Git Repository 변경 사항을 Kubernetes Cluster에 자동으로 반영한다.

---

### Why?

Manual Sync는 운영자가 직접 Sync를 수행해야 한다.

반면 Auto Sync는 Git Repository를 지속적으로 감시하면서 변경 사항이 발생하면 ArgoCD가 자동으로 Kubernetes Cluster를 원하는 상태로 유지한다.

즉 운영자는 Kubernetes를 직접 수정하지 않고 Git Repository만 수정하면 되므로 GitOps 운영 방식이 완성된다.

이번 프로젝트에서는 Auto Sync를 활성화하여 Git Push 이후 Kubernetes Deployment와 Pod가 자동으로 변경되는 환경을 검증하였다.

---

### 수행 내용

Application 설정에서 Auto Sync를 활성화하였다.

추가로 다음 옵션을 함께 활성화하였다.

- Prune Resources
- Self Heal

---

### 옵션 설명

| 옵션 | 설명 |
|------|------|
| Auto Sync | Git 변경 사항을 자동으로 Kubernetes에 반영 |
| Prune Resources | Git에서 삭제된 Resource를 Kubernetes에서도 자동 삭제 |
| Self Heal | Kubernetes Resource가 변경되면 Git 상태로 자동 복구 |

---

### 실행 결과

Application의 Sync Policy가 Manual에서 Automated로 변경되었다.

이후 Git Repository 변경 사항을 사람이 직접 Sync하지 않아도 ArgoCD가 자동으로 감지하여 Kubernetes Cluster를 원하는 상태로 유지할 수 있는 환경이 구성되었다.

---

### 결과 분석

Auto Sync는 GitOps의 핵심 기능이다.

Git Repository를 기준으로 Kubernetes Cluster를 지속적으로 동기화하므로 운영자는 Kubernetes를 직접 수정할 필요가 없다.

또한 Self Heal 기능을 활성화함으로써 운영 중 Kubernetes Resource가 임의로 변경되더라도 Git Repository 상태로 자동 복구할 수 있는 환경을 구성하였다.

---

### 학습 포인트

- Auto Sync는 Git 변경 사항을 자동으로 Kubernetes에 반영한다.
- Manual Sync와 Auto Sync는 운영 방식이 다르다.
- Self Heal은 Kubernetes Resource Drift를 자동으로 복구한다.
- Prune은 Git에서 삭제된 Resource를 Kubernetes에서도 제거한다.

---

### 캡처

![Auto Sync Enabled](docs/screenshots/day4/18-auto-sync-enabled.jpg)

---

### 실무 TIP

개발 환경에서는 Auto Sync를 활성화하여 빠른 배포를 수행하는 경우가 많다.

반면 운영 환경에서는 승인 절차를 위해 Manual Sync를 유지하거나 Auto Sync를 제한적으로 사용하는 경우도 많다.

환경의 특성에 따라 Sync Policy를 구분하여 운영하는 것이 일반적이다.

---

### 운영 시 고려사항

Auto Sync를 활성화하면 Git Repository 변경 사항이 즉시 Kubernetes Cluster에 반영된다.

따라서 운영 환경에서는 Branch 보호 정책(Branch Protection), Pull Request 승인, Code Review 등을 함께 적용하여 의도하지 않은 변경 사항이 운영 환경에 반영되지 않도록 관리해야 한다.



## 7-15. GitOps 자동 동기화 검증

### 배경

Auto Sync를 활성화한 이후 Git Repository를 수정하면 ArgoCD가 변경 사항을 자동으로 감지하여 Kubernetes Cluster를 원하는 상태로 유지해야 한다.

이번 프로젝트에서는 Deployment Manifest의 Replica 개수를 변경한 뒤 GitHub Repository에 Push하여 GitOps 기반 Continuous Delivery 환경이 정상적으로 동작하는지를 최종 검증하였다.

---

### 목적

Git Repository 변경 사항이 ArgoCD를 통해 Kubernetes Deployment와 Pod에 자동으로 반영되는지 확인한다.

---

### Why?

GitOps에서는 Git Repository가 항상 시스템의 기준(Desired State)이 된다.

운영자는 Kubernetes Cluster를 직접 수정하지 않고 Git Repository만 변경한다.

ArgoCD는 Git Repository를 지속적으로 감시(Polling)하면서 변경 사항을 감지하고 Kubernetes Cluster를 Git Repository와 동일한 상태로 유지한다.

이번 프로젝트에서는 Replica 개수를 변경하여 Git Push 이후 Deployment와 Pod가 자동으로 변경되는 과정을 검증하였다.

---

### 수행 내용

Deployment Manifest의 Replica 개수를 변경하였다.

```yaml
replicas: 3
```

↓

```yaml
replicas: 2
```

이후 Git Commit과 Push를 수행하였다.

ArgoCD는 Target Revision(feature/day4-argocd)을 기준으로 변경 사항을 자동 감지하였으며 Auto Sync를 수행하였다.

---

### 사용 명령어

```bash
git add .

git commit -m "feat(day4): update deployment replicas to 2"

git push origin feature/day4-argocd

kubectl get deployment

kubectl get pods
```

---

### 명령어 설명

| 명령어 | 설명 |
|---------|------|
| `git add .` | 변경 파일 Stage 등록 |
| `git commit` | 변경 사항 Commit |
| `git push` | GitHub Repository 반영 |
| `kubectl get deployment` | Deployment 상태 확인 |
| `kubectl get pods` | Pod 상태 확인 |

---

### 실행 결과

Git Push 이후 ArgoCD가 Git Repository 변경 사항을 자동으로 감지하였다.

운영자가 별도로 Sync를 수행하지 않았음에도 Deployment Replica 개수가 자동으로 변경되었으며 Pod 역시 3개에서 2개로 자동 조정되는 것을 확인하였다.

최종적으로 Application 상태는 `Healthy`, `Synced` 상태를 유지하였다.

---

### 결과 분석

이번 검증을 통해 Git Repository만 수정하면 Kubernetes Cluster가 자동으로 원하는 상태를 유지하는 GitOps 운영 방식을 확인하였다.

GitHub Actions는 Docker Image를 생성하는 CI 역할을 수행하고, ArgoCD는 Git Repository 변경 사항을 Kubernetes Cluster에 자동 반영하는 CD 역할을 수행하였다.

이를 통해 CI와 CD가 하나의 파이프라인으로 연결되는 구조를 구축하였다.

---

### GitOps 전체 동작 흐름

```text
Developer

↓

Git Commit

↓

Git Push

↓

GitHub Repository

↓

ArgoCD

↓

Auto Sync

↓

Deployment Update

↓

ReplicaSet Update

↓

Pod Update

↓

Healthy / Synced
```

---

### 학습 포인트

- Git Repository가 항상 Desired State가 된다.
- Git Push만으로 Kubernetes Cluster가 자동 변경된다.
- Deployment 변경은 ReplicaSet을 통해 Pod 변경으로 이어진다.
- Auto Sync를 이용하면 운영자가 직접 Sync를 수행할 필요가 없다.
- GitHub Actions(CI)와 ArgoCD(CD)가 하나의 DevOps Pipeline을 구성한다.

---

### 캡처

#### Auto Sync 활성화

![Auto Sync Enabled](docs/screenshots/day4/18-auto-sync-enabled.jpg)

#### Deployment 자동 변경

![Deployment Updated](docs/screenshots/day4/15-replicas-sync-success.jpg)

#### Pod 자동 변경

![Kubernetes Pods Auto Updated](docs/screenshots/day4/19-kubernetes-pods-auto-updated.jpg)

---

### 실무 TIP

운영 환경에서는 Auto Sync를 이용하여 애플리케이션을 자동 배포하되, 운영 Branch 보호 정책과 Pull Request 승인 절차를 함께 적용하는 것이 일반적이다.

또한 Image Tag를 Git Commit SHA와 함께 관리하여 원하는 시점으로 쉽게 Rollback할 수 있도록 구성한다.

---

### 운영 시 고려사항

GitOps 환경에서는 Kubernetes를 직접 수정하는 것이 아니라 Git Repository를 통해 변경 사항을 관리해야 한다.

운영자가 `kubectl edit` 또는 `kubectl scale` 등을 이용하여 직접 변경하면 Git Repository와 Kubernetes Cluster 간 Drift가 발생할 수 있으며, Self Heal 기능이 활성화된 경우 Git Repository 상태로 자동 복구된다.


# 8. 핵심 기술 이해

---

## 8-1. GitOps란?

### GitOps의 정의

GitOps(Git Operations)는 Git Repository를 시스템의 단일 진실 공급원(Single Source of Truth)으로 사용하는 운영 방식이다.

애플리케이션의 배포와 운영 상태를 Git Repository에서 관리하며 Kubernetes Cluster는 항상 Git Repository의 상태와 동일하도록 유지된다.

운영자는 Kubernetes Cluster를 직접 수정하지 않고 Git Repository만 변경하며, GitOps 플랫폼(ArgoCD)이 변경 사항을 자동으로 감지하여 Kubernetes Cluster를 원하는 상태(Desired State)로 유지한다.

---

### GitOps를 사용하는 이유

기존 Kubernetes 운영 방식에서는 운영자가 직접 `kubectl apply`, `kubectl edit`, `kubectl scale` 등의 명령어를 이용하여 Cluster를 수정하였다.

이 방식은 변경 이력이 남지 않거나 운영자마다 작업 방식이 달라질 수 있다는 문제가 있다.

GitOps는 모든 변경 사항을 Git Repository에서 관리하기 때문에 변경 이력 추적, 코드 리뷰, 승인 절차, Rollback 등을 하나의 Git Workflow 안에서 수행할 수 있다.

---

### 기존 운영 방식

```text
Developer

↓

kubectl apply

↓

Kubernetes
```

운영자가 직접 Kubernetes를 수정한다.

---

### GitOps 운영 방식

```text
Developer

↓

Git Commit

↓

Git Push

↓

Git Repository

↓

ArgoCD

↓

Kubernetes
```

Git Repository만 수정하면 ArgoCD가 Kubernetes Cluster를 자동으로 동기화한다.

---

### 이번 프로젝트에서 GitOps

이번 프로젝트에서는 GitHub Repository를 Single Source of Truth로 사용하였다.

Deployment Manifest의 Replica 개수를 변경한 후 GitHub Repository에 Push를 수행하였으며 ArgoCD가 이를 자동으로 감지하여 Kubernetes Deployment와 Pod를 자동으로 변경하는 것을 확인하였다.

즉 Kubernetes Cluster를 직접 수정하지 않고 Git Repository만 변경하여 운영하는 GitOps 방식을 구현하였다.

---

### GitOps의 장점

- Git 기반 변경 이력 관리
- 변경 사항 추적(Audit)
- Rollback 용이
- 운영 자동화
- GitHub 기반 협업 가능
- Kubernetes Drift 자동 복구

---

### 학습 포인트

- GitOps는 Git Repository를 기준으로 운영한다.
- Kubernetes는 Git Repository와 동일한 상태를 유지한다.
- Git 변경 사항은 자동으로 Kubernetes Cluster에 반영될 수 있다.
- GitOps는 Infrastructure as Code(IaC) 운영 방식과 밀접한 관계를 가진다.

---

### 실무 TIP

최근 Kubernetes 운영 환경에서는 ArgoCD, FluxCD와 같은 GitOps 플랫폼을 이용하여 Git 기반 운영 방식을 적용하는 경우가 많다.

운영자는 Kubernetes Cluster를 직접 수정하지 않고 Git Repository를 수정하는 방식으로 운영하여 변경 이력과 운영 정책을 일관성 있게 관리한다.

---

### 운영 시 고려사항

GitOps 환경에서는 Git Repository가 운영 환경의 기준이 되므로 Branch Protection, Pull Request, Code Review 등의 Git 운영 정책을 함께 적용하는 것이 중요하다.

또한 운영자가 Kubernetes Cluster를 직접 수정하는 것을 최소화하여 Configuration Drift를 방지해야 한다.


## 8-2. ArgoCD란?

### ArgoCD의 정의

ArgoCD는 Kubernetes를 위한 GitOps 기반 Continuous Delivery(CD) 플랫폼이다.

Git Repository를 지속적으로 감시(Polling)하면서 Git에 저장된 Desired State와 Kubernetes Cluster의 Actual State를 비교하고, 두 상태가 다를 경우 자동으로 Kubernetes를 Git 상태와 동일하게 유지한다.

ArgoCD는 CNCF(Cloud Native Computing Foundation)의 Graduated 프로젝트이며 Kubernetes 환경에서 가장 널리 사용되는 GitOps 플랫폼 중 하나이다.

---

### ArgoCD를 사용하는 이유

기존 Kubernetes 운영에서는 운영자가 직접 `kubectl apply`를 수행하여 Deployment를 수정하였다.

이 방식은 운영자의 실수(Human Error)가 발생할 수 있으며, 누가 언제 어떤 설정을 변경했는지 추적하기 어렵다.

ArgoCD를 사용하면 Git Repository를 기준으로 Kubernetes Cluster를 자동으로 관리할 수 있으므로 운영 표준화와 변경 이력 관리가 가능하다.

또한 Git Repository만 수정하면 Kubernetes Cluster가 자동으로 변경되므로 GitOps 기반 운영 환경을 구축할 수 있다.

---

### ArgoCD 주요 구성 요소

ArgoCD는 여러 개의 Kubernetes Pod로 구성된다.

각 구성 요소는 서로 다른 역할을 수행하며 함께 GitOps 기능을 제공한다.

| 구성 요소 | 역할 |
|-----------|------|
| argocd-server | Web Dashboard 및 API 제공 |
| argocd-repo-server | Git Repository와 통신 및 Manifest 조회 |
| argocd-application-controller | Desired State와 Actual State 비교 및 Sync 수행 |
| argocd-applicationset-controller | ApplicationSet 관리 |
| argocd-dex-server | 사용자 인증(Authentication) |
| argocd-notifications-controller | 이벤트 및 알림 관리 |
| argocd-redis | Cache 저장 |

---

### ArgoCD 구조

```text
GitHub Repository

        │

Repository Server

        │

Application Controller

        │

Kubernetes API Server

        │

Deployment

        │

ReplicaSet

        │

Pod
```

Repository Server는 Git Repository를 조회한다.

Application Controller는 Git Repository와 Kubernetes Cluster를 비교한다.

차이가 발생하면 Kubernetes API Server를 통해 Deployment를 수정하여 Git 상태와 동일하게 유지한다.

---

### 이번 프로젝트에서 ArgoCD 역할

이번 프로젝트에서는 GitHub Repository를 ArgoCD에 등록하고 Kubernetes Application을 생성하였다.

Deployment Manifest를 수정한 후 GitHub Repository에 Push를 수행하였으며 ArgoCD가 변경 사항을 자동으로 감지하여 Kubernetes Deployment와 Pod를 자동으로 변경하는 것을 확인하였다.

이를 통해 GitHub Repository를 Single Source of Truth로 사용하는 GitOps 기반 Continuous Delivery 환경을 구축하였다.

---

### ArgoCD의 장점

- Git 기반 운영
- Kubernetes 자동 동기화
- Configuration Drift 자동 감지
- Rollback 지원
- Web Dashboard 제공
- Manual Sync / Auto Sync 지원

---

### 학습 포인트

- ArgoCD는 GitOps 기반 CD 플랫폼이다.
- Git Repository를 지속적으로 감시한다.
- Desired State와 Actual State를 비교한다.
- Kubernetes Cluster를 Git 상태와 동일하게 유지한다.
- Manual Sync와 Auto Sync를 모두 지원한다.

---

### 실무 TIP

최근 Kubernetes 운영 환경에서는 Jenkins와 같은 기존 CD 방식보다 ArgoCD나 FluxCD를 이용한 GitOps 운영 방식이 빠르게 확산되고 있다.

특히 Amazon EKS, Azure AKS, Google GKE 환경에서는 GitOps를 기본 운영 방식으로 적용하는 기업이 증가하고 있다.

---

### 운영 시 고려사항

ArgoCD는 Git Repository를 기준으로 Kubernetes Cluster를 관리하므로 운영자가 `kubectl edit`, `kubectl scale` 등으로 직접 리소스를 수정하면 Configuration Drift가 발생할 수 있다.

운영 환경에서는 Git Repository를 통한 변경만 허용하는 운영 정책을 적용하는 것이 일반적이다.



## 8-3. Desired State와 Actual State

### Desired State란?

Desired State는 Git Repository에 정의되어 있는 "원하는 시스템 상태"를 의미한다.

Git Repository에 저장된 Kubernetes Manifest(YAML)는 Kubernetes Cluster가 반드시 유지해야 하는 목표 상태이며, GitOps에서는 이 Desired State가 시스템의 기준이 된다.

운영자는 Kubernetes Cluster를 직접 수정하지 않고 Git Repository만 변경하여 Desired State를 정의한다.

---

### Actual State란?

Actual State는 현재 Kubernetes Cluster에서 실제로 실행되고 있는 상태를 의미한다.

Deployment, ReplicaSet, Pod, Service 등 Kubernetes Resource가 현재 어떤 상태로 동작하고 있는지를 나타낸다.

Actual State는 운영 중 다양한 이유로 Desired State와 달라질 수 있으며 ArgoCD는 이러한 차이를 지속적으로 감시한다.

---

### Desired State와 Actual State 비교

GitOps에서는 항상 두 가지 상태를 비교한다.

```text
Desired State

↓

Git Repository

────────────────────────

Actual State

↓

Kubernetes Cluster
```

두 상태가 동일하면

```text
Synced
```

상태가 된다.

반대로 두 상태가 다르면

```text
OutOfSync
```

상태가 된다.

---

### 이번 프로젝트에서 Desired State

이번 프로젝트에서는 GitHub Repository에 저장된 Deployment Manifest가 Desired State 역할을 수행하였다.

예를 들어

```yaml
replicas: 2
```

로 Git Repository를 수정하면

Desired State는 Replica 2개가 된다.

---

### 이번 프로젝트에서 Actual State

Git Repository를 수정한 직후 Kubernetes Cluster는 기존 Replica 3개를 그대로 유지하고 있었다.

즉

```text
Desired State

↓

Replica 2

────────────────────

Actual State

↓

Replica 3
```

상태가 되었으며 ArgoCD는 이를 감지하여 OutOfSync 상태를 표시하였다.

이후 Auto Sync가 수행되면서 Kubernetes Deployment와 Pod가 자동으로 Replica 2개로 변경되었고 다시 Synced 상태가 되었다.

---

### Desired State와 Actual State 동작 과정

```text
Git Repository 수정

↓

Desired State 변경

↓

ArgoCD 감지

↓

OutOfSync

↓

Auto Sync

↓

Deployment 변경

↓

ReplicaSet 변경

↓

Pod 변경

↓

Synced
```

---

### 이번 프로젝트에서 검증한 내용

Deployment Manifest의 Replica 개수를

```yaml
replicas: 3
```

에서

```yaml
replicas: 2
```

로 변경하였다.

Git Push 이후 ArgoCD는 Desired State가 변경되었음을 감지하였으며 Kubernetes Deployment와 Pod를 자동으로 변경하였다.

이를 통해 Desired State와 Actual State 동기화 과정을 직접 검증하였다.

---

### 학습 포인트

- Desired State는 Git Repository를 의미한다.
- Actual State는 Kubernetes Cluster를 의미한다.
- 두 상태가 다르면 OutOfSync가 된다.
- Sync 이후 Desired State와 Actual State는 다시 동일해진다.
- GitOps는 항상 Desired State를 기준으로 운영된다.

---

### 실무 TIP

GitOps 환경에서는 운영자가 Kubernetes Cluster를 직접 수정하지 않는다.

모든 변경은 Git Repository를 통해 수행하며 ArgoCD가 Desired State를 기준으로 Kubernetes Cluster를 지속적으로 유지한다.

---

### 운영 시 고려사항

운영자가 `kubectl edit`, `kubectl scale` 등을 이용하여 직접 Kubernetes Resource를 변경하면 Desired State와 Actual State가 달라지면서 Configuration Drift가 발생할 수 있다.

Self Heal 기능이 활성화되어 있는 경우 ArgoCD는 이러한 변경 사항을 감지하여 Git Repository의 Desired State로 자동 복구한다.


## 8-4. Sync란?

### Sync의 정의

Sync는 Git Repository의 Desired State와 Kubernetes Cluster의 Actual State를 동일한 상태로 만드는 과정을 의미한다.

ArgoCD는 Git Repository를 지속적으로 감시하면서 Desired State와 Actual State를 비교한다.

두 상태가 서로 다르면 OutOfSync 상태를 표시하며 Sync를 수행하여 Kubernetes Cluster를 Git Repository와 동일한 상태로 변경한다.

즉 Sync는 GitOps에서 Desired State를 Actual State에 반영하는 핵심 기능이다.

---

### Sync를 사용하는 이유

Git Repository는 운영자가 원하는 최종 상태를 정의한다.

그러나 Kubernetes Cluster는 운영 중 Replica 변경, Resource 수정, 장애 복구 등 다양한 이유로 Git Repository와 다른 상태가 될 수 있다.

ArgoCD는 이러한 차이를 지속적으로 감지하고 Sync를 수행하여 Kubernetes Cluster를 항상 Git Repository와 동일하게 유지한다.

이를 통해 운영 환경의 일관성과 재현성을 확보할 수 있다.

---

### Sync 동작 과정

```text
Git Repository

↓

Desired State

↓

ArgoCD 비교

↓

OutOfSync

↓

Sync

↓

Kubernetes Deployment

↓

ReplicaSet

↓

Pod

↓

Synced
```

---

### 이번 프로젝트에서 Sync

이번 프로젝트에서는 Deployment Manifest의 Replica 개수를 변경하여 GitHub Repository에 Push하였다.

Git Push 이후 ArgoCD는 Desired State와 Actual State가 서로 다르다는 것을 감지하여 OutOfSync 상태를 표시하였다.

이후 Sync를 수행하면서 Deployment, ReplicaSet, Pod가 새로운 Replica 개수로 변경되었으며 최종적으로 Application 상태가 Synced로 변경되는 것을 확인하였다.

---

### Sync 수행 대상

ArgoCD는 Deployment뿐 아니라 다양한 Kubernetes Resource를 Sync할 수 있다.

대표적인 대상은 다음과 같다.

- Deployment
- ReplicaSet
- Pod
- Service
- ConfigMap
- Secret
- Ingress
- NetworkPolicy
- PersistentVolumeClaim

즉 Git Repository에 정의된 대부분의 Kubernetes Manifest를 Sync 대상으로 관리할 수 있다.

---

### 학습 포인트

- Sync는 Desired State를 Actual State에 반영하는 과정이다.
- OutOfSync 상태가 발생하면 Sync를 수행하여 두 상태를 동일하게 만든다.
- ArgoCD는 다양한 Kubernetes Resource를 Sync할 수 있다.
- Sync는 GitOps 운영의 핵심 기능이다.

---

### 실무 TIP

실무에서는 Sync 수행 전 Diff 기능을 이용하여 Git Repository와 Kubernetes Cluster의 차이를 먼저 확인하는 경우가 많다.

이를 통해 운영자가 변경 내용을 검토한 후 Manual Sync를 수행하거나 Auto Sync 정책에 따라 자동 반영하도록 운영한다.

---

### 운영 시 고려사항

운영 환경에서는 Sync가 Kubernetes Cluster에 직접 영향을 주므로 변경 사항을 충분히 검토한 후 수행하는 것이 중요하다.

특히 Production 환경에서는 Branch 보호 정책, Pull Request 승인, Code Review 등을 함께 적용하여 안전하게 Sync를 수행하는 것이 일반적이다.


## 8-5. Manual Sync

### Manual Sync의 정의

Manual Sync는 운영자가 직접 ArgoCD Dashboard에서 Sync를 수행하는 방식이다.

Application이 OutOfSync 상태가 되면 운영자가 변경 내용을 확인한 후 직접 Sync 버튼을 선택하여 Kubernetes Cluster를 Git Repository의 상태와 동일하게 만든다.

즉 운영자의 승인(Approval)을 기반으로 Kubernetes를 변경하는 GitOps 운영 방식이다.

---

### Manual Sync를 사용하는 이유

운영 환경에서는 Git Repository가 변경되었다고 해서 즉시 Kubernetes Cluster를 변경하는 것이 항상 적절한 것은 아니다.

특히 Production 환경에서는 변경 사항을 충분히 검토한 후 운영자가 승인하여 반영하는 절차가 필요하다.

Manual Sync는 이러한 운영 절차를 지원하기 위해 제공되는 기능이다.

---

### Manual Sync 동작 과정

```text
Git Repository 변경

↓

Desired State 변경

↓

ArgoCD

↓

OutOfSync

↓

운영자 승인

↓

Manual Sync

↓

Deployment 변경

↓

ReplicaSet 변경

↓

Pod 변경

↓

Synced
```

---

### 이번 프로젝트에서 Manual Sync

이번 프로젝트에서는 Application 생성 직후 ArgoCD가 기존 Kubernetes Resource를 처음 관리하는 과정에서 `OutOfSync` 상태가 발생하였다.

운영자가 직접 Manual Sync를 수행하여 Deployment와 Service를 ArgoCD 관리 대상으로 편입하였다.

Sync 완료 이후 Application 상태가 `Healthy`, `Synced` 상태로 변경되는 것을 확인하였다.

---

### Manual Sync의 장점

- 운영자가 변경 사항을 직접 검토할 수 있다.
- 승인 절차를 적용할 수 있다.
- 운영 환경 변경을 통제하기 쉽다.
- Production 환경에 적합하다.

---

### Manual Sync의 단점

- 운영자가 직접 Sync를 수행해야 한다.
- 즉시 반영이 어렵다.
- 반복적인 운영 작업이 발생할 수 있다.

---

### 학습 포인트

- Manual Sync는 운영자가 직접 수행한다.
- OutOfSync 상태를 Synced 상태로 변경한다.
- 운영 승인 절차에 적합하다.
- Production 환경에서 많이 사용된다.

---

### 실무 TIP

실무에서는 Production 환경에서 Manual Sync를 사용하는 경우가 많다.

개발 환경에서는 Auto Sync를 사용하더라도 운영 환경은 Pull Request 승인, Change Request 승인 등을 거친 후 Manual Sync를 수행하는 경우가 일반적이다.

---

### 운영 시 고려사항

Manual Sync를 수행하기 전에 Git Repository와 Kubernetes Cluster의 차이(Diff)를 충분히 검토하는 것이 중요하다.

운영 환경에서는 승인되지 않은 변경 사항이 반영되지 않도록 운영 정책과 함께 사용하는 것이 일반적이다.


## 8-6. Auto Sync

### Auto Sync의 정의

Auto Sync는 Git Repository의 변경 사항을 ArgoCD가 자동으로 감지하여 Kubernetes Cluster에 반영하는 기능이다.

운영자가 직접 Sync를 수행하지 않아도 Git Repository와 Kubernetes Cluster를 지속적으로 비교하며 Desired State와 Actual State가 다를 경우 자동으로 Sync를 수행한다.

즉 Git Repository만 수정하면 Kubernetes Cluster가 자동으로 원하는 상태를 유지하는 GitOps 운영 방식의 핵심 기능이다.

---

### Auto Sync를 사용하는 이유

GitOps의 목적은 운영자가 Kubernetes를 직접 수정하지 않고 Git Repository만 수정하여 운영하는 것이다.

Manual Sync는 운영자가 직접 Sync를 수행해야 하지만 Auto Sync는 Git Repository 변경 사항을 자동으로 감지하여 Kubernetes Cluster를 원하는 상태로 유지한다.

이를 통해 반복적인 운영 작업을 줄이고 운영 자동화를 구현할 수 있다.

---

### Auto Sync 동작 과정

```text
Git Repository 변경

↓

Desired State 변경

↓

ArgoCD 감지

↓

OutOfSync

↓

Auto Sync

↓

Deployment 변경

↓

ReplicaSet 변경

↓

Pod 변경

↓

Healthy

↓

Synced
```

---

### 이번 프로젝트에서 Auto Sync

이번 프로젝트에서는 Deployment Manifest의 Replica 개수를 변경한 후 GitHub Repository에 Push하였다.

Application의 Sync Policy를 Auto Sync로 변경한 상태였기 때문에 운영자가 별도로 Sync 버튼을 누르지 않아도 ArgoCD가 Git 변경 사항을 자동으로 감지하였다.

이후 Deployment Replica 개수가 자동으로 변경되었으며 Pod 역시 새로운 Replica 개수에 맞게 자동으로 재구성되는 것을 확인하였다.

최종적으로 Application 상태는 다시 `Healthy`, `Synced` 상태가 되었다.

---

### Auto Sync 구성 옵션

이번 프로젝트에서는 다음 옵션을 함께 활성화하였다.

| 옵션 | 역할 |
|------|------|
| Auto Sync | Git 변경 사항 자동 반영 |
| Prune Resources | Git에서 삭제된 Resource를 Kubernetes에서도 자동 삭제 |
| Self Heal | Kubernetes Resource 변경 시 Git 상태로 자동 복구 |

---

### Auto Sync의 장점

- Git Push만으로 자동 배포 가능
- 운영 자동화
- Configuration Drift 자동 복구
- 운영자 개입 최소화
- GitOps 운영 방식 구현

---

### Auto Sync의 단점

- Git Repository 변경 사항이 즉시 반영된다.
- 운영 환경에서는 승인 절차가 어려울 수 있다.
- 잘못된 Manifest도 자동으로 반영될 수 있다.

---

### 학습 포인트

- Auto Sync는 GitOps의 핵심 기능이다.
- Git Repository 변경 사항을 자동으로 Kubernetes에 반영한다.
- 운영자가 직접 Sync를 수행하지 않는다.
- Self Heal과 Prune 기능을 함께 사용할 수 있다.
- Git Push만으로 Deployment와 Pod가 자동 변경된다.

---

### 실무 TIP

개발(Development) 환경에서는 Auto Sync를 활성화하여 빠른 배포를 수행하는 경우가 많다.

반면 운영(Production) 환경에서는 Branch Protection, Pull Request 승인, Code Review 등의 절차를 함께 적용하여 의도하지 않은 변경 사항이 자동으로 반영되지 않도록 운영하는 것이 일반적이다.

---

### 운영 시 고려사항

Auto Sync를 활성화하면 Git Repository가 운영 환경의 기준이 되므로 Git Repository 관리 정책이 매우 중요해진다.

운영 환경에서는 Feature Branch, Develop Branch, Main Branch를 구분하여 운영하고 Branch Protection을 적용하는 것이 일반적이다.

또한 Auto Sync를 사용할 경우 Git Repository 변경 사항이 즉시 운영 환경에 반영될 수 있으므로 변경 관리(Change Management) 정책을 함께 적용해야 한다.


## 8-7. Application이란?

### Application의 정의

Application은 ArgoCD에서 Git Repository와 Kubernetes Cluster를 연결하는 가장 핵심적인 객체이다.

Git Repository에 저장된 Kubernetes Manifest를 어떤 Kubernetes Cluster와 Namespace에 배포할 것인지 정의하는 역할을 수행한다.

Repository가 Git Source를 의미한다면, Application은 실제 GitOps 운영 정책을 정의하는 객체라고 볼 수 있다.

---

### Application을 사용하는 이유

Git Repository를 ArgoCD에 등록했다고 해서 Kubernetes Cluster가 자동으로 관리되는 것은 아니다.

ArgoCD는 어떤 Repository를 사용할 것인지뿐 아니라 어떤 Branch(Revision), 어떤 디렉터리(Path), 어느 Kubernetes Cluster와 Namespace에 배포할 것인지를 알아야 한다.

이러한 정보를 정의하는 것이 Application이다.

Application이 생성되어야 비로소 Git Repository와 Kubernetes Cluster가 연결되며 GitOps 기반 Continuous Delivery가 시작된다.

---

### Application 구성 요소

이번 프로젝트에서 생성한 Application은 다음과 같이 구성하였다.

| 항목 | 내용 |
|------|------|
| Name | flask-app |
| Project | default |
| Repository | GitHub Repository |
| Target Revision | feature/day4-argocd |
| Path | k8s |
| Cluster | https://kubernetes.default.svc |
| Namespace | default |

---

### Application 동작 과정

```text
Git Repository

↓

Application

↓

Deployment

↓

ReplicaSet

↓

Pod
```

Application은 Git Repository의 Manifest를 Kubernetes Resource로 연결하는 역할을 수행한다.

---

### 이번 프로젝트에서 Application

이번 프로젝트에서는 `flask-app`이라는 Application을 생성하였다.

Application 생성 이후 ArgoCD는 GitHub Repository의 `k8s` 디렉터리를 지속적으로 감시하게 되었으며 Deployment와 Service Manifest를 Kubernetes Cluster와 자동으로 동기화하였다.

또한 Deployment Manifest의 Replica 변경 사항을 자동으로 감지하여 Kubernetes Deployment와 Pod를 자동으로 변경하는 것을 확인하였다.

---

### Application의 장점

- Git Repository와 Kubernetes Cluster 연결
- GitOps 운영 기준 제공
- Branch별 운영 가능
- Namespace별 배포 가능
- 여러 Application을 독립적으로 관리 가능

---

### 학습 포인트

- Application은 ArgoCD의 핵심 객체이다.
- Repository와 Kubernetes를 연결한다.
- Branch, Path, Namespace를 함께 관리한다.
- Application이 생성되어야 GitOps가 시작된다.

---

### 실무 TIP

실무에서는 개발(Development), 스테이징(Staging), 운영(Production) 환경마다 별도의 Application을 생성하여 관리하는 경우가 많다.

또한 하나의 Repository에서 여러 Application을 운영하여 MSA(Microservice Architecture)를 구성하는 경우도 많다.

---

### 운영 시 고려사항

Application 생성 시 Target Revision, Path, Namespace를 정확하게 설정해야 한다.

특히 잘못된 Branch를 지정하면 의도하지 않은 Kubernetes Manifest가 운영 환경에 반영될 수 있으므로 환경별 Branch 운영 정책을 함께 적용하는 것이 중요하다.


## 8-8. Repository란?

### Repository의 정의

Repository는 ArgoCD가 Kubernetes Manifest를 가져오는 Git Source를 의미한다.

GitHub, GitLab, Bitbucket, Azure DevOps 등 Git 기반 형상관리 시스템을 사용할 수 있으며, ArgoCD는 등록된 Repository를 지속적으로 감시하여 변경 사항을 확인한다.

Repository는 GitOps에서 Desired State를 저장하는 저장소 역할을 수행한다.

---

### Repository를 사용하는 이유

GitOps에서는 Kubernetes Cluster를 직접 수정하지 않는다.

운영자가 Git Repository를 수정하면 ArgoCD가 이를 감지하여 Kubernetes Cluster를 원하는 상태로 유지한다.

즉 Repository는 Kubernetes 운영 환경의 기준이 되는 Manifest를 저장하는 공간이며 모든 변경 사항은 Git Commit과 Push를 통해 관리된다.

이를 통해 변경 이력 관리, Code Review, Rollback, 협업 환경을 하나의 Git Workflow 안에서 수행할 수 있다.

---

### 이번 프로젝트에서 Repository

이번 프로젝트에서는 GitHub Repository를 ArgoCD에 등록하였다.

Repository 등록 이후 ArgoCD는 GitHub Repository를 지속적으로 감시하였으며 `k8s` 디렉터리에 저장된 Deployment와 Service Manifest를 Kubernetes Cluster와 자동으로 동기화하였다.

Repository는 GitOps 운영의 시작점이며 이후 생성한 Application이 Repository를 참조하여 Kubernetes Cluster를 관리하게 된다.

---

### Repository와 Application 차이

Repository와 Application은 서로 다른 역할을 수행한다.

| Repository | Application |
|------------|-------------|
| Git Source 등록 | Git Source를 Kubernetes와 연결 |
| Git Repository 정보 관리 | Cluster, Namespace, Path, Revision 관리 |
| Manifest 저장 위치 | 실제 배포 대상 정의 |
| GitOps Source | GitOps 실행 객체 |

---

### Repository 동작 과정

```text
GitHub Repository

↓

Manifest(YAML)

↓

Application

↓

Kubernetes
```

Repository는 Manifest를 저장하고,

Application은 해당 Manifest를 Kubernetes에 적용한다.

---

### 학습 포인트

- Repository는 Git Source를 의미한다.
- Repository는 Desired State를 저장한다.
- Repository만 등록한다고 Kubernetes가 자동으로 관리되지는 않는다.
- Application이 Repository를 참조하여 GitOps를 수행한다.

---

### 실무 TIP

실무에서는 개발, 테스트, 운영 환경마다 서로 다른 Repository를 운영하거나 하나의 Repository에서 Branch를 이용하여 환경을 분리하는 경우가 많다.

또한 Private Repository를 사용하는 경우 Personal Access Token(PAT), SSH Key, Repository Credential 등을 이용하여 인증을 구성한다.

---

### 운영 시 고려사항

Repository 접근 권한은 최소 권한 원칙(Principle of Least Privilege)에 따라 관리하는 것이 중요하다.

또한 운영 환경에서는 Branch Protection과 Code Review를 함께 적용하여 운영 Manifest가 임의로 변경되지 않도록 관리하는 것이 일반적이다.



## 8-9. Tracking Annotation이란?

### Tracking Annotation의 정의

Tracking Annotation은 ArgoCD가 Kubernetes Resource를 자신의 관리 대상으로 식별하기 위해 자동으로 추가하는 Annotation이다.

ArgoCD는 Git Repository의 Manifest와 Kubernetes Cluster의 Resource를 비교할 때 Tracking Annotation을 이용하여 자신이 관리하는 Resource인지 여부를 판단한다.

대표적으로 다음과 같은 Annotation이 추가된다.

```yaml
metadata:
  annotations:
    argocd.argoproj.io/tracking-id: ...
```

Tracking Annotation은 Kubernetes Resource의 Metadata에 저장되며 GitOps 운영을 위한 내부 식별자로 사용된다.

---

### Tracking Annotation을 사용하는 이유

Git Repository와 Kubernetes Cluster에는 동일한 이름의 Deployment나 Service가 존재할 수 있다.

그러나 Kubernetes Resource가 ArgoCD에 의해 생성된 것인지, 운영자가 직접 `kubectl apply`를 이용하여 생성한 것인지는 Kubernetes 자체에서는 구분할 수 없다.

ArgoCD는 Tracking Annotation을 이용하여 자신이 관리하는 Resource를 식별하고 Git Repository와 Kubernetes Cluster를 올바르게 비교한다.

이를 통해 GitOps 환경에서 Resource를 안정적으로 관리할 수 있다.

---

### 이번 프로젝트에서 Tracking Annotation

이번 프로젝트에서는 DAY2에서 `kubectl apply`를 이용하여 Deployment와 Service를 생성하였다.

이후 DAY4에서 ArgoCD Application을 생성하였을 때 기존 Resource에는 Tracking Annotation이 존재하지 않았다.

따라서 ArgoCD는 Git Repository와 Kubernetes Cluster가 서로 다르다고 판단하여 초기 상태에서 `OutOfSync`를 표시하였다.

이후 Manual Sync를 수행하면서 ArgoCD가 Tracking Annotation을 Resource에 추가하였고 Kubernetes Resource를 자신의 관리 대상으로 편입하였다.

---

### Tracking Annotation 동작 과정

```text
DAY2

kubectl apply

↓

Deployment 생성

↓

Tracking Annotation 없음

────────────────────────

DAY4

Application 생성

↓

OutOfSync

↓

Manual Sync

↓

Tracking Annotation 생성

↓

ArgoCD 관리 시작
```

---

### 이번 프로젝트에서 확인한 내용

Application 생성 직후 ArgoCD Dashboard의 Diff 화면을 확인한 결과 Tracking Annotation이 존재하지 않는 것이 초기 OutOfSync의 원인임을 확인하였다.

Manual Sync 이후에는 Tracking Annotation이 추가되면서 Application 상태가 `Healthy`, `Synced` 상태로 변경되었다.

이를 통해 ArgoCD가 기존 Kubernetes Resource를 자신의 관리 대상으로 편입하는 과정을 직접 확인하였다.

---

### 학습 포인트

- Tracking Annotation은 ArgoCD가 Resource를 식별하기 위한 Metadata이다.
- Kubernetes Resource가 ArgoCD 관리 대상인지 확인하는 기준이 된다.
- 기존 Resource에는 Tracking Annotation이 존재하지 않을 수 있다.
- 최초 Manual Sync 이후 Tracking Annotation이 추가된다.
- Initial OutOfSync는 정상적인 GitOps 동작 과정이다.

---

### 실무 TIP

운영 환경에서는 이미 운영 중인 Kubernetes Cluster를 ArgoCD로 전환(Migration)하는 경우가 많다.

이때 기존 Resource에는 Tracking Annotation이 존재하지 않으므로 최초 Sync 과정에서 OutOfSync가 발생하는 것이 일반적이다.

초기 Sync 이후에는 ArgoCD가 모든 Resource를 자신의 관리 대상으로 편입하게 된다.

---

### 운영 시 고려사항

Tracking Annotation은 ArgoCD 내부 관리에 사용되는 Metadata이므로 운영자가 직접 수정하거나 삭제하지 않는 것이 좋다.

Tracking Annotation이 손상되면 ArgoCD가 Resource를 정상적으로 식별하지 못하여 GitOps 동기화 과정에 문제가 발생할 수 있다.


## 8-10. Target Revision이란?

### Target Revision의 정의

Target Revision은 ArgoCD가 감시할 Git Repository의 Branch 또는 Tag를 의미한다.

ArgoCD는 Repository 전체를 감시하는 것이 아니라 Target Revision으로 지정된 Branch만 지속적으로 모니터링한다.

즉 Git Repository 안에서 어떤 Branch를 기준으로 Kubernetes Cluster를 운영할 것인지를 정의하는 GitOps의 핵심 설정이다.

---

### Target Revision을 사용하는 이유

하나의 Git Repository에는 여러 개의 Branch가 존재할 수 있다.

예를 들어 다음과 같은 Branch를 운영할 수 있다.

- main
- develop
- feature/day4-argocd
- release

ArgoCD는 이 모든 Branch를 동시에 감시하지 않는다.

Target Revision으로 지정한 하나의 Branch만 감시하며 해당 Branch의 Manifest만 Kubernetes Cluster에 반영한다.

---

### 이번 프로젝트에서 Target Revision

처음 Application을 생성할 때 Target Revision을 `main`으로 설정하였다.

그러나 실제 작업은 `feature/day4-argocd` Branch에서 진행하고 있었기 때문에 Deployment Manifest를 수정하고 Git Push를 수행해도 ArgoCD는 아무런 변경 사항을 감지하지 않았다.

처음에는 Auto Sync가 정상적으로 동작하지 않는 것으로 판단하였다.

하지만 원인을 분석한 결과 ArgoCD는 `main` Branch를 감시하고 있었으며 실제 변경 사항은 `feature/day4-argocd` Branch에 존재하였다.

Target Revision을 `feature/day4-argocd`로 변경한 이후 Git Push를 수행하자 ArgoCD가 즉시 OutOfSync 상태를 감지하였으며 이후 Auto Sync를 통해 Kubernetes Deployment와 Pod가 자동으로 변경되는 것을 확인하였다.

---

### Target Revision 동작 과정

초기 상태

```text
GitHub Repository

├── main
│      replicas: 2
│
└── feature/day4-argocd
       replicas: 3

↓

Target Revision

↓

main
```

ArgoCD는 main Branch만 감시하므로 feature Branch 변경 사항은 반영되지 않는다.

---

변경 후

```text
GitHub Repository

├── main
│
└── feature/day4-argocd

↓

Target Revision

↓

feature/day4-argocd
```

ArgoCD는 feature Branch를 감시하면서 Git 변경 사항을 자동으로 감지한다.

---

### 이번 프로젝트에서 확인한 내용

Target Revision을 변경한 이후 Deployment Manifest를 수정하여 Git Push를 수행하였다.

ArgoCD는 Git 변경 사항을 자동으로 감지하였으며 Application 상태가 OutOfSync가 된 이후 Auto Sync를 수행하여 Deployment와 Pod를 자동으로 변경하였다.

이를 통해 Target Revision이 GitOps 운영에서 매우 중요한 설정이라는 것을 확인하였다.

---

### 학습 포인트

- Target Revision은 ArgoCD가 감시할 Git Branch를 의미한다.
- ArgoCD는 Target Revision만 지속적으로 감시한다.
- 잘못된 Branch를 지정하면 Git 변경 사항을 감지하지 못한다.
- GitOps 운영에서는 Target Revision 관리가 매우 중요하다.

---

### 실무 TIP

실무에서는 환경별로 서로 다른 Target Revision을 사용하는 경우가 많다.

예를 들어

- Development → develop
- Staging → release
- Production → main

과 같이 Branch를 구분하여 운영한다.

이를 통해 동일한 Git Repository에서도 환경별 GitOps 운영이 가능하다.

---

### 운영 시 고려사항

Target Revision을 운영 Branch와 다르게 설정하면 Git 변경 사항이 Kubernetes Cluster에 반영되지 않을 수 있다.

운영 환경에서는 Branch 전략과 GitOps 정책을 함께 설계하여 Target Revision이 항상 올바른 Branch를 참조하도록 관리하는 것이 중요하다.


## 8-11. NodePort란?

### NodePort의 정의

NodePort는 Kubernetes Service의 한 종류로 Kubernetes Cluster 외부에서 Node의 특정 포트를 통해 Service에 접근할 수 있도록 제공하는 방식이다.

Kubernetes는 기본적으로 Pod를 외부에 직접 노출하지 않는다.

NodePort를 사용하면 Kubernetes Node에 특정 포트(기본적으로 30000~32767 범위)를 할당하여 외부 요청을 Kubernetes Service로 전달할 수 있다.

---

### NodePort를 사용하는 이유

Pod는 생성과 삭제가 반복되는 Kubernetes의 최소 실행 단위이므로 IP 주소가 언제든 변경될 수 있다.

따라서 Pod를 직접 외부에 노출하는 것은 적절하지 않다.

NodePort는 Service 앞단에서 고정된 접근 지점을 제공하므로 외부 사용자는 Pod의 IP 변경과 관계없이 동일한 방식으로 Kubernetes Service에 접근할 수 있다.

이번 프로젝트에서는 ArgoCD Dashboard를 외부에서 접근하기 위해 NodePort 방식을 적용하였다.

---

### NodePort 동작 과정

```text
Browser

↓

NodePort

↓

Service

↓

Pod
```

NodePort는 외부 요청을 Service로 전달하고 Service는 Label Selector를 이용하여 적절한 Pod로 트래픽을 전달한다.

---

### 이번 프로젝트에서 NodePort

ArgoCD 설치 이후 기본적으로 `argocd-server` Service는 ClusterIP 타입으로 생성되었다.

ClusterIP는 Kubernetes 내부에서만 접근할 수 있으므로 Dashboard를 외부 브라우저에서 사용할 수 없었다.

따라서 `argocd-server` Service를 NodePort 방식으로 변경하여 외부 접근이 가능한 환경을 구성하였다.

---

### 이번 프로젝트에서 확인한 내용

NodePort는 정상적으로 생성되었으며 Kubernetes 내부에서는 정상적으로 동작하는 것을 확인하였다.

그러나 Minikube(Docker Driver) 환경에서는 NodePort가 EC2 Public Interface에 직접 바인딩되지 않는 특성이 있어 외부 브라우저에서는 바로 접근할 수 없었다.

이후 `kubectl port-forward`를 이용하여 Dashboard 접근을 검증하였다.

---

### NodePort의 장점

- 외부에서 Kubernetes Service 접근 가능
- 별도의 LoadBalancer 없이 사용 가능
- 개발 및 테스트 환경에 적합
- Kubernetes 기본 기능으로 제공

---

### NodePort의 단점

- 고정 포트(30000~32767) 사용
- 운영 환경에서는 직접 사용하는 경우가 드물다.
- 클라우드 환경에서는 Security Group 등 네트워크 정책을 함께 구성해야 한다.

---

### 학습 포인트

- NodePort는 Kubernetes Service를 외부에 노출하는 방식이다.
- Pod가 아닌 Service를 외부에 공개한다.
- Kubernetes Node를 통해 외부 접근을 제공한다.
- 운영 환경에서는 Ingress 또는 LoadBalancer를 사용하는 경우가 많다.

---

### 실무 TIP

NodePort는 학습 및 테스트 환경에서는 많이 사용하지만 Production 환경에서는 Ingress Controller와 LoadBalancer를 함께 사용하는 것이 일반적이다.

특히 Amazon EKS에서는 AWS Load Balancer Controller(ALB Controller)를 이용하여 Ingress 기반으로 서비스를 운영하는 경우가 가장 많다.

---

### 운영 시 고려사항

NodePort를 생성하더라도 Kubernetes 내부 설정만으로 외부 접근이 가능한 것은 아니다.

AWS 환경에서는 Security Group, Network ACL, 방화벽 정책 등을 함께 구성해야 하며, Minikube(Docker Driver)와 같이 실행 환경에 따라 네트워크 동작 방식이 달라질 수 있다는 점을 고려해야 한다.


## 8-12. kubectl port-forward란?

### kubectl port-forward의 정의

`kubectl port-forward`는 Kubernetes Resource(Pod 또는 Service)의 포트를 Local 환경 또는 지정한 네트워크 인터페이스로 전달(Forward)하는 기능이다.

Kubernetes Cluster 내부에서 실행 중인 애플리케이션을 외부에 직접 노출하지 않고도 임시로 접근할 수 있도록 제공하는 Kubernetes CLI 기능이다.

주로 테스트, 장애 분석, 운영 지원과 같은 목적으로 사용된다.

---

### kubectl port-forward를 사용하는 이유

이번 프로젝트에서는 ArgoCD Server를 NodePort 방식으로 변경하고 AWS Security Group에서도 해당 포트를 허용하였다.

그러나 Minikube(Docker Driver) 환경에서는 NodePort가 EC2 Public Interface에 직접 바인딩되지 않는 특성 때문에 외부 브라우저에서 Dashboard에 접근할 수 없었다.

NodePort 자체에는 문제가 없었지만 실행 환경의 네트워크 구조 때문에 Dashboard 접근이 제한되었다.

이를 해결하기 위해 `kubectl port-forward`를 이용하여 EC2의 8080 포트와 ArgoCD Server를 연결하였다.

---

### 사용 명령어

```bash
kubectl port-forward -n argocd svc/argocd-server 8080:443 --address 0.0.0.0
```

---

### 명령어 설명

| 명령어 | 설명 |
|---------|------|
| `kubectl port-forward` | Kubernetes Resource와 Local Port 연결 |
| `-n argocd` | argocd Namespace 지정 |
| `svc/argocd-server` | argocd-server Service 선택 |
| `8080:443` | EC2의 8080 포트를 Service의 443 포트와 연결 |
| `--address 0.0.0.0` | 모든 네트워크 인터페이스에서 접근 허용 |

---

### 동작 과정

```text
Browser

↓

EC2:8080

↓

kubectl port-forward

↓

argocd-server Service

↓

ArgoCD Dashboard
```

---

### 이번 프로젝트에서 port-forward

NodePort를 통한 직접 접근이 실패한 이후 `kubectl port-forward`를 적용하였다.

이후 EC2의 8080 포트를 이용하여 ArgoCD Dashboard에 정상적으로 로그인하였으며 Git Repository 등록, Application 생성, Manual Sync, Auto Sync 등 GitOps 기능을 모두 검증하였다.

---

### NodePort와 port-forward 비교

| NodePort | kubectl port-forward |
|-----------|----------------------|
| Service를 외부에 노출 | Service와 Local Port를 임시 연결 |
| 장기간 운영 가능 | 테스트 및 검증 목적 |
| 운영 환경 일부 사용 | 운영 환경에서는 거의 사용하지 않음 |
| Kubernetes Networking 기능 | kubectl CLI 기능 |

---

### 학습 포인트

- `kubectl port-forward`는 Kubernetes Resource와 Local Port를 연결한다.
- NodePort가 불가능한 환경에서 Dashboard 접근을 검증할 수 있다.
- Pod뿐 아니라 Service도 Port Forward 대상이 될 수 있다.
- Port Forward는 임시 연결이므로 터미널을 종료하면 연결도 종료된다.

---

### 실무 TIP

운영 환경에서는 `kubectl port-forward`를 지속적인 서비스 공개 방식으로 사용하지 않는다.

주로 장애 분석, 로그 확인, 테스트, 임시 접근과 같은 운영 지원 목적으로 활용한다.

외부 서비스 공개는 Ingress Controller 또는 LoadBalancer를 이용하는 것이 일반적이다.

---

### 운영 시 고려사항

`kubectl port-forward`는 테스트와 검증을 위한 임시 연결 방식이다.

운영 환경에서는 Ingress, ALB, NLB 등을 이용한 네트워크 구성이 권장되며 `kubectl port-forward`를 서비스 운영 방식으로 사용하는 것은 적절하지 않다.

또한 Port Forward는 터미널 세션이 유지되는 동안에만 동작하므로 장기간 운영 환경에는 적합하지 않다.


## 8-13. GitOps 동작 원리

### GitOps 동작 원리

GitOps는 Git Repository를 기준으로 Kubernetes Cluster를 운영하는 방식이다.

운영자는 Kubernetes Cluster를 직접 수정하지 않고 Git Repository만 변경한다.

ArgoCD는 Git Repository를 지속적으로 감시(Polling)하면서 Git Repository의 Desired State와 Kubernetes Cluster의 Actual State를 비교한다.

두 상태가 서로 다르면 OutOfSync 상태를 표시하며 Manual Sync 또는 Auto Sync를 수행하여 Kubernetes Cluster를 Git Repository와 동일한 상태로 유지한다.

즉 Git Repository가 Kubernetes 운영의 기준이 된다.

---

### GitOps 전체 동작 과정

```text
Developer

↓

Deployment Manifest 수정

↓

Git Commit

↓

Git Push

↓

GitHub Repository

↓

ArgoCD Polling

↓

Desired State 변경 감지

↓

OutOfSync

↓

Sync

↓

Kubernetes API Server

↓

Deployment Update

↓

ReplicaSet Update

↓

Pod Update

↓

Healthy

↓

Synced
```

---

### 이번 프로젝트에서 GitOps 동작 과정

이번 프로젝트에서는 Deployment Manifest의 Replica 개수를 변경하였다.

기존

```yaml
replicas: 3
```

↓

변경

```yaml
replicas: 2
```

GitHub Repository에 Push를 수행하자 ArgoCD는 Target Revision(feature/day4-argocd)을 지속적으로 감시하고 있었기 때문에 변경 사항을 자동으로 감지하였다.

이후 Deployment를 수정하고 ReplicaSet을 갱신하였으며 기존 Pod를 종료하고 새로운 Replica 개수에 맞게 Pod를 재생성하였다.

최종적으로 Application 상태는 Healthy와 Synced 상태가 되었으며 Kubernetes Cluster는 Git Repository와 동일한 상태를 유지하였다.

---

### GitOps에서 ArgoCD 역할

ArgoCD는 Git Repository와 Kubernetes Cluster를 비교하는 GitOps Controller 역할을 수행한다.

주요 동작은 다음과 같다.

- Git Repository Polling
- Desired State와 Actual State 비교
- OutOfSync 감지
- Sync 수행
- Configuration Drift 복구(Self Heal)
- Git Repository 기준 상태 유지

즉 ArgoCD는 Git Repository를 기준으로 Kubernetes Cluster를 자동 운영하는 플랫폼이다.

---

### GitOps를 사용하는 이유

GitOps를 적용하면 Kubernetes를 직접 수정하지 않아도 된다.

모든 변경 사항은 Git Repository에서 관리되므로 변경 이력 관리, Code Review, Rollback, 협업 환경을 하나의 Git Workflow 안에서 수행할 수 있다.

또한 Git Repository가 항상 기준이 되므로 운영 환경의 일관성을 유지할 수 있다.

---

### 학습 포인트

- GitOps는 Git Repository를 기준으로 Kubernetes를 운영한다.
- ArgoCD는 Desired State와 Actual State를 지속적으로 비교한다.
- OutOfSync는 상태 차이를 의미한다.
- Sync 이후 Kubernetes는 Git Repository와 동일한 상태를 유지한다.
- GitHub Repository만 수정하면 Kubernetes가 자동으로 변경된다.

---

### 실무 TIP

최근 Kubernetes 운영 환경에서는 GitOps를 기본 운영 방식으로 채택하는 기업이 증가하고 있다.

특히 Amazon EKS, Azure AKS, Google GKE에서는 ArgoCD 또는 FluxCD를 이용하여 Git Repository를 기준으로 운영하는 사례가 많다.

---

### 운영 시 고려사항

GitOps를 운영할 때는 Git Repository가 운영 환경의 기준이 되므로 Branch 전략, Pull Request, Code Review, Branch Protection 등을 함께 적용하는 것이 중요하다.

또한 운영자가 Kubernetes Cluster를 직접 수정하지 않는 운영 정책을 함께 적용하여 Configuration Drift를 최소화하는 것이 좋다.



## 8-14. GitHub Actions와 ArgoCD 연계 구조

### GitHub Actions와 ArgoCD 관계

GitHub Actions와 ArgoCD는 모두 자동화를 수행하지만 역할은 서로 다르다.

GitHub Actions는 애플리케이션을 Build하고 Docker Image를 생성하는 CI(Continuous Integration)를 담당한다.

반면 ArgoCD는 Git Repository의 Kubernetes Manifest를 기준으로 Kubernetes Cluster를 자동으로 동기화하는 CD(Continuous Delivery)를 담당한다.

즉 두 플랫폼은 서로 경쟁하는 관계가 아니라 하나의 DevOps Pipeline을 구성하는 역할을 수행한다.

---

### 역할 비교

| GitHub Actions | ArgoCD |
|----------------|---------|
| Continuous Integration(CI) | Continuous Delivery(CD) |
| Docker Image Build | Kubernetes Deployment 관리 |
| Docker Hub Push | Git Repository 감시 |
| Build 자동화 | Sync 자동화 |
| Source Code 기준 | Kubernetes Manifest 기준 |

---

### 이번 프로젝트 전체 구조

```text
Developer

↓

Source Code 수정

↓

Git Commit

↓

Git Push

↓

GitHub Repository

↓

GitHub Actions

↓

Docker Image Build

↓

Docker Hub Push

↓

Kubernetes Manifest 변경

↓

ArgoCD Polling

↓

Desired State 변경 감지

↓

Auto Sync

↓

Deployment Update

↓

ReplicaSet Update

↓

Pod Update

↓

Healthy / Synced
```

---

### 이번 프로젝트에서 구현한 과정

DAY1에서는 Docker 기반 Flask 애플리케이션을 컨테이너 환경에서 실행하였다.

DAY2에서는 Kubernetes Cluster를 구축하고 Deployment와 Service를 이용하여 애플리케이션을 Kubernetes 환경으로 이전하였다.

DAY3에서는 GitHub Actions를 이용하여 Docker Image를 자동으로 Build하고 Docker Hub에 Push하는 CI 환경을 구축하였다.

DAY4에서는 ArgoCD를 이용하여 Git Repository를 지속적으로 감시하고 Git 변경 사항이 Kubernetes Deployment와 Pod에 자동으로 반영되는 GitOps 기반 Continuous Delivery 환경을 구축하였다.

이를 통해 Source Code 변경부터 Kubernetes Deployment까지 자동으로 연결되는 DevOps Pipeline을 완성하였다.

---

### CI와 CD 차이

#### CI (Continuous Integration)

```text
Developer

↓

Git Push

↓

GitHub Actions

↓

Docker Build

↓

Docker Hub
```

목적

- Build 자동화
- 테스트 자동화
- Image 생성

---

#### CD (Continuous Delivery)

```text
Git Repository

↓

ArgoCD

↓

Deployment

↓

ReplicaSet

↓

Pod
```

목적

- Kubernetes 자동 배포
- Desired State 유지
- GitOps 운영

---

### 이번 프로젝트에서 얻은 결과

이번 프로젝트를 통해 다음과 같은 DevOps Pipeline을 구축하였다.

- Docker 기반 컨테이너 환경 구축
- Kubernetes 기반 오케스트레이션
- GitHub Actions 기반 CI 자동화
- Docker Hub 기반 Image Registry 구성
- ArgoCD 기반 GitOps Continuous Delivery 구축
- Git Push만으로 Kubernetes 자동 동기화 검증

---

### 학습 포인트

- GitHub Actions와 ArgoCD는 서로 다른 역할을 수행한다.
- GitHub Actions는 CI를 담당한다.
- ArgoCD는 CD를 담당한다.
- Docker Hub는 CI와 CD를 연결하는 Image Registry 역할을 수행한다.
- GitHub Repository는 GitOps의 Single Source of Truth 역할을 수행한다.

---

### 실무 TIP

최근 DevOps 환경에서는 Jenkins 대신 GitHub Actions를 사용하는 사례가 증가하고 있으며, Kubernetes 배포는 ArgoCD 또는 FluxCD를 이용한 GitOps 방식이 빠르게 확산되고 있다.

특히 Amazon EKS 환경에서는 GitHub Actions와 ArgoCD를 함께 사용하는 구성이 가장 많이 사용되는 DevOps 아키텍처 중 하나이다.

---

### 운영 시 고려사항

CI와 CD는 서로 다른 책임을 가진다.

GitHub Actions는 Docker Image 생성까지 담당하고, Kubernetes 배포는 ArgoCD가 담당하도록 역할을 분리하는 것이 유지보수성과 운영 안정성 측면에서 유리하다.

또한 운영 환경에서는 Immutable Image 정책과 Branch Protection을 함께 적용하여 안전한 GitOps 운영 환경을 구축하는 것이 중요하다.


# 9. Problem Solving

DAY4에서는 GitOps 기반 Continuous Delivery 환경을 구축하는 과정에서 여러 가지 문제가 발생하였다.

특히 Minikube(Docker Driver)의 네트워크 구조와 ArgoCD의 GitOps 동작 방식을 이해하는 과정에서 다양한 문제를 경험하였으며, 각 문제를 직접 분석하고 해결하였다.

이번 장에서는 실제 프로젝트에서 발생한 문제와 해결 과정을 정리하였다.

---

## 9-1. NodePort를 통한 ArgoCD Dashboard 접근 실패

### 문제

ArgoCD Server를 NodePort 방식으로 변경하고 AWS Security Group에서도 해당 포트를 허용하였지만 EC2 Public IP를 이용한 Dashboard 접근이 실패하였다.

브라우저에서는 다음과 같은 오류가 발생하였다.

```text
ERR_CONNECTION_REFUSED
```

---

### 원인 분석

처음에는 AWS Security Group 설정 문제로 판단하였다.

그러나 NodePort 자체는 정상적으로 생성되어 있었으며 Kubernetes Service와 Endpoint에도 이상이 없었다.

추가 분석 결과 Minikube(Docker Driver)가 Kubernetes Node를 Docker Network 내부에서 실행하고 있었기 때문에 NodePort가 EC2 Public Interface에 직접 바인딩되지 않는 구조임을 확인하였다.

즉 Kubernetes Service에는 문제가 없었으며 실행 환경의 네트워크 구조가 원인이었다.

---

### 확인 과정

다음 명령을 이용하여 내부 동작을 검증하였다.

```bash
minikube ip

curl -k https://$(minikube ip):30965

minikube service argocd-server -n argocd --url
```

내부에서는 정상적으로 ArgoCD Dashboard가 응답하는 것을 확인하였다.

이를 통해 Kubernetes Service에는 문제가 없음을 확인하였다.

---

### 해결

`kubectl port-forward`를 이용하여 EC2의 8080 포트와 ArgoCD Service를 연결하였다.

```bash
kubectl port-forward -n argocd svc/argocd-server 8080:443 --address 0.0.0.0
```

이후 브라우저에서 정상적으로 ArgoCD Dashboard에 접속하였다.

---

### 배운 점

NodePort는 Kubernetes 내부 기능이며 클라우드 네트워크와는 별도로 동작한다.

Minikube(Docker Driver) 환경에서는 NodePort가 EC2 Public Interface에 직접 연결되지 않을 수 있으므로 실행 환경의 네트워크 구조를 먼저 이해하는 것이 중요하다는 것을 확인하였다.

---

## 9-2. Initial OutOfSync 발생

### 문제

Application 생성 직후 ArgoCD Dashboard에서는 다음과 같은 상태가 표시되었다.

```text
Healthy

OutOfSync
```

Deployment와 Service는 이미 정상적으로 실행되고 있었기 때문에 처음에는 Git Repository와 Kubernetes Manifest가 동일한데 왜 OutOfSync가 발생하는지 이해하기 어려웠다.

---

### 원인 분석

ArgoCD Diff 화면을 확인한 결과 기존 Kubernetes Resource에는 ArgoCD의 Tracking Annotation이 존재하지 않았다.

Deployment와 Service는 DAY2에서 `kubectl apply`를 이용하여 생성한 Resource였기 때문에 아직 ArgoCD가 관리 대상으로 인식하지 못하고 있었다.

---

### 확인 과정

ArgoCD Diff 화면을 확인하여 다음 Annotation이 존재하지 않는 것을 확인하였다.

```yaml
argocd.argoproj.io/tracking-id
```

---

### 해결

Manual Sync를 수행하여 기존 Kubernetes Resource를 ArgoCD 관리 대상으로 편입하였다.

Sync 완료 이후 Tracking Annotation이 자동으로 생성되었으며 Application 상태가 `Healthy`, `Synced`로 변경되었다.

---

### 배운 점

Initial OutOfSync는 오류가 아니라 기존 Kubernetes Resource를 ArgoCD 관리 대상으로 등록하는 정상적인 과정이라는 것을 이해하였다.

---

## 9-3. Auto Sync가 동작하지 않은 문제

### 문제

Deployment Manifest를 수정하고 Git Push를 수행하였지만 ArgoCD가 OutOfSync 상태로 변경되지 않았으며 Auto Sync도 수행되지 않았다.

처음에는 Auto Sync 설정이 정상적으로 적용되지 않은 것으로 판단하였다.

---

### 원인 분석

Application 설정을 확인한 결과 Target Revision이 `main` Branch를 감시하도록 구성되어 있었다.

반면 실제 작업은 `feature/day4-argocd` Branch에서 진행하고 있었기 때문에 ArgoCD는 Git 변경 사항을 감지하지 못하였다.

---

### 확인 과정

Application 설정에서 Target Revision을 확인한 결과 다음과 같이 설정되어 있었다.

```text
main
```

Git Push는 다음 Branch에서 수행하였다.

```text
feature/day4-argocd
```

---

### 해결

Target Revision을 `feature/day4-argocd`로 변경하였다.

이후 Git Push를 다시 수행하자 ArgoCD가 즉시 OutOfSync 상태를 감지하였으며 Auto Sync를 통해 Deployment와 Pod가 자동으로 변경되는 것을 확인하였다.

---

### 배운 점

ArgoCD는 Repository 전체를 감시하는 것이 아니라 Target Revision으로 지정된 Branch만 감시한다.

GitOps 운영에서는 Target Revision 관리가 매우 중요한 요소라는 것을 확인하였다.


# 10. DAY4 회고

DAY4에서는 ArgoCD를 이용하여 GitOps 기반 Continuous Delivery(CD) 환경을 구축하였다.

기존에는 Kubernetes Deployment를 직접 수정하거나 `kubectl apply` 명령을 이용하여 Kubernetes Cluster를 관리하였다.

이번에는 GitHub Repository를 Single Source of Truth로 사용하는 GitOps 운영 방식을 적용하여 Git Repository만 수정하면 ArgoCD가 Kubernetes Cluster를 자동으로 원하는 상태로 유지하는 환경을 구현하였다.

또한 Git Repository 연동, Kubernetes Application 생성, Manual Sync, Auto Sync를 모두 직접 검증하면서 GitOps의 동작 원리를 이해할 수 있었다.

특히 Deployment Manifest의 Replica 개수를 변경한 후 Git Push만으로 Kubernetes Deployment와 Pod가 자동으로 변경되는 과정을 확인함으로써 CI와 CD가 하나의 DevOps Pipeline으로 연결되는 구조를 직접 구축하였다.

이번 프로젝트를 통해 GitHub Actions는 CI를 담당하고 ArgoCD는 CD를 담당한다는 역할 분리를 명확하게 이해할 수 있었으며 GitOps 기반 Kubernetes 운영 방식의 장점을 직접 경험할 수 있었다.

---

## 잘된 점

- ArgoCD 기반 GitOps 환경을 성공적으로 구축하였다.
- Git Repository를 Single Source of Truth로 사용하는 운영 방식을 구현하였다.
- GitHub Repository와 Kubernetes Cluster를 정상적으로 연동하였다.
- Manual Sync와 Auto Sync를 모두 검증하였다.
- Git Push만으로 Deployment와 Pod가 자동 변경되는 GitOps 환경을 구축하였다.
- GitHub Actions(CI)와 ArgoCD(CD)를 하나의 DevOps Pipeline으로 연결하였다.

---

## 아쉬운 점

- Minikube(Docker Driver) 환경의 네트워크 구조를 처음 접하면서 NodePort 접근 문제를 해결하는 데 시간이 소요되었다.
- Target Revision을 main으로 설정하여 초기 Auto Sync 검증이 정상적으로 수행되지 않았다.
- Tracking Annotation의 역할을 처음에는 이해하지 못하여 Initial OutOfSync 원인을 분석하는 과정이 필요하였다.

---

## 개선할 점

- Amazon EKS 환경에서 ArgoCD를 구성하여 실제 운영 환경과 동일한 GitOps 구조를 구축한다.
- Ingress Controller와 AWS Load Balancer Controller를 이용하여 운영 환경과 동일한 접근 구조를 구성한다.
- Git Commit SHA 기반 Immutable Image Tag 전략을 적용하여 GitOps 배포 안정성을 향상시킨다.
- ApplicationSet을 이용하여 다중 Application 관리 환경을 구성한다.

---

## DAY4 핵심 성과

- ArgoCD 설치 완료
- Git Repository 연동 완료
- Kubernetes Application 생성 완료
- Manual Sync 검증 완료
- Auto Sync 검증 완료
- Git 변경 자동 감지 완료
- Kubernetes Deployment 자동 변경 완료
- Replica 자동 변경 검증 완료
- GitOps 기반 Continuous Delivery 구축 완료

---

## 이번 프로젝트에서 가장 크게 배운 점

GitOps는 단순히 Kubernetes를 자동으로 배포하는 기술이 아니라 Git Repository를 기준으로 Kubernetes Cluster 전체를 운영하는 방식이라는 것을 이해하였다.

또한 GitHub Actions를 이용한 CI와 ArgoCD를 이용한 CD를 하나의 파이프라인으로 연결하면서 DevOps와 GitOps가 실제 운영 환경에서 어떻게 결합되는지를 직접 구축하고 검증할 수 있었다.


# 11. DAY5 계획

DAY5에서는 Kubernetes 환경의 상태를 실시간으로 모니터링하기 위한 Monitoring 환경을 구축한다.

DAY4에서 구축한 GitOps 기반 Continuous Delivery 환경을 기반으로 Prometheus와 Grafana를 설치하고 Kubernetes Cluster의 CPU, Memory, Pod 상태 등을 시각적으로 확인할 수 있는 환경을 구성할 예정이다.

---

## DAY5 목표

- Prometheus 설치
- Grafana 설치
- Node Exporter 구성
- Metrics Server 구성
- Kubernetes Monitoring 구축
- Dashboard 구성
- Kubernetes Resource 모니터링
- Pod 및 Node 상태 시각화

---

## DAY5 산출물

- Prometheus 구축
- Grafana 구축
- Kubernetes Monitoring Dashboard
- Node Exporter 구성
- Metrics 수집 환경 구축
- README 업데이트
- Master Document v1.5 업데이트
- DAY5.md 작성

---

## DAY5에서 중점적으로 학습할 내용

- Prometheus Architecture
- Grafana Dashboard
- Prometheus Exporter
- Metrics Server
- Time Series Database(TSDB)
- Kubernetes Monitoring
- Alerting 구조

---

## DAY5 완료 목표

Kubernetes Cluster의 CPU, Memory, Node, Pod 상태를 실시간으로 수집하고 Grafana Dashboard를 이용하여 시각적으로 확인할 수 있는 Monitoring 환경을 구축한다.