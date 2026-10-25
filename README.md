# 🩺⚡ Self-Healing Infrastructure

> **Automated incident detection, alert routing, and self-healing infrastructure recovery with zero human intervention.**

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![NGINX](https://img.shields.io/badge/NGINX-009639?style=flat-square&logo=nginx&logoColor=white)](https://nginx.org/)
[![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white)](https://prometheus.io/)
[![Alertmanager](https://img.shields.io/badge/Alertmanager-FFA500?style=flat-square&logo=prometheus&logoColor=white)](https://prometheus.io/docs/alerting/latest/alertmanager/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Ansible](https://img.shields.io/badge/Ansible-EE0000?style=flat-square&logo=ansible&logoColor=white)](https://www.ansible.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)

---

## 📖 Overview

In modern cloud-native systems, downtime directly impacts user experience and revenue. **Self-Healing Infrastructure** is an end-to-end DevOps demonstration that watches over an NGINX web server, instantly identifies crashes or failed health checks, and autonomously triggers an Ansible playbook to resurrect the service and verify recovery.

## 🎯 Project objective
The objective is to build a system that automatically detects when a service fails, sends an alert, and attempts to recover the service without manual intervention.

In our project, NGINX is the service being monitored. When it stops responding, the system detects the failure and uses Ansible to restart its Docker container.


### 🔄 The Self-Healing Loop:
1. 🩺 **Monitor:** Blackbox Exporter continuously probes the NGINX HTTP endpoint.
2. 🚨 **Detect:** Prometheus evaluates scrape metrics against alert rules.
3. 📣 **Route:** Alertmanager groups notifications and fires a webhook payload.
4. ⚡ **Remediate:** Flask webhook receives the alert and kicks off an Ansible playbook.
5. 🛡️ **Verify & Log:** Ansible restarts the container, confirms HTTP 200, and logs the incident.

---

## 🏗️ Architecture & Workflow

```text
       ┌───────────────────────────┐
       │   🌐 NGINX Web Server     │ ◄──────────┐
       │  (Target Container: 8081) │            │
       └─────────────┬─────────────┘            │
                     │ HTTP Probe               │
                     ▼                          │
       ┌───────────────────────────┐            │
       │   🔍 Blackbox Exporter    │            │
       └─────────────┬─────────────┘            │
                     │ Scrapes                  │
                     ▼                          │
       ┌───────────────────────────┐            │
       │  📊 Prometheus + Rules    │            │
       └─────────────┬─────────────┘            │
                     │ Fires Alert              │
                     ▼                          │
       ┌───────────────────────────┐            │
       │   🔔 Alertmanager         │            │
       └─────────────┬─────────────┘            │
                     │ POST /webhook            │
                     ▼                          │
       ┌───────────────────────────┐            │
       │  🐍 Flask Webhook Engine  │            │
       │      (Host Machine)       │            │
       └─────────────┬─────────────┘            │
                     │ Triggers                 │
                     ▼                          │
       ┌───────────────────────────┐            │
       │   🤖 Ansible Playbook     │────────────┘
       │  (Docker Restart + Check) │  Auto-Restarts & Verifies
       └───────────────────────────┘
```

---

## 🧰 Technology Stack

| Layer | Tool | Purpose |
| :--- | :--- | :--- |
| **Workload** | ![NGINX](https://img.shields.io/badge/NGINX-009639?style=flat-square&logo=nginx&logoColor=white) | Production-grade web server serving traffic |
| **Probing** | ![Blackbox](https://img.shields.io/badge/Blackbox_Exporter-E6522C?style=flat-square&logo=prometheus&logoColor=white) | Out-of-band HTTP/HTTPS endpoint availability checker |
| **Monitoring** | ![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white) | Time-series metrics engine and alert evaluator |
| **Alerting** | ![Alertmanager](https://img.shields.io/badge/Alertmanager-FFA500?style=flat-square&logo=prometheus&logoColor=white) | Deduplication, grouping, and webhook dispatching |
| **Event Bridge** | ![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white) | Lightweight Python microservice handling incoming alerts |
| **Remediation** | ![Ansible](https://img.shields.io/badge/Ansible-EE0000?style=flat-square&logo=ansible&logoColor=white) | Infrastructure-as-Code automation and service recovery |
| **Orchestration** | ![Docker Compose](https://img.shields.io/badge/Docker_Compose-2496ED?style=flat-square&logo=docker&logoColor=white) | Unified local container networking and service management |

---

## 📁 Project Structure

```text
self-healing-infrastructure/
├── 🔔 alertmanager/
│   └── alertmanager.yml         # Alert routing & webhook definitions
├── 🤖 ansible/
│   └── recover_nginx.yml        # Recovery playbook & HTTP verification
├── 📝 logs/
│   └── recovery.log             # Audit trail of automated recovery runs
├── 📊 prometheus/
│   ├── blackbox.yml             # HTTP probe configuration
│   ├── prometheus.yml           # Scrape targets & Alertmanager config
│   └── rules/
│       └── alerts.yml           # NginxDown threshold rules
├── 🐍 webhook/
│   ├── app.py                   # Flask server receiving alerts & launching Ansible
│   └── Dockerfile               # Containerized webhook definition
├── 📄 .gitignore                # Ignore virtual environments, cache & logs
├── 🐳 docker-compose.yml        # Orchestrates Prometheus, Blackbox & Alertmanager
└── 📖 README.md                 # Project documentation
```

---

## 📋 Prerequisites

Before getting started, make sure you have the following installed:

- 🐳 [Docker Desktop](https://www.docker.com/products/docker-desktop/) (running)
- 🐍 [Python 3.10+](https://www.python.org/)
- 🤖 [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
- 🐙 [Git](https://git-scm.com/)

> 📌 **Assumption:** A target NGINX container named `nginx-service` is running locally with port `8081` mapped to container port `80`:
> ```bash
> docker run -d --name nginx-service -p 8081:80 nginx:alpine
> ```

---

## 🚀 Setup & Execution

### 1️⃣ Spin up the Monitoring Stack
Bring up Prometheus, Blackbox Exporter, and Alertmanager in detached mode:
```bash
docker compose up -d
```

### 2️⃣ Start the Flask Remediation Webhook
Launch the webhook listener on your host:
```bash
cd ~/self-healing-infrastructure
source .venv/bin/activate
python webhook/app.py
```
*The webhook engine will start listening for incident payloads on `http://localhost:5001`.*

### 3️⃣ Access Dashboards & Web UIs
Quickly open your monitoring portals:
- 📊 **Prometheus:** [http://localhost:9090](http://localhost:9090)
- 🔔 **Alertmanager:** [http://localhost:9093](http://localhost:9093)
- 🩺 **Flask Webhook Health:** [http://localhost:5001/health](http://localhost:5001/health)

---

## 🧪 Simulate Failure & Auto-Recovery

Test the self-healing pipeline by intentionally crashing the NGINX web server!

### Step 1: Kill the NGINX Container
```bash
docker stop nginx-service
```

### Step 2: Watch the Magic Happen ✨
1. 🔍 **Blackbox Exporter** detects probe failure (`probe_success == 0`).
2. 🚨 **Prometheus** triggers the `NginxDown` alert after the configured threshold.
3. 📣 **Alertmanager** receives the alert and posts a webhook to Flask (`http://host.docker.internal:5001/webhook`).
4. 🤖 **Flask** triggers `ansible/recover_nginx.yml`.
5. 🔄 **Ansible** restarts the `nginx-service` container and verifies HTTP response 200.

### Step 3: Verify Restoration
Confirm that the container has been brought back to life:
```bash
docker ps --filter name=nginx-service
```

Test the live endpoint:
```bash
curl -I http://localhost:8081
```
*You should receive an **`HTTP/1.1 200 OK`** response!* 🎯

---

## 🌟 Key Features

- 🎯 **Blackbox Synthetic Probing:** Active external health checks verifying true application availability.
- ⏱️ **Rapid Detection:** Automated alerting thresholds for immediate fault identification.
- 🔄 **Autonomous Self-Healing:** Seamless bridge between Prometheus alerts and Ansible playbooks.
- 🔒 **Duplicate Alert Protection:** Built-in safeguards to prevent redundant concurrent recovery attempts.
- 📜 **Full Audit Logging:** Detailed records in `logs/recovery.log` tracking downtime and remediation actions.
- ✅ **Post-Remediation Verification:** End-to-end check guaranteeing the service is actually answering requests.

---

## ⚠️ Limitations & Considerations

- 🧪 **Development Focus:** Built as an educational project for local sandbox experimentation.
- 💻 **Host-Bound Webhook:** Flask webhook executes directly on the host to manage local Docker sockets and Ansible execution.
- 🧠 **In-Memory State:** Dedup state is tracked in application memory and resets if Flask restarts.
- 🔁 **Alertmanager Resolution:** Configured with `send_resolved: false` to highlight incident-driven triggers.
- 🛡️ **Production Readiness:** Enterprise environments should include mTLS, HMAC payload signatures, and secret management.

---

## 🎓 Learning Outcomes

- 📈 Instrumenting infrastructure health checks with Prometheus and Blackbox Exporter.
- 🚨 Configuring alerting rules and notification pipelines in Alertmanager.
- 🔗 Building event-driven automation bridges using Python & Flask.
- 🤖 Writing idempotent Ansible playbooks for automated service remediation.
- 🐳 Managing interconnected monitoring ecosystems with Docker Compose.

---

- 📈 Instrumenting infrastructure health checks with Prometheus and Blackbox Exporter.
- 🚨 Configuring alerting rules and notification pipelines in Alertmanager.
- 🔗 Building event-driven automation bridges using Python & Flask.
- 🤖 Writing idempotent Ansible playbooks for automated service remediation.
- 🐳 Managing interconnected monitoring ecosystems with Docker Compose.

---



