# ECorp - Samba AD and GitLab-based Corporate Infrastructure Lab

A reference architecture showcasing a GitLab-based corporate infrastructure for development-oriented companies. This project is a conceptual model designed to:

1. Demonstrate the structural components of a modern developer environment, including AD/DC and integrated CI/CD.
2. Provide a modular foundation for experimenting with personal projects in a controlled setting.
3. Offer a sandbox for building and testing automated deployment workflows.

The project is organized into submodules covering core services, corporate add-ons, and example application environments to serve as a starting point for infrastructure experimentation.

_Important note_: This installer makes unusual modifications on the hosts system, deactivating docker network isolation, modify routes, so it is better to deploy in an LXC container or dind.

## Core infrastructure

The infrastructure wrapped around 3 core technology:

- samba _for_ Active Direcory Domain Controller functionalities
- gitlab _for_ code management and CI/CD
- dns _for_ dns server to serve custom DNS records and delegated zones

## TODO doc
- explain .env config, key points
- designed to be routed project
- useful if you delegate/forward ecorp.intra.net to the host machine in your home network
- `core` tag in CI/CD
- ECORP_ global vars
- 
