# TODOS

Keep this project minimal and outsource components to module projects that can be deployed separatly.

- update global gitlab variables
    - DNS_CORE_ZONE_NAME as set in .env
    - ECORP_CORE_NETWORK_BRIDGE def: ecorp_core
    - ECORP_SSH_EXTRA_AUTH

- import git repos
- runner config, volumes, [runners.docker] pull_policy = "if-not-present"

### TODO controller page
- run, observe, see last log of ansible provisioning
- dump CA if self signed is the option

### To test
Test from zero:
- open web vscode editor
