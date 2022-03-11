# Jira Release Notes

## Description:

Easily get Jira release notes from the comfort zone of your CLI! :)

`ydemetriades/jira-release-notes` docker image enables you to fetch Jira Release Notes.
You can find it at [DockerHub](https://hub.docker.com/repository/docker/ydemetriades/ydemetriades/jira-release-notes).

## Runtime & Tags

`ydemetriades/jira-release-notes` is available both for Linux and Windows.

### Linux

|Tag|Version|Pull|
|:-:|:-----:|----|
|__v1.0__|__v1.0__|`ydemetriades/jira-release-notes:v1.0`|

_Note_: `latest` tag points to `v2.0`

### Windows

`ydemetriades/jira-release-notes` on Windows is available only for `1809`

|Tag|Version|Pull|
|:-:|:-----:|----|
|__v1.0-win1809__|__v1.0__|`ydemetriades/jira-release-notes:v1.0-win1809`|

Note: `latest-win1809` tag points to `v2.0-win1809`

## Parameters

All parameters are passed as executable arguments or by environment variables.
Always accessible by `jira-release-notes.py -h` :)

|Parameter|Environment Variable|Required|Description|Default Value|Available Options|Example|
|:--:|:------:|:------:|-----------|:-------------:|:-----------------:|-------|
|`--version VERSION`, `-v`|`JIRA_VERSION_NAME`|Yes|The unique name of the version|-|-|-v v1.0|
|`--project PROJECTID`, `-p`|`JIRA_PROJ`|Yes|The ID of the project to which this version is attached|-|-|-p 10000|
|`--user USER`, `-u`|`JIRA_AUTH_USER`|Yes|The Jira authentication user [email]|-|-|-u user|
|`--password PASSWORD`|`JIRA_AUTH_PASSWORD`|Yes|Jira API Authorization Password / API Token|-|-|--password 12345|
|`--url URL`|`JIRA_URL`|No|Jira Url|https://jira.org|-|--url https://jira.mydomain.com|
|`--api-version API_VERSION`|`JIRA_API_VERSION`|No|Jira API Version|__3__|[2, 3]|--api-version 3|
|`--format FORMAT`|`JIRA_RELEASE_NOTES_OUTPUT_FORMAT`|No|The Jira Release Notes Output format|text|[`text`, `markdown`, `html`]|-|
|`--skip-output-intro`|`JIRA_RELEASE_NOTES_OUTPUT_SKIP_INTRO`|No|Flag: Skip Output Intro [Version + Issues Count]|false|-|-|
|`--skip-output-version-name`|`JIRA_RELEASE_NOTES_OUTPUT_SKIP_INTRO_VERSION_NAME`|No|Flag: Skip Version name in Output Intro|false|-|-|
|`--skip-output--issues-count`|`JIRA_RELEASE_NOTES_OUTPUT_SKIP_INTRO_ISSUES_COUNT`|No|Flag: Skip Issues count in Output Intro|false|-|-|
|`--skip-output-issue-type-title`|`JIRA_RELEASE_NOTES_OUTPUT_SKIP_ISSUE_TYPE_TITLE`|No|Flag: Skip Issue type title in Output|false|-|-|
|`--skip-output-newline-between-issue-types`|`JIRA_RELEASE_NOTES_OUTPUT_SKIP_NEWLINE_BETWEEN_ISSUE_TYPES`|No|Flag: Skip new-line break between Issue types in Output|false|-|-|


## Notes

1. Enable Jira Api from Administration Settings
2. User __JIRA_AUTH_USER__ must be an Administrator for __JIRA_PROJ__ project

## Examples

### CLI Examples

```bash
jira-release-notes.py -v v1.0.0 -p 10000 -u youremail@example.com --password 'YOUR_API_TOKEN'
```

```bash
jira-release-notes.py \
    -v v1.0.0 \
    -p 10000 \
    -u youremail@example.com \
    --password 'YOUR_API_TOKEN' \
    --format markdown
    --skip-output-intro 
```

### Docker Examples

```
docker run -d --rm \ 
-e JIRA_VERSION_NAME=v1.0 \
-e JIRA_PROJ=TES \
-e JIRA_AUTH_USER=user \
-e JIRA_AUTH_PASSWORD=password \
ydemetriades/jira-release-notes
```

## Maintainers

[Yiannis Demetriades](https://github.com/ydemetriades)
