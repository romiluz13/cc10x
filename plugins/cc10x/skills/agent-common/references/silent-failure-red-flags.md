# Silent Failure Red Flags

## Core Red Flags

| Pattern | Problem | Fix |
| --------- | --------- | ----- |
| `catch (e) {}` | Swallows errors | Add logging + user feedback |
| Log-only catch | User never knows | Add user-facing message |
| "Something went wrong" | Not actionable | Be specific about what failed |
| `\|\| defaultValue` | Masks errors | Check explicitly first |
| `?.` chains without logging | Silent short-circuit | Log when chain short-circuits to null |
| Retry without notification | User unaware of degradation | Notify after retry exhaustion |

## Language-Specific Red Flags

| Language | Pattern | Problem |
| ---------- | --------- | --------- |
| Python | `except Exception: pass` or bare `except:` | Swallows all errors including KeyboardInterrupt |
| Python | `logging.exception()` in a bare except | Logs but never re-raises; caller assumes success |
| Go | `_ = riskyCall()` | Discarded error; caller cannot distinguish success from failure |
| Go | `if err != nil { return nil }` | Error swallowed; upstream receives zero-value as valid |
| Java | `catch (Exception e) { e.printStackTrace(); }` | Log-only; no re-throw or user notification |
| Rust | `.unwrap()` in non-test code | Panics on error instead of propagating |
| Shell | Missing `set -e` or unchecked `$?` | Script continues after command failure |

## Severity Classification

1. Can this cause DATA LOSS or SECURITY breach? → CRITICAL
2. Will USER see broken/wrong behavior? → HIGH
3. Is functionality correct but UX degraded? → MEDIUM
4. Is this style/cleanliness only? → LOW
