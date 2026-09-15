#!/usr/bin/env python3
"""Parallel Search API helper; Python standard library only."""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def search(payload, api_key):
    if not api_key or not api_key.strip():
        raise ValueError('Set PARALLEL_API_KEY in the agent runtime environment.')
    request = urllib.request.Request(
        'https://api.parallel.ai/v1/search',
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'x-api-key': api_key},
        method='POST',
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.load(response)
    except urllib.error.HTTPError as exc:
        guidance = {
            401: 'Check the Parallel API key.',
            403: 'Check account access and balance.',
            422: 'Check the request against the Search API schema.',
            429: 'Rate limited. Wait before retrying.',
        }.get(exc.code, 'Check service status before retrying.')
        exc.close()
        raise RuntimeError(f'Parallel Search HTTP {exc.code}. {guidance}') from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise RuntimeError('Parallel Search network failure or timeout. Check connectivity before retrying.') from None
    except (ValueError, UnicodeError):
        raise RuntimeError('Parallel Search returned invalid JSON.') from None
    if not isinstance(result, dict) or not isinstance(result.get('results'), list):
        raise RuntimeError('Parallel Search returned an unexpected response shape.')
    return result


def positive_int(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError('must be positive')
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--objective', help='Self-contained research question and scope')
    parser.add_argument('--query', action='append', required=True, help='Keyword query; repeat for 2–3 queries')
    parser.add_argument('--mode', choices=['turbo', 'fast', 'basic', 'advanced'], default='fast')
    parser.add_argument('--max-chars-total', type=positive_int, default=20000)
    parser.add_argument('--session-id', help='Session ID from a previous search in the same task')
    parser.add_argument('--dry-run', action='store_true', help='Print request JSON without sending or requiring credentials')
    args = parser.parse_args()
    queries = [query.strip() for query in args.query]
    if not all(queries):
        parser.error('--query must not be blank')
    payload = {'search_queries': queries, 'mode': args.mode, 'max_chars_total': args.max_chars_total}
    if args.objective:
        payload['objective'] = args.objective
    if args.session_id:
        payload['session_id'] = args.session_id
    try:
        result = payload if args.dry_run else search(payload, os.environ.get('PARALLEL_API_KEY', ''))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
