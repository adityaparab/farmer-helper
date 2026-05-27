# Response Compatibility Guide

## Purpose
Define stable API compatibility expectations for response modes, language hooks, structured errors, and streaming events.

## Response modes
Applicable endpoints:
1. `POST /answers/generate`
2. `POST /retrieval/query`

Supported values:
1. `concise`
2. `detailed`

Compatibility rules:
1. `response_mode` is optional and defaults to `concise`.
2. Existing clients that do not send `response_mode` remain compatible.
3. Responses always echo the resolved `response_mode`.

## Language hooks
Applicable endpoints:
1. `POST /answers/generate`
2. `POST /answers/generate-stream`
3. `POST /retrieval/query`

Compatibility rules:
1. `language` is optional and defaults to `en`.
2. Current implementation treats language as a routing/contract hook.
3. Future localization providers should use this field without changing shape.

## Structured error contract
Error payload shape:
1. `status`: currently `error`
2. `error_code`: stable machine-readable code
3. `message`: human-readable detail
4. `retryable`: boolean retry hint

Guidance:
1. Clients should key logic from `error_code` and `retryable`.
2. `message` is suitable for user display and logs.
3. New error fields may be added in future without breaking existing clients.

## Streaming compatibility
Endpoint:
1. `POST /answers/generate-stream`

Media type:
1. `application/x-ndjson`

Event sequence:
1. `metadata` event appears first.
2. Zero or more `chunk` events can appear for answer text.
3. A `final` event always terminates the stream.

Consumer guidance:
1. Process each line as an independent JSON object.
2. Treat unknown event keys as forward-compatible metadata.
3. Final response object in `final` event matches non-stream response fields.

## Backward compatibility policy
1. Existing response fields are not removed without deprecation notice.
2. New optional fields may appear and should be ignored by strict clients unless needed.
3. Contract additions prioritize machine readability and predictable defaults.
