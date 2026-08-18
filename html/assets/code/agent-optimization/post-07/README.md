# Qwen 3.5 Media-History Template Companion

This package is the practical companion for Part 7 of the Local-First Agent Operations series. It gives Hermes users running a matching Qwen model route a reviewable chat template, a stock fallback, sanitized fixtures, expected results, provenance checks, and rollback instructions.

It is not a generic ChatML template. Qwen uses `<|im_start|>` and `<|im_end|>` as its ChatML turn envelope, and its tool calling is Hermes-like, but this complete file also depends on Qwen vision placeholders, thinking layout, tool-call serialization, and Jinja runtime helpers. The media-history policy may be ported to another ChatML-style template only after preserving that model's control tokens, multimodal markers, reasoning rules, tool schema, and assistant generation boundary.

## Package Contents

| File | Purpose |
| --- | --- |
| `Qwen-3_5-media-history-template.jinja` | Attributed Apache-2.0 derivative with media-history pruning |
| `Qwen-3_5-stock-template.jinja` | Unmodified fallback baseline, apart from one trailing newline |
| `fixtures.json` | Seven invented, compact fixtures expanded locally into long synthetic media markers |
| `expected-results.json` | Expected retained, omitted, counted, error, and stock-equivalence results |
| `render_fixture.py` | Renders one fixture for manual inspection |
| `test_media_history_template.py` | Self-contained checksum and behavior tests |
| `NOTICE.md` | Immutable provenance, modification notice, checksums, and license boundary |
| `LICENSE-APACHE-2.0.txt` | Apache License 2.0 text |

## Supported Input Assumptions

The tested runtime supplies Jinja 3.1.6 and the `raise_exception` helper used by the Qwen template. The render context includes `messages`, `tools`, `add_generation_prompt`, `enable_thinking`, `add_vision_id`, `bos_token`, and `eos_token`.

Messages use the Qwen 3.5-family shape exercised by the fixtures:

- roles are `system`, `user`, `assistant`, or `tool`;
- content is a string, `null`, or a list of structured text, image, or video parts;
- assistant `tool_calls` are iterable and each call exposes a function name and argument mapping;
- tool results are textual strings when the media-history policy inspects them;
- native structured images and videos are processed separately by the model engine after the template emits Qwen vision placeholders.

The template has also worked with the matching Qwen 3.6 prompt format in the publisher's environment. That is an operational observation, not universal compatibility evidence. Render and generation acceptance are still required for the exact model artifact and runtime you use.

## What the Policy Does

Textual image tool results are removed as complete exchanges, including the most recent result. They are often truncated before they reach history and cannot be reconstructed reliably. Native structured image and video parts remain eligible and render Qwen vision placeholders.

For explicit textual audio and video results, only the latest result of each type remains. Older associated assistant calls and tool results are removed. Assistant tool calls that carry recognizable media bytes or explicitly decode base64 are also removed.

Textual tool-result detection requires content longer than 4,096 characters. Image detection also requires image-result structure plus a PNG, JPEG, or `data:image/` marker. Audio and video detection require their corresponding result labels and data-URL markers. Jinja does not validate base64. The threshold and marker checks are routing policy, not proof that the payload is valid media.

## Stock Versus Derived Behavior

| Input history | Stock Qwen template | Media-history derivative |
| --- | --- | --- |
| Ordinary text and tool history | Retained | Byte-identical rendered prompt in the supplied fixture |
| Native structured image or video part | Qwen vision placeholder retained | Qwen vision placeholder retained |
| Textual image tool result | Retained as tool-response text | Entire image-producing exchange removed |
| Assistant-side media byte or decode call | Retained | Associated assistant call and following tool result removed |
| Multiple explicit textual audio results | All retained | Only latest explicit audio exchange retained |
| Multiple explicit textual video results | All retained | Only latest explicit video exchange retained |
| Long incidental PNG signature without image-result structure | Retained | Retained |
| Malformed system-message ordering | Template error | Same template error |

## Verify Before Installing

Run the checksum and behavior suite with the same application-owned Python environment used by LLM-Ops-Kit:

```bash
python -m unittest -v test_media_history_template.py
```

Render individual sanitized fixtures before touching a model profile:

```bash
python render_fixture.py native_structured_media
python render_fixture.py textual_image_exchanges
python render_fixture.py ordinary_text_tool_history
```

The fixture payloads are invented. Long base64-like strings are generated locally from obvious canary markers and repeated letters; they are not real images, audio, video, prompts, conversations, or model output.

If you have a sanitized captured OpenAI-compatible request, render it with the LLM-Ops-Kit proxy tool and compare stock with derived output:

```bash
model-proxy render \
  --input sanitized-request.json \
  --chat-template ./Qwen-3_5-stock-template.jinja

model-proxy render \
  --input sanitized-request.json \
  --chat-template ./Qwen-3_5-media-history-template.jinja
```

Do not use a private production capture for a public comparison. Remove hostnames, users, paths, tokens, conversation content, media, tool arguments, and generated artifacts first.

## Install for a Tested llama.cpp Route

Keep both files together in an operator-owned template directory. Point the Qwen model profile at the derivative and ensure the runtime starts llama.cpp with Jinja and the same chat-template file:

```text
--jinja --chat-template-file /path/to/Qwen-3_5-media-history-template.jinja
```

For an LLM-Ops-Kit model profile, the relevant shape is:

```json
{
  "template": {
    "enabled": true,
    "path": "/path/to/Qwen-3_5-media-history-template.jinja"
  }
}
```

Plan the restart, apply it, and verify status using your configured stack and component names:

```bash
llmops component plan restart STACK:MODEL_COMPONENT
llmops component restart STACK:MODEL_COMPONENT
llmops component status STACK:MODEL_COMPONENT
```

If the passive model proxy renders diagnostic prompts, point its `--chat-template` setting at the same file. Otherwise the diagnostic view can disagree with what llama.cpp constructs.

Hermes continues sending its OpenAI-compatible message and tool history to the selected Qwen route. The filtering happens when the model runtime renders that history. This package does not require rewriting Hermes requests in a proxy.

## Acceptance and Rollback

Before replacement, retain the model's bundled template, the exact model revision, and one sanitized render fixture. Compare stock and derivative output, then run a bounded generation canary that covers ordinary text, tool calling, native structured vision, and the media-history case you actually need.

If role boundaries, thinking behavior, tool calls, native vision, or generation termination changes unexpectedly, restore the stock fallback immediately:

```json
{
  "template": {
    "enabled": true,
    "path": "/path/to/Qwen-3_5-stock-template.jinja"
  }
}
```

Restart the model component and repeat the same sanitized render and generation canaries. Do not keep the derivative merely because it reduces a prompt. Correct model behavior remains the acceptance gate.

## License and Provenance

The Qwen baseline and this derivative are distributed under Apache License 2.0. Read `NOTICE.md` for the immutable upstream URL, revision, modification notice, and checksums. Read `LICENSE-APACHE-2.0.txt` for the license terms.
