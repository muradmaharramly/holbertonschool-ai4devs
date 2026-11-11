# Risk Assessment — jQuery 1.12.4 (Legacy `1.x` Branch)

Prioritized risk register for **jQuery `1.12.4`** (`f55d0ec8`), ranked by severity (`High`, `Medium`, `Low`) and grounded in verified source locations.

---

## 1. Prioritized Risk Matrix

| ID | Risk | Severity | Category | Primary Locations | Summary Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **R1** | DOM XSS via `htmlPrefilter` & `innerHTML` parsing | **High** | Security | `src/manipulation.js:33,288-290`<br>`src/manipulation/buildFragment.js:56`<br>`src/core/parseHTML.js:30-34` | `rxhtmlTag` regex rewrites self-closing tags before `innerHTML` assignment; `parseHTML()` evaluates inline event handlers (`onerror`, etc.) during `innerHTML` parsing before stripping `<script>` tags. |
| **R2** | Prototype pollution in `jQuery.extend(true, ...)` | **High** | Security | `src/core.js:156-184` | `for (name in options)` lacks a `"__proto__"` guard; deep-merging untrusted JSON payloads can mutate `Object.prototype`. |
| **R3** | Auto-executed AJAX script responses & CSP `'unsafe-eval'` | **High** | Security / Platform | `src/ajax/script.js:13-21`<br>`src/ajax.js:153-160`<br>`src/core.js:290-300`<br>`src/ajax/parseJSON.js:47` | Omitting `dataType` in `$.ajax()` auto-executes `javascript` Content-Type responses via `globalEval()` (`eval`/`execScript`); `parseJSON()` falls back to `Function(...)`. Fails strict CSP. |
| **R4** | Uncaught exceptions & synchronous re-entrancy in `$.Deferred` | **Medium** | Reliability | `src/deferred.js:13-49` | Exceptions inside `.then()` handlers are not caught into rejections; `Callbacks("once memory")` runs settled callbacks synchronously, violating Promises/A+ ordering. |
| **R5** | Tight coupling via shared `jQuery.cache` & global state | **Medium** | Maintainability | `src/data.js:61-104`<br>`src/exports/global.js:24-26`<br>`src/event.js:456,534-542` | Events, queues, manipulation flags, and user data share mutable `jQuery.cache` and expando keys; `handlers()` mixes Array + Map semantics on `matches = []`. |
| **R6** | Fragile regex-based bundler & untested custom builds | **Medium** | Build / Release | `build/tasks/build.js:49-104`<br>`README.md:93,149` | RequireJS output is flattened with AST-less regexes (`convert()`); custom module exclusion combos (`grunt custom:-...`) are not tested in CI. |
| **R7** | EOL toolchain, ES3 lock-in & IE6–8 workaround bloat | **Medium** | Tech Debt / Operations | `package.json`, `.travis.yml`<br>`src/.jshintrc:19`<br>`src/ajax/xhr.js`, `src/manipulation.js` | Depends on EOL Node `0.10`–`6`, `jsdom@5.6.1`, `grunt-jscs@2.1.0`; `"es3": true` and `53` IE `// Support:` workarounds inflate bundle size (`286.6 KiB`) and hinder audits. |
| **R8** | Sloppy-mode execution & silent error swallowing | **Low** | Diagnostics | `src/intro.js:40-44`<br>`src/ajax.js:272-282`<br>`src/ajax/xhr.js:217-227` | `"use strict"` is disabled globally (`#13335`); `ajaxConvert()` triggers `TypeError` on `undefined(response)` as control flow; XHR creation uses empty `catch (e) {}` blocks. |

---

## 2. Detailed Risk Notes & Mitigation Priorities

### High Severity (Immediate Remediation / Containment)

