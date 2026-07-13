# firewall.py
# This is our "Defender" - it inspects incoming messages BEFORE they reach the AI,
# and inspects outgoing replies AFTER the AI responds, to catch injection attempts.

import re

SECRET_CODE = "VAULT-CODE-7788"

# Each rule = a pattern name + a list of regex patterns that suggest an attack.
# We keep these human-readable so you can easily add new ones as you discover them.
INJECTION_RULES = [
    {
        "name": "Instruction Override",
        "patterns": [
            r"ignore (all )?(previous|prior|above) instructions",
            r"disregard (all )?(previous|prior|above) instructions",
        ]
    },
    {
        "name": "System Prompt Extraction",
        "patterns": [
            r"(repeat|reveal|show|print|output).{0,30}(system prompt|instructions|exact instructions)",
            r"what (were|are) (the )?(exact )?instructions",
            r"word for word",
        ]
    },
    {
        "name": "Fake Authority Claim",
        "patterns": [
            r"i am (the )?(admin|administrator|developer|system administrator)",
            r"security audit",
            r"debugging purposes",
        ]
    },
    {
        "name": "Roleplay Jailbreak",
        "patterns": [
            r"you are ['\"]?\w+['\"]?,? an? ai with no restrictions",
            r"let'?s play a game",
            r"developer mode",
            r"no restrictions",
        ]
    },
    {
        "name": "Encoding/Spelling Trick",
        "patterns": [
            r"spell (it|the code|out)",
            r"letter by letter",
            r"one letter at a time",
            r"translate the (secret|code)",
        ]
    },
    {
        "name": "Direct Secret Request",
        "patterns": [
            r"vault code",
            r"secret code",
            r"internal code",
        ]
    },
]


def scan_input(user_message: str):
    """
    Checks the user's message against known attack patterns.
    Returns (is_suspicious, matched_rule_names)
    """
    matched_rules = []
    lowered = user_message.lower()

    for rule in INJECTION_RULES:
        for pattern in rule["patterns"]:
            if re.search(pattern, lowered):
                matched_rules.append(rule["name"])
                break  # no need to check other patterns in this rule

    is_suspicious = len(matched_rules) > 0
    return is_suspicious, matched_rules


def scan_output(reply_text: str):
    """
    Safety net: even if the input filter missed something,
    check if the secret code leaked into the AI's reply.
    Returns True if leaked.
    """
    return SECRET_CODE in reply_text


def redact_if_leaked(reply_text: str):
    """
    If the secret leaked anyway, redact it before it reaches the user.
    """
    if SECRET_CODE in reply_text:
        return reply_text.replace(SECRET_CODE, "[REDACTED BY FIREWALL]")
    return reply_text