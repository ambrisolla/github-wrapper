# github-wrapper
Script to list jobs for all Github Actions workflows. 

## Usage
Export Github PAT:
```bash
$ export GH_PAT='your_GitHub_PAT'

```
Execute the following command:

```bash
$ ./github-wrapper.py -r prometheus/prometheus -a get_jobs | jq
```
Output:
```json
{
  "job_count": 22,
  "jobs": [
    "Fuzzing",
    "action",
    "analyze",
    "benchmark_cancel",
    "benchmark_restart",
    "benchmark_start",
    "buf",
    "build",
    "build_all",
    "codeql",
    "fuzzing",
    "golangci",
    "publish_main",
    "publish_release",
    "publish_ui_release",
    "repo_sync",
    "run_funcbench",
    "test_go",
    "test_golang_oldest",
    "test_mixins",
    "test_ui",
    "test_windows"
  ]
}

```


# Options
```bash
usage: github-wrapper.py [-h] -r REPOSITORY [-a {get_jobs}]

Github wrapper to collect Workflows informations.

options:
  -h, --help            show this help message and exit
  -r REPOSITORY, --repository REPOSITORY
                        Github repository format: owner/repository
  -a {get_jobs}, --action {get_jobs}
                        Action to perform.
```

