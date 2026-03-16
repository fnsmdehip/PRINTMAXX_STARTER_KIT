#!/bin/bash
# Test the guardrail hook
HOOK="$HOME/.claude/scripts/guardrail-hook.sh"
PASS=0; FAIL=0

test_allow() {
  local desc="$1"; local input="$2"
  echo "$input" | "$HOOK" > /dev/null 2>&1
  if [ $? -eq 0 ]; then echo "  ALLOW OK: $desc"; ((PASS++)); else echo "  ALLOW FAIL: $desc"; ((FAIL++)); fi
}

test_block() {
  local desc="$1"; local input="$2"
  result=$(echo "$input" | "$HOOK" 2>&1)
  code=$?
  if [ $code -eq 2 ]; then echo "  BLOCK OK: $desc — $result"; ((PASS++)); else echo "  BLOCK FAIL: $desc (exit=$code)"; ((FAIL++)); fi
}

echo "=== CAPABILITY (should allow) ==="
test_allow "app launch"     '{"tool_name":"Bash","tool_input":{"command":"open -a Simulator"}}'
test_allow "curl"            '{"tool_name":"Bash","tool_input":{"command":"curl https://api.example.com"}}'
test_allow "python"          '{"tool_name":"Bash","tool_input":{"command":"python3 test.py"}}'
test_allow "simulator"       '{"tool_name":"Bash","tool_input":{"command":"xcrun simctl list"}}'
test_allow "git commit"      '{"tool_name":"Bash","tool_input":{"command":"git commit -m fix"}}'
test_allow "git push"        '{"tool_name":"Bash","tool_input":{"command":"git push origin main"}}'
test_allow "npm install"     '{"tool_name":"Bash","tool_input":{"command":"npm install express"}}'
test_allow "brew"            '{"tool_name":"Bash","tool_input":{"command":"brew install jq"}}'
test_allow "surge deploy"    '{"tool_name":"Bash","tool_input":{"command":"surge ./build"}}'
test_allow "launchctl"       '{"tool_name":"Bash","tool_input":{"command":"launchctl list"}}'
test_allow "project write"   '{"tool_name":"Write","tool_input":{"file_path":"/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/test.py"}}'
test_allow "tmp write"       '{"tool_name":"Write","tool_input":{"file_path":"/tmp/test.txt"}}'
test_allow "claude dir"      '{"tool_name":"Write","tool_input":{"file_path":"/Users/macbookpro/.claude/test.txt"}}'
test_allow "launchagent"     '{"tool_name":"Write","tool_input":{"file_path":"/Users/macbookpro/Library/LaunchAgents/test.plist"}}'
test_allow "project rm"      '{"tool_name":"Bash","tool_input":{"command":"rm /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/old.txt"}}'
test_allow "kill node"       '{"tool_name":"Bash","tool_input":{"command":"killall node"}}'
test_allow "ls anything"     '{"tool_name":"Bash","tool_input":{"command":"ls ~/Desktop"}}'
test_allow "cat anything"    '{"tool_name":"Bash","tool_input":{"command":"cat /etc/hosts"}}'

echo ""
echo "=== DESTRUCTION (should block) ==="
test_block "rm -rf home"     '{"tool_name":"Bash","tool_input":{"command":"rm -rf ~/"}}'
test_block "rm -rf root"     '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}'
test_block "rm -rf star"     '{"tool_name":"Bash","tool_input":{"command":"rm -rf *"}}'
test_block "git force push"  '{"tool_name":"Bash","tool_input":{"command":"git push --force origin main"}}'
test_block "git push -f"     '{"tool_name":"Bash","tool_input":{"command":"git push -f origin main"}}'
test_block "git reset hard"  '{"tool_name":"Bash","tool_input":{"command":"git reset --hard origin/main"}}'
test_block "git clean"       '{"tool_name":"Bash","tool_input":{"command":"git clean -fd"}}'
test_block "write desktop"   '{"tool_name":"Write","tool_input":{"file_path":"/Users/macbookpro/Desktop/pwned.txt"}}'
test_block "write documents" '{"tool_name":"Write","tool_input":{"file_path":"/Users/macbookpro/Documents/other/file.txt"}}'
test_block "write ssh"       '{"tool_name":"Write","tool_input":{"file_path":"/Users/macbookpro/.ssh/id_rsa"}}'
test_block "write zshrc"     '{"tool_name":"Edit","tool_input":{"file_path":"/Users/macbookpro/.zshrc"}}'
test_block "write etc"       '{"tool_name":"Write","tool_input":{"file_path":"/etc/hosts"}}'
test_block "write creds"     '{"tool_name":"Write","tool_input":{"file_path":"/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/credentials.json"}}'
test_block "dd"              '{"tool_name":"Bash","tool_input":{"command":"dd if=/dev/zero of=/dev/sda"}}'
test_block "diskutil"        '{"tool_name":"Bash","tool_input":{"command":"diskutil eraseDisk JHFS+ Clean disk0"}}'
test_block "killall finder"  '{"tool_name":"Bash","tool_input":{"command":"killall Finder"}}'
test_block "rm outside"      '{"tool_name":"Bash","tool_input":{"command":"rm -r /Users/macbookpro/other_project"}}'
test_block "zshrc redirect"  '{"tool_name":"Bash","tool_input":{"command":"echo bad > ~/.zshrc"}}'

echo ""
echo "=== RESULTS: $PASS passed, $FAIL failed ==="