- **R1 — DOM XSS (`htmlPrefilter` / `buildFragment` / `parseHTML`):**
  - *Impact:* Passing user-controlled strings to `$()`, `.html()`, `.append()`, or `$.parseHTML()` allows script or event-handler execution even when `<script>` removal is expected (`parseHTML` removes `<script>` nodes *after* `tmp.innerHTML` has already parsed the markup).
  - *Mitigation:* Upgrade to jQuery `3.5.0+` (or `4.x`), avoid passing untrusted HTML into DOM sinks, and sanitize inputs with DOMPurify before insertion.

- **R2 — Prototype Pollution (`jQuery.extend`):**
  - *Impact:* Applications merging parsed JSON or query-string objects with `$.extend(true, target, input)` are vulnerable to polluting `Object.prototype` properties across the runtime.
  - *Mitigation:* Guard against `"__proto__"`, `"constructor"`, and `"prototype"` keys before recursive merge, or replace `$.extend(true, ...)` with safe `Object.assign` / structured cloning (`structuredClone`).

- **R3 — Auto-Eval AJAX & CSP Incompatibility:**
  - *Impact:* An endpoint returning `Content-Type: application/javascript` to a `$.ajax(url)` call without an explicit `dataType` triggers `globalEval()` automatically. Additionally, `window.eval` / `execScript` and `Function("return " + str)` violate strict `script-src` CSP headers.
  - *Mitigation:* Always specify explicit `dataType` (e.g., `"json"` or `"text"`) in `$.ajax()` calls, disallow `jsonp`/`script` auto-conversion for untrusted URLs, and migrate to `fetch()` + `JSON.parse()`.

### Medium Severity (Planned Refactoring & Upgrade Path)

- **R4 — Non-Standard `jQuery.Deferred` Semantics:**
  - *Impact:* Refactoring async code toward native `Promise` / `async`–`await` can introduce subtle timing and error-handling regressions because `1.12.4` `.then()` does not catch thrown errors and runs resolved callbacks synchronously.
  - *Mitigation:* Wrap `$.Deferred` boundaries with `Promise.resolve(...)` adapters during migration and audit all `.then()`/`.fail()` chains for synchronous throw assumptions.

- **R5 — Shared Mutable State & Module Coupling:**
  - *Impact:* Modifying `data.js`, `event.js`, or `manipulation.js` carries high regression risk because internal flags (`globalEval`, `events`, `fx` queues) live in a shared `jQuery.cache` expando store and `src/event.js` mutates `event` objects in place.
  - *Mitigation:* Isolate legacy jQuery usage behind facade modules in consuming apps; avoid custom patches to `src/data.js` or `src/event.js` without running the full `test/unit/` QUnit suite.

- **R6 — Regex Bundler & Untested Custom Exclusions:**
  - *Impact:* Building stripped-down custom bundles (e.g., excluding `deferred` without also excluding `ajax`, `effects`, and `core/ready`) yields silently broken builds (`README.md:93`).
  - *Mitigation:* Ship only the full tested build or migrate module bundling to an AST-based bundler (Rollup/esbuild) if custom treeshaking is required.

- **R7 — EOL Toolchain & Legacy IE Bloat:**
  - *Impact:* Automated CI builds and security scanners fail on modern Node.js LTS due to `jsdom@5.6.1`, `grunt@0.4.5`, and unmaintained `jscs`; ES3 restrictions prevent modern static analysis and syntax modernization.
  - *Mitigation:* Isolate legacy builds in containerized/pinned Node environments only as a temporary bridge while planning migration off the `1.x` branch.

### Low Severity (Hygiene & Observability)

- **R8 — Sloppy Mode & Silent Error Paths:**
  - *Impact:* Commented-out `"use strict"` (`src/intro.js:44`), empty `catch` blocks (`src/ajax/xhr.js:217-227`), and `ajaxConvert()` using `conv(response)` when `conv` is `undefined` obscure root causes during production debugging.
  - *Mitigation:* Add explicit `if (!conv)` guards in conversion code and re-enable strict mode once legacy ASP.NET `arguments.caller.callee` dependencies are retired.
