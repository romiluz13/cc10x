#!/bin/bash
# Scaffold for two-workflow-resume: a repo with two in-flight workflow artifacts, the unrelated one newer. Runs in the empty run workspace.
set -eu
git init -q -b main
git config user.email "eval@example.invalid"
git config user.name "Eval Fixture"
mkdir -p .cc10x/workflows
cat > .cc10x/workflows/wf-alpha-0001.json <<'EOF'
{"workflow_uuid":"wf-alpha-0001","workflow_id":"wf-alpha-0001","workflow_type":"BUILD","state_root":".cc10x","user_request":"create alpha.txt containing the single line alpha","phase_cursor":"build-implement","proof_status":"gaps_found","status_history":[{"event":"workflow_started"}]}
EOF
cat > .cc10x/workflows/wf-beta-0002.json <<'EOF'
{"workflow_uuid":"wf-beta-0002","workflow_id":"wf-beta-0002","workflow_type":"BUILD","state_root":".cc10x","user_request":"create beta.txt containing the single line beta","phase_cursor":"beta-hold","proof_status":"gaps_found","status_history":[{"event":"workflow_started"}]}
EOF
touch -t 202601010000 .cc10x/workflows/wf-alpha-0001.json
touch -t 202602010000 .cc10x/workflows/wf-beta-0002.json
printf '# Scratch repo\n' > README.md
git add -f .cc10x
git add -A
git commit -q -m "chore: initial commit"
