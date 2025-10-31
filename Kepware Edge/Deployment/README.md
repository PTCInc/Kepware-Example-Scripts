# Deploying Kepware Edge: Examples for Docker-like and Kubernetes Environments

## Purpose

- Provide example files and guidance to deploy Kepware Edge in containerized environments:
    - Docker-like runtimes (Docker, Rancher, Podman, etc with Docker Compose capabilities)
    - Kubernetes (manifests)

## Contents

- Example docker compose files for running a single Kepware Edge container instance
- Example Kubernetes manifests for running a single Kepware Edge container instance (Service, PersistentVolumeClaim, Pod)

## To use

- Review the examples in this folder and choose the example for the target platform (docker-compose, k8s).
- Update configuration values that are wrapped in <> such as:
    - Image name / tag
    - Persistent storage paths and volume claims
    - Environment variables (if necessary) (admin credentials, load example project)
- Update other network configuration as needed. The default assumes a simple bridged type deployment with ports beign allocated by the container runtime / orchestrator host.
- For Docker-like usage:
    - Start the container with docker-compose up after editing the compose file.
- For Kubernetes usage:
    - Apply manifests with kubectl apply -f k8s/

## Requirements

- Valid Kepware Edge license and Kepware Edge License Server
- Container runtime (Docker/Podman) or a Kubernetes cluster
- Persistent storage for configuration and data
- Network access for data and configuration endpoints and any downstream devices or PLCs

## Notes

- Examples are intentionally minimal and intended as starting points — adapt them for production security, observability, and HA.
- Enable and insecure connections to Kepware Configuration API only as required; restrict access via network policies, firewall rules, or service mesh.

## References

- Documentation for Kepware Edge product information and manuals can be found [HERE](https://www.ptc.com/en/support/help/Kepware).
