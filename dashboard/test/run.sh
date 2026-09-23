#!/bin/bash
# Every check of the staging dashboard: the server's unittest (lab on :8491), the scripts' (run.py and stepgit.py on a
# throwaway worktree) and the page's smoke run in a headless Chrome (lab on :8490), side by side. Exit 0 only when both pass.
D="$(dirname "$(realpath "$0")")"
t0=$(date +%s)
( python3 -W ignore::ResourceWarning -m unittest discover -s "$D" -p 'test_server.py' 2>&1; r=$?; python3 -W ignore::ResourceWarning -m unittest discover -s "$D" -p 'test_steps.py' 2>&1; exit $(( r | $? )) ) >"$D/unittest.out" & u=$!
( STANDIN_SECONDS=2 python3 "$D/lab.py" up "$D/run-smoke" 8490 && node "$D/smoke.mjs" http://127.0.0.1:8490 "$D/run-smoke"; r=$?; python3 "$D/lab.py" down "$D/run-smoke"; exit $r ) >"$D/smoke.out" 2>&1 & s=$!
wait $u; ur=$?; wait $s; sr=$?
echo "== unittest (test_server.py, then test_steps.py)"; cat "$D/unittest.out"
echo "== smoke (smoke.mjs)"; cat "$D/smoke.out"
echo "== $(( $(date +%s) - t0 )) s · unittest $([ $ur = 0 ] && echo passed || echo FAILED) · smoke $([ $sr = 0 ] && echo passed || echo FAILED)"
[ $ur = 0 ] && [ $sr = 0 ]
