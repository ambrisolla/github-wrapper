#!/usr/bin/env python

# Name: github-wrapper.py
# Description: this script is used to list all jobs in Github Actions Workflows
# Version: 1.0
# Author: André Brisolla / https://github.com/ambrisolla
# Date: 2023-09-01
# Usage: github-wrapper.py [-h] -r REPOSITORY [-a {get_jobs}]
# Python packages: PyYAML, requests

import os
import sys
import yaml
import json
import requests
from argparse import ArgumentParser


class GHWrapper:

    def __init__(self):
        self.pat = os.environ.get('GH_PAT') 
        self.headers = {
            'Authorization': f'token {self.pat}',
            'Accept': 'application/vnd.github.v3+json'}

    def get_default_branch(self):
        url = f'https://api.github.com/repos/{self.repository}'
        req = requests.get(url, headers=self.headers)
        res = req.json()
        return res.get('default_branch', None)

    def get_jobs(self):
        try:
            url = (f'https://api.github.com/repos/{self.repository}'
                   f'/actions/workflows')
            req = requests.get(url, headers=self.headers)
            if req.status_code == 200:
                res = req.json()
                default_branch = self.get_default_branch()
                paths = [x.get("path") for x in res.get('workflows')]
                urls = [f'https://raw.githubusercontent.com/{self.repository}/{default_branch}/{x}'
                        for x in paths]
                self.get_job_name(urls)
            else:
                print(req.text)
        except Exception as err:
            print(json.dumps({
                'error': str(err)}))

    def get_job_name(self, urls):
        try:
            jobs = []
            for url in urls:
                req = requests.get(url, headers=self.headers)
                if req.status_code == 200:
                    gh_workflow_data = req.text
                    yaml_data = yaml.safe_load(gh_workflow_data)
                    jobs.append(list(yaml_data['jobs'].keys()))
                else:
                    # some error, maybe some workflows files couldn't exist ?!
                    pass
            job_list = sorted(
                list(set([item for subitems in jobs for item in subitems])))
            print(json.dumps({
                'job_count': len(job_list),
                'jobs': job_list
            }))
        except Exception as err:
            return {
                'error': str(err)}


if __name__ == '__main__':
    parser = ArgumentParser(
        description="Github wrapper to collect Workflows informations.")
    parser.add_argument(
        "-r", "--repository",
        help="Github repository format: owner/repository",
        required=True)
    parser.add_argument(
        "-a", "--action",
        help="Action to perform.",
        choices=['get_jobs'])
    args = vars(parser.parse_args())
    if args.get('action') == None:
        print('error: no action specified')
        parser.print_help()
        sys.exit(1)
    else:
        action = args.get('action')
        repository = args.get('repository')
        ghw = GHWrapper()
        ghw.repository = repository
        eval(f'ghw.{action}()')