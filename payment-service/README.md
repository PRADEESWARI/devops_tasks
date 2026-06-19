# Exercise 19 – Helm Chart Engineering

## Overview

This project demonstrates the implementation of a reusable Helm chart for Kubernetes applications. The objective of this exercise is to build a production-ready Helm chart that supports multiple environments, configurable resources, ConfigMaps, Secrets, Ingress, and Horizontal Pod Autoscaling (HPA).

In modern DevOps environments, Kubernetes applications are rarely deployed using static YAML files. Maintaining separate deployment manifests for different environments such as Development, QA, and Production becomes difficult as the project grows. Helm solves this problem by acting as a package manager for Kubernetes, enabling reusable templates and environment-specific configurations.

The primary goal of this exercise is to understand how Helm simplifies Kubernetes deployments and how a single chart can be reused across multiple environments with different configurations.

---

# Objective

The objective of this exercise is to create a reusable Helm chart named **payment-service** that supports:

* Replica configuration
* Resource requests and limits
* ConfigMaps
* Secrets
* Ingress
* Horizontal Pod Autoscaler
* Environment-specific configurations (Dev, QA, Prod)

---

# Prerequisites

Before starting this exercise, the following tools must be installed on the system:

### Docker

Verify Docker installation:

```bash
docker --version
```

Example Output:

```bash
Docker version 29.2.1
```

---

### Kubernetes CLI

Verify kubectl installation:

```bash
kubectl version --client
```

Example Output:

```bash
Client Version: v1.34.1
```

---

### Helm

Verify Helm installation:

```bash
helm version
```

Example Output:

```bash
version.BuildInfo{Version:"v4.2.1"}
```

---

# Why Helm?

Without Helm, a Kubernetes application may require multiple YAML files such as:

```text
deployment.yaml
service.yaml
ingress.yaml
configmap.yaml
secret.yaml
hpa.yaml
```

Managing these files individually becomes difficult as applications grow.

Helm provides:

* Reusable templates
* Environment-specific values
* Version management
* Easier upgrades and rollbacks
* Simplified Kubernetes deployments

Helm follows the concept:

```text
Templates + Values = Kubernetes Manifests
```

---

# Project Creation

A new Helm chart was created using the following command:

```bash
helm create payment-service
```

Output:

```bash
Creating payment-service
```

This command automatically generated a Helm project structure.

---

# Project Structure

```text
payment-service/
│
├── Chart.yaml
├── values.yaml
├── dev-values.yaml
├── qa-values.yaml
├── prod-values.yaml
│
├── charts/
│
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    ├── hpa.yaml
    ├── serviceaccount.yaml
    ├── configmap.yaml
    ├── secret.yaml
    └── tests/
```

---

# Understanding Chart.yaml

The Chart.yaml file contains metadata about the Helm chart.

Example:

```yaml
apiVersion: v2
name: payment-service
description: Payment Service Helm Chart
type: application
version: 0.1.0
appVersion: "1.16.0"
```

### Purpose

* Defines chart name
* Defines chart version
* Defines application version
* Helps Helm manage chart releases

---

# Understanding values.yaml

The values.yaml file stores configurable values used by templates.

Example:

```yaml
replicaCount: 1

image:
  repository: nginx
  tag: latest
```

Instead of hardcoding values inside templates, Helm dynamically reads them from values.yaml.

This allows the same chart to be reused across multiple environments.

---

# Environment Configuration

To support multiple environments, three separate values files were created.

## Development Environment

File:

```text
dev-values.yaml
```

Configuration:

```yaml
replicaCount: 1

environment: dev

logLevel: debug

secret:
  dbPassword: dev123
  jwtSecret: devjwt

resources:
  requests:
    cpu: 100m
    memory: 128Mi

  limits:
    cpu: 200m
    memory: 256Mi
```

---

## QA Environment

File:

```text
qa-values.yaml
```

Configuration:

```yaml
replicaCount: 2

environment: qa

logLevel: info

secret:
  dbPassword: qa123
  jwtSecret: qajwt
```

---

## Production Environment

File:

```text
prod-values.yaml
```

Configuration:

```yaml
replicaCount: 3

environment: prod

logLevel: error

secret:
  dbPassword: prod123
  jwtSecret: prodjwt
```

---

# ConfigMap Implementation

A ConfigMap template was created to store application configuration.

File:

```text
templates/configmap.yaml
```

Configuration:

