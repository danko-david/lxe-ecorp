---
id: TASK-5
title: Publish the diorama to the real registry
status: To Do
assignee: []
created_date: '2026-10-15 00:10'
labels:
  - to-test
dependencies: []
priority: medium
ordinal: 5000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
ci_ensure_diorama and ci_weekly_diorama are only tested against tests/fake/docker. The first push of master with the CI variables set (REPO=lxeu/, DOCKER_REGISTRY_USERNAME, DOCKER_REGISTRY_PASSWORD) is the real test.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 lxeu/ecorp-diorama:<version> and latest are on Docker Hub after a pipeline on master
- [ ] #2 A scheduled pipeline published <version>-<year>w<week>
<!-- AC:END -->
