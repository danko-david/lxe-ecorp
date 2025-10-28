
# A Mock corporate infrastructure model for developer company

_Important notes_: This installer makes unusual modifications on the hosts system, deactivating docker network isolation, modify routes, so better to deploy in an LXC container or dind.

## Core components
- dns _for_ dns server for name resolution
- samba _for_ AD functionalities
- samba _for_ fileshare
- gitlab _for_ code management and CI/CD
- redmine _for_ ticketing 
- nexus _for_ package management and external package mirroring
- squid _for_ external resource mirroring
- squid _for_ separation and filtering for user workstations
- nextcloud/mattermost _for_ teams and sharepoint alternative

## Networking model

Environment CIRD: 172.30/16
    Core components zone: 172.30.0/24
    Admin workstation zone: 172.30.1/24
    User workstation zone: 172.30.2/24


## Other network spaces



