# TODOS

Keep this project minimal and outsource components to module projects that can be deployed separatly.

## TODOS
- spawn default files
- SSL cerfiticate for: AD, gitlab, gitlab registry (self signed and let's encrypt mirage)
- update global gitlab variables
    - DNS_CORE_ZONE_NAME as set in .env
    - ECORP_CORE_NETWORK_BRIDGE def: ecorp_core
    - ECORP_SSH_EXTRA_AUTH

- import git repos
- runner config, volumes, [runners.docker] pull_policy = "if-not-present"

- test mattermost, integrate to gitlab if it is good for this purpose

### TODO controller page
- show main information from .env
- run, observe, see last log of ansible provisioning
- dump CA if self signed is the option
- create documentation page like in homestack

### To test
Test from zero:
- open web vscode editor
- is gitlab's docker registry available?

## Additional components
- samba _for_ fileshare
- redmine _for_ ticketing 
- nexus _for_ package management and external package mirroring
- squid _for_ external resource mirroring
- squid _for_ separation and filtering for user workstations
- nextcloud/mattermost _for_ teams and sharepoint alternative


