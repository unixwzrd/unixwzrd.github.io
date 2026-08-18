# Attribution and Modification Notice

`Qwen-3_5-media-history-template.jinja` is a modified form of Qwen's `chat_template.jinja` from `Qwen/Qwen3.5-27B`.

Upstream source:

- Repository: `Qwen/Qwen3.5-27B`
- Immutable revision: `feea018b31f89dc0950e61da42577a7a4ab09169`
- Source file: `https://huggingface.co/Qwen/Qwen3.5-27B/blob/feea018b31f89dc0950e61da42577a7a4ab09169/chat_template.jinja`
- Raw source: `https://huggingface.co/Qwen/Qwen3.5-27B/resolve/feea018b31f89dc0950e61da42577a7a4ab09169/chat_template.jinja`
- Upstream license: Apache License 2.0

The derivative adds a media-history policy that:

- removes every textual image tool result and its associated assistant tool exchange;
- removes assistant tool calls that explicitly carry or decode historical media bytes;
- retains only the latest explicit textual audio result and latest explicit textual video result;
- preserves native structured image and video message parts and their Qwen vision placeholders;
- requires media-result structure, known data markers, and a content length greater than 4,096 characters for textual tool-result detection.

The derivative does not validate base64 data. It does not claim compatibility with arbitrary ChatML, Llama, Mistral, Gemma, OpenAI, or other model-family templates.

## SHA-256 Checksums

| Artifact | SHA-256 |
| --- | --- |
| Immutable upstream `chat_template.jinja` bytes | `a4aee8afcf2e0711942cf848899be66016f8d14a889ff9ede07bca099c28f715` |
| Packaged stock fallback with one trailing newline | `d2cb9a5730cdd5f44bce3ada2dc1b0e00c6c59788b6d1c4d8d49c40a274dffb0` |
| Published attributed media-history derivative | `162671aeaf5e2c39966816dae53e5e6f8ac0dfb97d53f34094afe74e44b2fae6` |

The packaged stock fallback is byte-equivalent to the immutable upstream file after removing its single trailing newline. The test suite verifies both forms and the derivative checksum without requiring network access.

The template files and modifications in this companion are distributed under Apache License 2.0. They are not presented as solely covered by the surrounding repository's MIT license. See `LICENSE-APACHE-2.0.txt`.
