---
short_url: "https://unixwzrd.ai/s/d038dc533a/"
short_link_basis: "/_posts/2026-09-04-hands-on-put-multimodal-context-hygiene-through-a-test-bench.md"
layout: post
title: "Hands-On: Put Multimodal Context Hygiene Through a Test Bench"
date: 2026-09-02 10:00:00 -0500
categories: [hands-on]
tags: [ai, agent-operations, ai-agents, python, qwen, jinja, multimodal, context-hygiene, model-proxy, testing, local-first]
image: /assets/images/blog/agent-optimization/post-07-multimodal-context-hygiene-hero.png
excerpt: "Run sanitized conversations through stock and derived Qwen templates, verify exactly what changes, exercise the routing boundary, and inspect the passive model-proxy relationship."
series: "Local First AI and Agent Operations"
series_part: "7A"
series_order: 75
series_total: 14
series_url: /blog/series/local-first-ai-and-agent-operations/
series_companion_of: 7
series_previous_title: "Multimodal Context Hygiene with a Jinja Chat Template"
series_previous_url: /technology/2026/09/02/multimodal-context-hygiene-with-a-jinja-chat-template/
series_next_title: "From Shell Scripts to an Operator-Ready LLM-Ops-Kit"
series_next_url: /technology/2026/09/06/from-shell-scripts-to-an-operator-ready-llm-ops-kit/
series_next_date: 2026-09-06 10:00:00 -0500
redirect_from:
  - /hands-on/2026/09/04/hands-on-put-multimodal-context-hygiene-through-a-test-bench/
published: true
---

In the [main Part 7 article]({{ page.series_previous_url | relative_url }}), I explained why media-history filtering belongs in the selected Qwen Jinja template instead of inside a model proxy that is supposed to remain passive. This companion lets you take that explanation apart and see whether it actually holds up.

I did not want to publish another page of source code and ask readers to accept it on faith. The useful part is running the same invented conversation through both templates and asking plain questions: Did the old image payload disappear? Did the latest audio result and native vision placeholder remain? Did ordinary tool history stay byte-for-byte identical?

That is the whole point of this lab. You do not need a model, GPU, private capture, or production agent configuration; Python and Jinja are enough for the core exercise. If LLM-Ops-Kit is already installed, the optional final section sends the same sanitized request through the model-proxy renderer. It shows where the proxy fits without pretending that the proxy performs the filtering.

<!--more-->

## What You Will Build and Verify

The package contains both Qwen templates, seven invented fixtures, expected results, two small Python tools, and two test modules. `inspect_fixture.py` renders each fixture twice and reports a bounded comparison without printing the long synthetic payloads.

{% include blog_diagram.html
   src="/assets/images/blog/agent-optimization/post-07a-template-lab.svg"
   alt="Sanitized fixtures rendered through stock and derived Qwen templates, compared by a bounded inspector, and checked by eleven executable tests."
   variant="series" %}

The lab gives you enough evidence to verify these boundaries yourself:

| Experiment | Result that must hold |
| --- | --- |
| Ordinary text and tool history | Stock and derived renders match exactly |
| Textual image history | Every image-producing call and result pair is absent from the derived render |
| Explicit textual audio and video history | Only the latest result of each type remains |
| Native structured image and video parts | Qwen image and video placeholders remain |
| Incidental PNG-looking text | Ordinary tool output remains when image-result structure is absent |
| Invalid system-message ordering | Both templates reject it with the intended validation error |
| Provenance | The packaged stock and derivative checksums match the reviewed files |

The character counts in this lab are measurements of invented rendered strings. They are not token counts, cost estimates, latency results, or generation-quality scores. I am using them because they make the transformation visible without pretending that one synthetic fixture predicts a production workload.

## Step 1: Unpack the Lab in Its Own Directory

Download the [complete twelve-file Hands-On 7A package]({{ '/assets/code/agent-optimization/post-07a/hands-on-07a-qwen-media-history-test-bench.zip' | relative_url }}) and expand it into a fresh working directory. Do not mix it into a model installation yet. I want the first pass to be about understanding the template behavior before a runtime or live model can complicate the result.

Every file is also available below through the site's standard source viewer. The disclosures stay collapsed until you choose one, and each file can be downloaded separately.

{% include source_code.html source="/assets/code/agent-optimization/post-07a/Qwen-3_5-media-history-template.jinja" language="jinja" title="Qwen-3_5-media-history-template.jinja" %}

{% include source_code.html source="/assets/code/agent-optimization/post-07a/Qwen-3_5-stock-template.jinja" language="jinja" title="Qwen-3_5-stock-template.jinja" %}

