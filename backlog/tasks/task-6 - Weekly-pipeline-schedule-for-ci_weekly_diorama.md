---
id: TASK-6
title: Weekly pipeline schedule for ci_weekly_diorama
status: To Do
assignee: []
created_date: '2026-10-15 00:10'
labels:
  - to-set-up
dependencies: []
priority: medium
ordinal: 6000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The weekly-diorama job only runs in scheduled pipelines on master. The schedule has to be created by hand in GitLab (CI/CD > Schedules). Recommended: Monday early morning, after GitLab's Wednesday patch and Thursday releases and Debian's Saturday point releases had a few days to settle.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A pipeline schedule on master exists in GitLab and its first run succeeded
<!-- AC:END -->
