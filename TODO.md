# TODOS

Keep this project minimal and outsource components to module projects that can be deployed separatly.
- runner config, volumes, dns, [runners.docker] pull_policy = "if-not-present"

### To test
Test from zero:
- open web vscode editor
- log in to GitLab as a domain user, and to the web interface with `HOME_WWW_USER` set: neither is covered by `tests/install`.
- `ci_ensure_diorama` and `ci_weekly_diorama` against the real registry: only tested with the fake docker.

### To set up
- CI/CD variables of the project for publishing: `REPO=lxeu/`, `DOCKER_REGISTRY_USERNAME`, `DOCKER_REGISTRY_PASSWORD`.
- A weekly pipeline schedule on `master` in GitLab for `ci_weekly_diorama`.

### Known problems
- `DC_REALM=ecorp` and `DC_DOMAIN=ecorp.intra` look swapped compared to what Samba calls them (realm is the DNS-style name, domain/workgroup the short one). With `ECORP_DNS_CORE_ZONE_NAME=e-corp.intra.net` there are three different names for one thing: the DC's hostname is `dc.ecorp.intra`, GitLab reaches it as `dc.e-corp.intra.net`.
- GitLab talks to the domain controller with `active_directory` set to `false`. Logging in works either way; with `true` GitLab would also notice accounts disabled in the domain. Not changed because it is untested.
- The week tag of the diorama (`<version>-w<week>`) has no year: if a version lives longer than a year, the tag of the same week is overwritten.
