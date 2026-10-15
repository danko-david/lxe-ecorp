---
id: TASK-2
title: A user disabled in the domain is blocked in GitLab
status: To Do
assignee: []
created_date: '2026-10-15 00:10'
labels:
  - to-test
dependencies: []
priority: medium
ordinal: 2000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Since 1.2.0 GitLab treats the domain controller as an Active Directory (active_directory true), which is meant to make it notice accounts disabled in the domain. tests/install only signs in an enabled domain user (domain_user_can_log_in_to_gitlab), so this behaviour is untested.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 An install test disables a domain user with samba-tool and shows that GitLab refuses or blocks it
<!-- AC:END -->