{% include source_code.html source="/assets/code/agent-optimization/post-07a/README.md" language="markdown" title="README.md" %}

{% include source_code.html source="/assets/code/agent-optimization/post-07a/fixtures.json" language="json" title="fixtures.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-07a/expected-results.json" language="json" title="expected-results.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-07a/render_fixture.py" language="python" title="render_fixture.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-07a/inspect_fixture.py" language="python" title="inspect_fixture.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-07a/test_media_history_template.py" language="python" title="test_media_history_template.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-07a/test_inspect_fixture.py" language="python" title="test_inspect_fixture.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-07a/requirements.txt" language="text" title="requirements.txt" %}

{% include source_code.html source="/assets/code/agent-optimization/post-07a/NOTICE.md" language="markdown" title="NOTICE.md" %}

{% include source_code.html source="/assets/code/agent-optimization/post-07a/LICENSE-APACHE-2.0.txt" language="text" title="LICENSE-APACHE-2.0.txt" %}

Create the working directory, download the archive, and inspect the inventory:

```bash
mkdir -p qwen-media-history-lab
cd qwen-media-history-lab
curl -fsSLo lab.zip https://unixwzrd.ai/assets/code/agent-optimization/post-07a/hands-on-07a-qwen-media-history-test-bench.zip
unzip lab.zip
rm lab.zip
ls -1
```

You should see both templates, fixtures, expectations, renderer, inspector, tests, the pinned Jinja requirement, and the provenance and license documents. Keep `NOTICE.md` and `LICENSE-APACHE-2.0.txt` with the templates. The derivative is Apache-2.0 material with an attribution and modification boundary.

## Step 2: Create a Small Python Environment

I prefer to run a lab like this in a disposable virtual environment. It keeps the one Python dependency visible and makes cleanup straightforward:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -c 'import jinja2; print(jinja2.__version__)'
```

The reviewed package pins Jinja 3.1.6 because that is the version exercised by the companion and the matching application-owned runtime. The template also expects the Hugging Face-style `raise_exception` helper. The standalone renderer supplies that helper locally, so you do not need a model server to reach the validation paths.

If Jinja is already available in an environment you trust, you can use that environment instead. I would still check the version and run the tests before drawing conclusions from a render.

## Step 3: Run the Contract Before Inspecting Pretty Output

Start with the tests:

```bash
python -m unittest -v test_media_history_template.py test_inspect_fixture.py
```

The expected result is eleven passing tests. Three cover template provenance, fixture behavior, and fixture-name agreement. Eight cover the reader-facing inspector, including ordinary-history equivalence, negative aggregate-result cases, textual-image removal, native placeholder retention, the intended malformed-ordering error, and the strict 4,096-character boundary.

A rendered prompt can look perfectly plausible while quietly dropping a role boundary, tool result, or assistant-generation marker. These tests do not prove that the model will produce a good answer, but they do prove agreement with the published fixture contract.

## Step 4: Compare All Seven Fixtures Without Dumping the Payloads

Run the bounded inspector:

```bash
python inspect_fixture.py
```

You should see this table:

```text
fixture                            stock   derived     delta         result
------------------------------ --------- --------- --------- --------------
native_structured_media              172       172         0           pass
textual_image_exchanges            10975       156    -10819           pass
latest_audio_video                 21263     10723    -10540           pass
truncated_image_history             5475       137     -5338           pass
incidental_signature_collision      5419      5419         0           pass
malformed_ordering                 error     error       n/a expected error
ordinary_text_tool_history           409       409         0           pass
```

Those numbers are deterministic for the packaged fixtures and templates. The negative delta is simply the derived character count minus the stock character count. It tells me how much invented rendered text the policy removed in this particular fixture, and nothing by itself about tokenizer behavior, KV-cache allocation, latency, cost, or answer quality.

The zero-delta cases matter too. Native structured media keeps its Qwen placeholders. The incidental-signature fixture stays intact because a marker without image-result structure is not enough to classify an image exchange.

## Step 5: Inspect One Decision in Detail

Ask the inspector for the textual-image case as JSON:

```bash
python inspect_fixture.py textual_image_exchanges --json
```

The result reports 10,975 stock characters, 156 derived characters, and seven passing absence checks without printing the canary expansions. I can see whether the contract held without turning the test log into another synthetic media archive.

Now use the lower-level renderer to prove that the markers really are present under the stock template and absent under the derivative:

```bash
python render_fixture.py textual_image_exchanges \
  --template ./Qwen-3_5-stock-template.jinja \
  | grep -oE 'PNG_(OLD|NEW)_CANARY' \
  | sort -u

