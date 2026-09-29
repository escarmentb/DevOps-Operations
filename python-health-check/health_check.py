#!/usr/bin/env python3

import json
import sys
import time
import urllib.error
import urllib.request

CONFIG_FILE = "services.json"
TIMEOUT_SECONDS = 5


def check_service(service):
    name = service["name"]
    url = service["url"]
    started_at = time.perf_counter()

    try:
        with urllib.request.urlopen(
            url,
            timeout=TIMEOUT_SECONDS
        ) as response:
            duration_ms = round(
                (time.perf_counter() - started_at) * 1000,
                2
            )

            return {
                "name": name,
                "url": url,
                "healthy": 200 <= response.status < 400,
                "status_code": response.status,
                "response_time_ms": duration_ms,
                "error": None
            }

    except urllib.error.HTTPError as error:
        return {
            "name": name,
            "url": url,
            "healthy": False,
            "status_code": error.code,
            "response_time_ms": None,
            "error": f"HTTP error: {error.reason}"
        }

    except urllib.error.URLError as error:
        return {
            "name": name,
            "url": url,
            "healthy": False,
            "status_code": None,
            "response_time_ms": None,
            "error": f"Connection error: {error.reason}"
        }


def main():
    try:
        with open(CONFIG_FILE, encoding="utf-8") as file:
            configuration = json.load(file)
    except FileNotFoundError:
        print(f"Configuration file not found: {CONFIG_FILE}")
        return 2
    except json.JSONDecodeError as error:
        print(f"Invalid JSON configuration: {error}")
        return 2

    results = []

    for service in configuration["services"]:
        result = check_service(service)
        results.append(result)

        if result["healthy"]:
            print(
                f'HEALTHY: {result["name"]} '
                f'HTTP {result["status_code"]} '
                f'in {result["response_time_ms"]} ms'
            )
        else:
            print(
                f'UNHEALTHY: {result["name"]} '
                f'{result["error"]}'
            )

    with open("health-results.json", "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)

    unhealthy_count = sum(
        1 for result in results if not result["healthy"]
    )

    print(f"\nChecked: {len(results)}")
    print(f"Unhealthy: {unhealthy_count}")
    print("Detailed results: health-results.json")

    return 1 if unhealthy_count else 0


if __name__ == "__main__":
    sys.exit(main())