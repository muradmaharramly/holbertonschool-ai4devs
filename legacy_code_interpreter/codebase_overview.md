# Codebase Overview — jQuery 1.12.4 (Legacy `1.x` Branch)

## 1. Project Identity & Scope

| Attribute | Value |
| :--- | :--- |
| **Target Codebase** | [jQuery](https://github.com/jquery/jquery) (`1.x` legacy branch) |
| **Analyzed Snapshot** | Tag `1.12.4` (commit `f55d0ec8f28d648ac6429d03f1e2102d85912e86`) |
| **Primary Language** | JavaScript (ES3-constrained; `src/.jshintrc` enforces `"es3": true`) |
| **License** | MIT (`LICENSE.txt`) |
| **Role of `1.12.4`** | Final release on the `1.x` line supporting legacy browsers (IE6–8, Android 2.3); the `2.x`+ branch dropped IE6–8 and added non-browser/Node support. |

---

## 2. Age & Maintenance History

- **Initial Commit:** `2006-03-22` (`8a4a1edf047f2c272f663866eb7b5fcd644d65b3` by John Resig — *"Inital Import."*).
- **Snapshot Release Date (`1.12.4`):** `2016-05-20` (commit `f55d0ec8` by Timmy Willison).
- **Overall Age:** **~20.6 years** since initial import (mainline repository remains active as of `2026-11-02`, tag `4.0.0-60-gfeaa9fcd`).
- **Frozen Legacy Age:** The `1.12.4` legacy branch snapshot has been unmaintained for **~10.5 years** since its May 2016 release.
- **Scale of History (up to `1.12.4`):** `5,869` commits across `263` listed contributors in `AUTHORS.txt`.

---

## 3. Size & Lines of Code (LOC)

Measured directly from tag `1.12.4` checkout:

| Directory / Artifact | `.js` Files | Total Lines | Non-Blank Lines | Notes |
| :--- | ---: | ---: | ---: | :--- |
| `src/` | 95 | 9,494 | 7,775 | Core modular AMD-wrapped library source |
| `build/` | 14 | 972 | 815 | Custom Grunt tasks (excl. root `Gruntfile.js`: 208 lines) |
| `dist/` | 2 | 11,013 | 8,940 | `dist/jquery.js` (11,008 lines, `293,430` B / `286.6 KiB`); `dist/jquery.min.js` (`97,163` B / `94.9 KiB`) |
| `test/unit/` | 24 | 22,157 | — | QUnit unit test modules |
| `test/data/` | 10 | 10,506 | — | Includes `test/data/jquery-1.9.1.js` (9,885 lines, vendored fixture) |
| `test/node_smoke_tests/` + `test/integration/` | 9 | 211 | — | Node smoke tests (8 files, 112 lines) & integration (1 file, 99 lines) |
| `external/` | 8 | 13,090 | 11,024 | Vendored/copied assets (`sizzle.js` 2,143; `qunit.js` 2,875; `sinon-1.14.1.js` 5,931; `require.js` 2,076) |

*Total across `test/` (all 45 `.js` files): `32,964` total lines (`26,796` non-blank lines), though ~30% of that total is the single `jquery-1.9.1.js` fixture.*

### Largest `src/` Modules & Subsystems

| Module / Subsystem | Files | Total Lines | Primary Responsibility |
| :--- | ---: | ---: | :--- |
| `src/event.js` (+ `src/event/`) | 4 | 1,207 | Event normalization, delegation, custom/special events, shorthand aliases |
| `src/ajax.js` (+ `src/ajax/`) | 10 | 1,444 | `$.ajax`, XHR/ActiveX transport, JSONP, script transport, `parseJSON`/`parseXML` |
| `src/manipulation.js` (+ `src/manipulation/`) | 13 | 954 | DOM insertion, cloning, `htmlPrefilter`, script evaluation tracking |
| `src/css.js` (+ `src/css/`) | 13 | 1,183 | Computed style shims, `cssHooks`, visibility/opacity workarounds |
| `src/attributes/` (+ `src/attributes.js`) | 6 | 883 | Attribute/property/class/value normalization across old IE |
| `src/effects.js` (+ `src/effects/`) | 4 | 832 | Animation loop, `Tween`, easing, `show`/`hide` |
| `src/core.js` (+ `src/core/`) | 6 | 943 | `jQuery()` constructor, `extend`, `each`, `globalEval`, `ready` |
| `src/data.js` (+ `src/data/`) | 3 | 385 | Element-to-cache expando mapping (`jQuery.cache`) |
| `src/deferred.js` & `src/callbacks.js` | 2 | 391 | Pre-Promises/A+ async primitives (`$.Deferred`, `$.Callbacks`) |

---

## 4. Dependencies & Toolchain

### Runtime Dependencies
- **`package.json` `dependencies`:** `{}` (zero npm runtime dependencies).
- **Bundled Selector Engine:** `sizzle` `2.2.1` (`external/sizzle/dist/sizzle.js`, 2,143 lines) is concatenated directly into `dist/jquery.js` by the build task (`src/selector-sizzle.js`). Unlike the `2.x`+ branch, **excluding Sizzle is unsupported on `1.x`** (`README.md`).

### Build, Lint & Test `devDependencies` (`package.json`)
- **Build & Bundling:** `grunt` (`0.4.5`), `grunt-cli` (`0.1.13`), `requirejs` (`2.1.17`), `grunt-contrib-uglify` (`0.9.2`), `grunt-npmcopy` (`0.1.0`), `grunt-babel` (`5.0.1`, used only for `test/node_smoke_tests/lib/ensure_iterability_es6.js`), `core-js` (`0.9.17`).
- **Static Analysis & Style:** `grunt-contrib-jshint` (`0.11.2`), `grunt-jscs` (`2.1.0` — deprecated/archived upstream), `grunt-jsonlint` (`1.0.4`), `commitplease` (`2.0.0`).
- **Testing & CI:** `qunitjs` (`1.17.1`), `qunit-assert-step` (`1.0.3`), `sinon` (`1.12.2` in `package.json`; `1.14.1` checked into `external/sinon/`), `jsdom` (`5.6.1`), `testswarm` (`1.1.0`).
- **CI Runtime Matrix (`.travis.yml`):** Node.js `0.10`, `0.12`, `4`, `5`, `6` and `npm` `2.1.12`.

---

## 5. Known Issues, Technical Debt & Pain Points

### 1. ES3 Language Lock-In & Disabled Strict Mode
- `src/.jshintrc` enforces `"es3": true`, `"evil": true`, and `"sub": true` because target browsers (IE < 10, Android < 4.1) fail ES5 conformance. Contributors cannot use `const`/`let`, ES5 array/object methods natively without internal shims, or ES modules.
- `src/intro.js` (lines 40–44) explicitly comments out `"use strict";` because legacy ASP.NET and third-party libraries walk call stacks via `arguments.caller.callee`, which throws in Firefox 18+ if strict-mode frames are present (ticket `#13335`). The entire `dist/jquery.js` bundle runs in sloppy mode.

### 2. Pervasive Legacy Browser Workarounds (IE6–8)
- `src/` contains **79** `// Support:` annotations, of which **53 (`67.1%`)** address Internet Explorer behaviors:
  - `src/ajax/xhr.js`: Falls back to `new window.ActiveXObject("Microsoft.XMLHTTP")` for IE6–8 and local file access, normalizes IE status code `1223` to `204`, and hooks `window.attachEvent("onunload", ...)` to manually abort open XHRs in IE < 10 (`#5280`).
  - `src/data.js`: Splits DOM node vs. plain JS object caching (`jQuery.cache` with numeric expando IDs and `deletedIds` recycling) solely because IE6–7 cannot garbage-collect circular references across the DOM–JS boundary.
  - `src/manipulation.js`: Injects `<tbody>` for table `<tr>` insertions (IE < 8) and falls back to `outerHTML` parsing in `jQuery.clone()` because IE <= 8 cannot clone detached unknown HTML5 elements (`rnoshimcache`).

### 3. Fragile Regex-Based Custom Build Pipeline
- `build/tasks/build.js` uses RequireJS (`r.js`) purely as a dependency tracer, then runs regex substitutions in `convert()` to strip `define(...)` wrappers, rewrite `src/var/*` modules into local `var` declarations, and delete `/* ExcludeStart */.../* ExcludeEnd */` blocks.
- `README.md` explicitly warns that custom builds (`grunt custom:-module`) are not regularly covered by unit tests due to module combinatorics, and `Gruntfile.js` (`line 32`) deletes `onevar` from JSHint options for `dist/jquery.js` because concatenation breaks single-file lint rules.

### 4. Security & Content Security Policy (CSP) Liabilities
- **DOM XSS Surface (`htmlPrefilter`):** `src/manipulation.js` (lines 33 & 288–290) rewrites self-closing tags via `rxhtmlTag` (`/<(?!area|br|...)(([\w:-]+)[^>]*)\/>/gi` -> `"<$1></$2>"`), a transformation historically associated with HTML-parsing XSS bypasses (fixed only in jQuery 3.5.0+).
- **CSP `'unsafe-eval'` Dependency:** `jQuery.globalEval` (`src/core.js:290-300`) executes scripts via `window.execScript` or `window["eval"].call(window, data)`, which fails under strict CSP policies disallowing `'unsafe-eval'`.
- **Dynamic Function JSON Fallback:** `jQuery.parseJSON` (`src/ajax/parseJSON.js:47`) falls back to `( Function( "return " + str ) )()` after regex token stripping when `window.JSON.parse` is unavailable, and coerces inputs via `data + ""` for Android 2.3 compatibility.

### 5. Non-Standard Async Semantics (`jQuery.Deferred`)
- `src/deferred.js` predates Promises/A+ and ES6 `Promise`:
  - Callbacks registered on already-settled deferreds execute **synchronously** via `jQuery.Callbacks("once memory")`, creating Zalgo/ordering hazards.
  - Exceptions thrown inside `.then()` handlers (`fn.apply(this, arguments)` at line 34) are **not caught** and converted into rejections; they crash the synchronous call stack instead.
  - `.then()` forwards variadic `arguments` rather than standard single-value resolution, complicating migration to native `Promise` / `async`–`await`.

### 6. High Module Coupling & Monolithic Files
- `src/event.js` (1,134 lines) and `src/ajax.js` (842 lines) pack dispatch, browser normalization, and state management into large closures.
- Internal state is tightly coupled across modules through `jQuery._data` / `jQuery.cache` (e.g., `event.js` storing handler arrays on DOM nodes, `manipulation.js` tracking `globalEval` flags via `jQuery._data`, `queue.js` storing queues in private data).
- `src/deprecated.js` retains obsolete APIs (`bind`, `unbind`, `delegate`, `undelegate`, `size`, `andSelf`) that encourage legacy patterns in consumer codebases.

### 7. Obsolete Toolchain & Environment Constraints
- `1.12.4` does not support Node.js / CommonJS without an externally supplied `window` (`README.md`, `src/intro.js:25-32`) and relies on EOL build/test packages (`grunt@0.4.5`, `jsdom@5.6.1`, `grunt-jscs@2.1.0`, `qunitjs@1.17.1`, Node `0.10`–`6` CI targets), increasing friction for modern security audits, CI automation, and regression testing.