python render_fixture.py textual_image_exchanges \
  --template ./Qwen-3_5-media-history-template.jinja \
  | grep -oE 'PNG_(OLD|NEW)_CANARY' \
  | sort -u
```

The stock command prints both canary names. The derivative command prints nothing. Because `grep` returns a nonzero status when it finds no match, that second pipeline may also leave a nonzero shell status. In this one inspection, that absence is the expected result.

This is also where complete-exchange removal becomes easier to understand. The derived render does not merely replace the long tool result with a note. It removes the associated assistant tool call, the textual result, and the assistant-side decode exchange covered by the fixture. Leaving the call while deleting only the result would create a malformed history that looks smaller but no longer tells a coherent story.

## Step 6: Check Native Media and Ordinary History

Inspect the two cases that must remain useful:

```bash
python inspect_fixture.py native_structured_media --json
python inspect_fixture.py ordinary_text_tool_history --json
```

The native case reports one `<|image_pad|>` and one `<|video_pad|>`. The long data URL itself is not placed into the rendered prompt, which is normal for this Qwen contract. The model engine receives and processes the structured media outside the textual template output.

The ordinary-history case reports `exact_match: true` and a character delta of zero. That comparison is the control. An optimization that removes obvious media payloads but changes routine tool calling, thinking layout, role boundaries, or assistant generation behavior is not a safe drop-in improvement.

## Step 7: Touch the 4,096-Character Boundary

The template only considers textual media results longer than 4,096 characters. That threshold is a routing gate. It is not base64 validation and it is not a general definition of media.

Run this temporary experiment from the lab directory:

```bash
python - <<'PY'
from render_fixture import render_case

prefix = '{"images":["iVBORw0KGgoTHRESHOLD_CANARY'
suffix = '"]}'

for length in (4096, 4097):
    content = prefix + ('A' * (length - len(prefix) - len(suffix))) + suffix
    case = {
        'payload': {
            'messages': [
                {'role': 'user', 'content': 'Create an invented image.'},
                {
                    'role': 'assistant',
                    'content': 'threshold image call',
                    'tool_calls': [
                        {
                            'type': 'function',
                            'function': {
                                'name': 'terminal',
                                'arguments': {'command': 'generate invented image'},
                            },
                        }
                    ],
                },
                {'role': 'tool', 'content': content},
                {'role': 'user', 'content': 'Continue.'},
            ],
            'tools': [],
            'add_generation_prompt': True,
        }
    }
    rendered = render_case(case)
    state = 'retained' if 'THRESHOLD_CANARY' in rendered else 'removed'
    print(f'{length}: {state}')
PY
```

The expected output is:

```text
4096: retained
4097: removed
```

I like this experiment because it leaves very little room for vague language. The condition is greater than 4,096, not greater than or equal to it, and the other image-result structure and marker checks still apply. One character changes the routing decision. That is exactly the sort of edge I would rather capture in a canary than explain in a comment and hope everybody interprets the same way.

## Step 8: See Where the Passive Model Proxy Fits

The core lab calls Jinja directly because a proxy or live model would only distract from the policy being tested. In an installed LLM-Ops-Kit route, the passive proxy can render a diagnostic view while forwarding the original OpenAI-compatible request upstream unchanged. The model runtime then uses the selected template to construct the actual prompt. Both rendering paths must point at the same template file if I expect those two views to agree.

{% include blog_diagram.html
   src="/assets/images/blog/agent-optimization/post-07a-proxy-template-boundary.svg"
   alt="A passive model proxy forwards the original request unchanged while its diagnostic renderer and the Qwen runtime reference the same selected media-history template."
   variant="series" %}

If `model-proxy` is installed, create a sanitized expanded request from the packaged fixture:

```bash
python - <<'PY' > ./sanitized-media-request.json
import json
from render_fixture import expand

with open('fixtures.json', encoding='utf-8') as handle:
    cases = json.load(handle)

print(json.dumps(expand(cases['textual_image_exchanges']['payload'])))
PY
```

If `jq` is available, you can inspect the request structure without printing message content or synthetic media strings:

```bash
jq '{message_count: (.messages | length), roles: [.messages[].role], assistant_tool_calls: ([.messages[] | select(.role == "assistant") | .tool_calls[]?] | length), tool_results: ([.messages[] | select(.role == "tool")] | length), structured_image_parts: ([.messages[].content? | arrays | .[] | select((.type? == "image") or has("image_url") or has("image"))] | length), structured_video_parts: ([.messages[].content? | arrays | .[] | select((.type? == "video") or has("video"))] | length)}' sanitized-media-request.json
```

For this fixture, the structural inventory reports eight messages, three assistant tool calls, three tool results, and no native structured image or video parts. The `roles` array shows the turn order without exposing message content. This check is optional because the core lab does not require `jq`.

Render it first with the stock template and then with the derivative, keeping the two diagnostic files separate:

```bash
model-proxy render \
  --input ./sanitized-media-request.json \
  --chat-template ./Qwen-3_5-stock-template.jinja \
  --log ./stock-render-metrics.ndjson \
  --raw-request-log ./stock-request.log \
  --rendered-prompt-log ./stock-rendered.log

