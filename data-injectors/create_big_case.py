#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author : Nabil Adouani (github:nadouani)

import argparse
import requests
import uuid
import time
import json
import random


def create_tasks(thehive_url, api_key, organisation, case_id, items):
    headers = {
        "Authorization": "Bearer {}".format(api_key),
        "Content-Type": "application/json",
        "X-Organisation": organisation
    }

    for i in range(int(items)):
        random_text = str(uuid.uuid4())[0:6]
        data = {
            "status": "Waiting",
            "group": "default",
            "title": "Task {}".format(random_text)
        }

        response = requests.post(
            '{}/api/case/{}/task'.format(thehive_url, case_id),
            headers=headers,
            json=data)

        if response.status_code == 201:
            print(
                "#{} - Task {} created".format(response.json()["_id"], i))
        elif response.status_code != 200:
            raise Exception("{} : {}".format(
                response.status_code, response.text))


def create_obeservables(thehive_url, api_key, organisation, case_id, items):
    headers = {
        "Authorization": "Bearer {}".format(api_key),
        "Content-Type": "application/json",
        "X-Organisation": organisation
    }

    for i in range(int(items)):
        random_text = str(uuid.uuid4())[0:6]
        data = {
            "dataType": "other",
            "ioc": random.choice([True, False]),
            "sighted": random.choice([True, False]),
            "ignoreSimilarity": random.choice([True, False]),
            "tlp": random.choice([0, 1, 2, 3]),
            "message": "",
            "tags": ["sample"],
            "data": [random_text]
        }

        response = requests.post(
            '{}/api/case/{}/artifact'.format(thehive_url, case_id),
            headers=headers,
            json=data)

        if response.status_code == 201:
            print(
                "#{} - Observable created".format(i))
        elif response.status_code != 200:
            raise Exception("{} : {}".format(
                response.status_code, response.text))


def create_cases(thehive_url, api_key, organisation, items, tasks, artifacts):

    headers = {
        "Authorization": "Bearer {}".format(api_key),
        "Content-Type": "application/json",
        "X-Organisation": organisation
    }

    for i in range(int(items)):
        random_text = str(uuid.uuid4())

        data = {
            "title": "Case {}".format(random_text),
            "description": "N/A",
            "tags": ["sample"],
            "startDate": int(time.time())*1000,
            "tlp": random.choice([0, 1, 2, 3]),
            "pap": random.choice([0, 1, 2, 3]),
            "severity": random.choice([1, 2, 3, 4]),
        }

        response = requests.post(
            '{}/api/case'.format(thehive_url),
            headers=headers,
            json=data)

        if response.status_code == 201:
            print("#{} - Case {} created".format(response.json()["_id"], i))

            create_tasks(thehive_url, api_key,
                         organisation, response.json()["_id"], tasks)

            create_obeservables(thehive_url, api_key,
                                organisation, response.json()["_id"], artifacts)
        elif response.status_code != 200:
            raise Exception("{} : {}".format(
                response.status_code, response.text))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--key",
                        help=("API key"), required=True)
    parser.add_argument("-u", "--url",
                        help=("TheHive server url."), required=True)
    parser.add_argument("-o", "--organisation",
                        help=("Organisation name."), required=True)
    parser.add_argument("-i", "--items",
                        help=("Number of cases."), required=True)
    parser.add_argument("-t", "--tasks",
                        help=("Number of tasks."), required=True)
    parser.add_argument("-a", "--artifacts",
                        help=("Number of observables."), required=True)
    return parser.parse_args()

  def main():
    args = parse_args()
    print("Submitting config to  {}".format(args.url))
    create_cases(args.url, args.key, args.organisation,
                 args.items, args.tasks, args.artifacts)


if __name__ == "__main__":
    main()