```yaml
apiVersion: v1
kind: ConfigMap

metadata:
  name: {{ .Release.Name }}-config

data:
  ENVIRONMENT: {{ .Values.environment | quote }}
  LOG_LEVEL: {{ .Values.logLevel | quote }}
```

### Purpose

ConfigMaps store non-sensitive application configuration such as:

* Environment name
* Logging level
* Feature flags
* Application URLs

Using ConfigMaps prevents hardcoding values inside application code.

---

# Secret Implementation

A Secret template was created to store sensitive data.

File:

```text
templates/secret.yaml
```

Configuration:

```yaml
apiVersion: v1
kind: Secret

metadata:
  name: {{ .Release.Name }}-secret

type: Opaque

data:
  DB_PASSWORD: {{ .Values.secret.dbPassword | b64enc }}
  JWT_SECRET: {{ .Values.secret.jwtSecret | b64enc }}
```

### Purpose

Secrets are used to store:

* Database passwords
* API keys
* JWT secrets
* Authentication tokens

### Important Note

Kubernetes Secrets are only Base64 encoded by default.

They are not encrypted unless etcd encryption or an external KMS solution is configured.

---

# Ingress Configuration

Ingress support was enabled to expose applications externally.

Configuration:

```yaml
ingress:
  enabled: true

  className: nginx

  hosts:
    - host: payment.local

      paths:
        - path: /
          pathType: Prefix
```

### Purpose

Ingress provides a single entry point for multiple applications.

Traffic Flow:

```text
Internet
    ↓
Ingress
    ↓
Service
    ↓
Pod
```

Benefits:

* Centralized routing
* SSL termination
* Reduced infrastructure cost
* Simplified application exposure

---

# Horizontal Pod Autoscaler (HPA)

Autoscaling was enabled to automatically scale application pods.

Configuration:

```yaml
autoscaling:
  enabled: true

  minReplicas: 2

  maxReplicas: 10

  targetCPUUtilizationPercentage: 70
```

### Purpose

Automatically adjusts pod count based on CPU utilization.

Example:

```text
CPU Usage 20% → 2 Pods

CPU Usage 70% → 5 Pods

CPU Usage 90% → 10 Pods
```

Benefits:

* Improved performance
* Cost optimization
* Better resource utilization

---

# Helm Validation

The chart was validated using Helm lint.

Command:

```bash
helm lint .
```

Purpose:

* Detect syntax issues
* Validate chart structure
* Verify templates

Expected Output:

```bash
1 chart(s) linted, 0 chart(s) failed
```

---

# Rendering Kubernetes Manifests

Helm templates were rendered without deploying.

Command:

```bash
helm template payment-service .
```

Purpose:

* Preview generated YAML
* Verify template rendering
* Debug configuration issues

---

# Environment-Specific Rendering

Development:

```bash
helm template payment-service . -f dev-values.yaml
```

QA:

```bash
helm template payment-service . -f qa-values.yaml
```

Production:

```bash
helm template payment-service . -f prod-values.yaml
```

Purpose:

* Validate environment configurations
* Verify replica counts
* Verify resource allocation
* Verify ConfigMaps and Secrets

---

# Issues Encountered

### Secret Template Error

Error:

```bash
nil pointer evaluating interface {}.dbPassword
```

Cause:

The chart expected secret values but they were not defined in values.yaml.

Solution:

Added default values:

```yaml
secret:
  dbPassword: ""
  jwtSecret: ""
```

This prevented Helm from failing when environment-specific values files were not supplied.

---

# Key Learnings

Throughout this exercise, the following concepts were learned:

* Helm Chart Creation
* Helm Templates
* values.yaml
* ConfigMaps
* Kubernetes Secrets
* Ingress
* Horizontal Pod Autoscaler
* Environment-specific Deployments
* Helm Debugging
* Helm Template Rendering

---

# Real-World Relevance

Helm is widely used in production Kubernetes environments.

Organizations use Helm to manage:

* Microservices
* Platform components
* Monitoring stacks
* CI/CD deployments
* Infrastructure applications

Examples:

* Prometheus
* Grafana
* ArgoCD
* NGINX Ingress Controller
* External Secrets Operator

Most production Kubernetes deployments use Helm because it improves consistency, reusability, and maintainability.

---

# Conclusion

This exercise successfully implemented a reusable Helm chart for the payment-service application. The chart supports multiple environments, configurable resources, ConfigMaps, Secrets, Ingress, and autoscaling. Validation and rendering were performed using Helm commands to ensure correct chart behavior.

The completed chart demonstrates industry-standard Helm practices and provides a strong foundation for future Kubernetes and GitOps-based deployments.
