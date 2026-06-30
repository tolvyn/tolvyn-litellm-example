# tolvyn-litellm-example

Route your existing [LiteLLM](https://github.com/BerriAI/litellm) traffic through
[TOLVYN](https://tolvyn.io) to get **per-team / per-agent / per-end-customer cost
attribution, budget enforcement, and an auditable, hash-chained ledger** — without
changing your application code.

## Why both?

LiteLLM and TOLVYN do different jobs and compose cleanly:

- **LiteLLM** is your routing/translation layer — one interface to OpenAI,
  Anthropic, Gemini, DeepSeek, and 100+ providers.
- **TOLVYN** is your financial-control layer — it answers *who* a cost belongs to,
  *whether* they're allowed to spend it, and writes an immutable record of every call.

You keep your LiteLLM setup exactly as it is. You point it at TOLVYN, and every call
LiteLLM routes is attributed and metered underneath. Two pieces, one request path.

## What this gives you that a spend dashboard doesn't

- **Enforced budgets** — calls can be hard-blocked at a cap, not just reported after.
- **Attribution down to end-customer** — bill or cost-allocate per team, agent, or
  the customer you're reselling AI to.
- **An immutable, hash-chained ledger** — a tamper-evident audit trail for disputes
  and compliance.

## Setup

You need:

- A TOLVYN account and an API key (`tlv_live_...`). Sign up at https://tolvyn.io.
- Your provider key (OpenAI / Anthropic / Gemini / DeepSeek) **stored in TOLVYN**,
  not passed through LiteLLM. TOLVYN injects it server-side. (Account → Provider
  Connections.)
- A team created in TOLVYN if you want team attribution (the team name must exist).

### Option A — LiteLLM gateway

Use `litellm_config.yaml` (see file). The only changes from a normal LiteLLM config:

1. `api_base` points at your TOLVYN proxy route for the provider.
2. `api_key` is your **TOLVYN** key (not the provider key).
3. `extra_headers` carry the attribution you want recorded.

```bash
export TOLVYN_KEY='tlv_live_...'        # your TOLVYN key
litellm --config litellm_config.yaml --port 4000
```

```bash
curl -sS -X POST http://localhost:4000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"my-model","messages":[{"role":"user","content":"hello"}],"max_tokens":16}'
```

### Option B — direct (LiteLLM Python SDK, no gateway)

See `example.py`.

## What lands in TOLVYN

After the call, the request shows up in your TOLVYN dashboard (and ledger)
attributed by the headers you sent:

| field        | value                          |
|--------------|--------------------------------|
| team         | the `X-Tolvyn-Team` you sent   |
| agent        | the `X-Tolvyn-Agent` you sent  |
| model        | the served model               |
| tokens / cost| metered from the provider usage|
| status       | 200                            |

## Attribution headers

| Header                  | Sets         |
|-------------------------|--------------|
| `X-Tolvyn-Team`         | team (name must exist in your TOLVYN account) |
| `X-Tolvyn-Agent`        | agent (free text) |
| `X-Tolvyn-Service`      | service (free text) |
| `X-Tolvyn-End-Customer` | end customer (free text) |

## Notes

- The provider key lives in TOLVYN, encrypted — it is never passed through LiteLLM.
  LiteLLM authenticates to TOLVYN with the TOLVYN key only.
- Swap the provider by changing the proxy route in `api_base`
  (`/v1/proxy/openai/v1`, `/v1/proxy/anthropic/v1`, `/v1/proxy/google/v1`,
  `/v1/proxy/deepseek/v1`) and the model name.

## License

MIT — see [LICENSE](./LICENSE).
