"""What the stand-in scripts share: their options, the status file they write and the log of what they were asked."""
import json, os, sys, time
from datetime import datetime, timezone


def now():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def args(argv):
    opts = {argv[k]: argv[k + 1] for k in range(len(argv) - 1) if argv[k].startswith('--')}
    pos = [a for k, a in enumerate(argv) if not a.startswith('--') and not (k and argv[k - 1].startswith('--'))]
    return pos, opts


def log(who, **kw):
    if os.environ.get('STANDIN_LOG'):
        with open(os.environ['STANDIN_LOG'], 'a') as f:
            f.write(json.dumps(dict(kw, who=who, t=time.time())) + '\n')


def write(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(obj, open(path + '.tmp', 'w'), indent=1)
    os.replace(path + '.tmp', path)
