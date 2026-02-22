# ECorp - AD and Gitlab based developer corporate infrastructure model

_Important note_: This installer makes unusual modifications on the hosts system, deactivating docker network isolation, modify routes, so it is better to deploy in an LXC container or dind.

This project is aims to showcase a infrastructure of a development oriented company, implement a foundation to operate personal projects and leave room to create experimenting environments for the actual projects inside gitlab in full CI/CD manner.

## Core infrastructure

The infrastructure wrapped around 3 core technology:

- samba _for_ Active Direcory Domain Controller functionalities
- gitlab _for_ code management and CI/CD
- dns _for_ dns server to serve custom DNS records and delegated zones

## TODO doc
- explain .env config, key points
- designed to be routed project
- useful if you delegate ecorp.intra.net to the host machine in your home network
- `core` tag in CI/CD
