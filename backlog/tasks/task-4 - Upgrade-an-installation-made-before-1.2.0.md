---
id: TASK-4
title: Upgrade an installation made before 1.2.0
status: To Do
assignee: []
created_date: '2026-10-15 00:10'
labels:
  - to-test
dependencies: []
priority: high
ordinal: 4000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Installations made before 1.2.0 keep DC_REALM and DC_DOMAIN in .env; they still win over the names derived from ECORP_DNS_CORE_ZONE_NAME. GitLab now binds as CN=Administrator,CN=Users,DC=ecorp instead of Administrator@<DC_DOMAIN>, the root token is regenerated, SSH into the controller becomes key-only. None of this was tried on a real upgrade.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 An installation of 1.1.0 upgraded to the current version still provisions, and domain users can still sign in to GitLab
<!-- AC:END -->