model-proxy render \
  --input ./sanitized-media-request.json \
  --chat-template ./Qwen-3_5-media-history-template.jinja \
  --log ./derived-render-metrics.ndjson \
  --raw-request-log ./derived-request.log \
  --rendered-prompt-log ./derived-rendered.log
```

Now compare only the invented canaries:

```bash
grep -oE 'PNG_(OLD|NEW)_CANARY' stock-rendered.log | sort -u
grep -oE 'PNG_(OLD|NEW)_CANARY' derived-rendered.log | sort -u

python - <<'PY'
import json

def framed_payload(path):
    text = open(path, encoding='utf-8').read()
    start = text.index('\n') + 1
    end = text.rindex('\n=== RAW_REQUEST END')
    return json.loads(text[start:end])

assert framed_payload('stock-request.log') == framed_payload('derived-request.log')
print('raw request payloads match')
PY
```

The stock diagnostic contains the textual image canaries and the derived diagnostic does not. The raw request payloads match after the timestamped frame headers and footers are excluded. Those timestamps are expected to differ because these are two separate render-only runs.

Render-only mode does not start the proxy or send bytes across a network, so this exercise does not independently prove passive forwarding. It shows that selecting a different diagnostic template changes the rendered view without changing the input payload recorded by the tool. The proxy's byte-preservation contract is covered by its production regressions and by Hands-On 6A. In a live route, the filtering still happens when the selected template renders message history, not while the proxy forwards the request.

This exercise writes only invented data, but its rendered and raw logs are still content-bearing artifacts. I would not repeat it with a private capture merely because the command happens to be convenient.

## Step 9: Clean Up the Lab Evidence

The standalone tests use temporary files and clean those up themselves. The optional proxy exercise creates the request and log files named above. Remove those invented artifacts when you are finished, then leave the virtual environment:

```bash
rm -f ./sanitized-media-request.json \
  ./stock-render-metrics.ndjson \
  ./stock-request.log \
  ./stock-rendered.log \
  ./derived-render-metrics.ndjson \
  ./derived-request.log \
  ./derived-rendered.log
deactivate
```

If you skipped the optional proxy exercise, those files will not exist and there is nothing to remove. Keep the package if you want a known comparison baseline, and keep the stock fallback beside the derivative if you move on to a private runtime canary. A rollback file stored somewhere else is not much of a rollback plan.

## What This Lab Does Not Prove

The lab proves behavior against seven invented fixture shapes. It does not prove better answers, universal Qwen compatibility, portability to another ChatML-style model, tokenizer-specific savings, KV-cache allocation, generation speed, or cost.

It also does not make the teaching package a production rollout procedure. A real change needs the exact model revision, exact runtime, bundled stock template, sanitized render canaries, ordinary text and tool-call checks, native vision checks, bounded generation acceptance, restart planning, health verification, and a tested rollback. If any role boundary, tool call, thinking behavior, native vision path, or generation terminator changes unexpectedly, restore the stock template and investigate.

## Current State

The separate Hands-On 7A package contains the technically approved stock and derived Qwen templates, seven sanitized fixtures, expected results, provenance and license material, the original renderer and tests, and a bounded inspector with eight additional tests. All eleven companion tests pass under Python with Jinja 3.1.6. The inspector produces the documented character counts and marker checks, and both the permanent threshold regression and temporary reader exercise produce the documented 4,096 and 4,097 results. The original nine-file Part 7 package remains byte-stable.

The tutorial, inspector, tests, requirements file, package, and two diagrams passed technical review before being staged here. The package remains a teaching artifact rather than a production template rollout.

## Next Work

The lab uses its own twelve-file archive, leaving the approved Part 7 download unchanged. A later revision may add a bounded model-generation canary after the render-only contract remains stable across the exact model and runtime under test.

The next production-facing step is still a bounded model and runtime canary, not a larger synthetic benchmark. The lesson I want readers to take away is simpler: give the same invented history to the stock and derived paths, verify what changed, verify what did not, and keep the passive observer out of the mutation business.
