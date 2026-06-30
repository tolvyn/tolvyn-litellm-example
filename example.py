"""
Direct example: call TOLVYN's OpenAI-compatible proxy via the LiteLLM Python SDK,
no gateway process. Attribution headers are passed through to TOLVYN.

  pip install litellm
  export TOLVYN_KEY='tlv_live_...'        # your TOLVYN key (NOT the provider key)
  python example.py

The provider key must already be stored in your TOLVYN account; TOLVYN injects it
server-side. LiteLLM authenticates to TOLVYN with the TOLVYN key only.
"""

import os

from litellm import completion

resp = completion(
    model="openai/deepseek-chat",  # openai/ = OpenAI-compatible wire format
    api_base="https://proxy.tolvyn.io/v1/proxy/deepseek/v1",
    api_key=os.environ["TOLVYN_KEY"],
    messages=[{"role": "user", "content": "hello"}],
    max_tokens=16,
    extra_headers={
        "X-Tolvyn-Team": "my-team",     # must match a team name in your TOLVYN account
        "X-Tolvyn-Agent": "my-agent",   # free text
    },
)

print(resp["choices"][0]["message"]["content"])
print("Check your TOLVYN dashboard — this call is attributed to team 'my-team'.")
