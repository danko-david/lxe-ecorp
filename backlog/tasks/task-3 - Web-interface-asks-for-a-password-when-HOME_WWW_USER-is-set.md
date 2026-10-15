---
id: TASK-3
title: Web interface asks for a password when HOME_WWW_USER is set
status: To Do
assignee: []
created_date: '2026-10-15 00:10'
labels:
  - to-test
dependencies: []
priority: medium
ordinal: 3000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Since 1.2.0 HOME_WWW_USER and HOME_WWW_PASSWORD reach the controller and protect the management web interface. tests/install runs with them unset, so the protected case is untested.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 An install test (or a test run with the variables set) shows the interface answers 401 without and 200 with the credentials
<!-- AC:END -->
