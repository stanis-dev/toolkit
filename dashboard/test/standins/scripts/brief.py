"""Stand-in for brief.py: as a command, a one-line brief; imported, the real module (brief_real.py, copied in)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if __name__ == '__main__':
    import standin
    pos, o = standin.args(sys.argv[1:])
    if os.environ.get('STANDIN_BRIEF_FAIL'):
        sys.exit('stand-in brief refused')
    print(f'# Brief stand-in · {" ".join(pos)} · step {o.get("--step")}')
else:
    from brief_real import *  # noqa: F401,F403
