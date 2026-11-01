# Proposed instincts from mining Django (D1–D6)

Drafted while mining django/django, round `2026-10-31-a05e16a-mine` (report: `reviews/Django/2026-10-31-a05e16a-mine.md`). Not yet approved. The labels D1–D6 are temporary; if approved, each takes the next free number at the end of `DEV-INSTINCTS.md`, after whichever earlier drafts are approved first.

**How strong the case is.** Django is human-written, so these rows are reference data and don't move the check order. Each draft below had at least three Django rows that fit no approved instinct and no earlier draft. Several also showed up in the same file more than once, or as a regression caused by a fix for an earlier row of the same class, which is the strongest signal the mining procedure has. All evidence is `reading` (upstream says fixed; nothing re-run).

---

#### D1. A shortcut must give the general path's answer (approved as #51, 2026-10-31)
- **Tag:** `proposed:fast-path-matches-slow-path`
- **Instinct:** an optimisation that answers without going through the general path (a count without the join, a bulk insert without save(), a "nothing to alter" skip, an insert that avoids a round trip) must give the same result as the general path for every input the general path accepts.
- **Missed (Django):**
  - DJ-036: `count()`/`exists()` on a many-to-many filtered on `instance.pk` while the full query joins on `to_field`. Every count was 0;
  - DJ-037: admin single-object logging moved onto `bulk_create`, which sends no save signals;
  - DJ-046, DJ-047: an insert-time loop re-implemented `pre_save` with the wrong flag and dropped fields only the database could fill (two regressions from one optimisation);
  - DJ-054: the "only the name changed, nothing to alter" check skipped renaming an M2M table;
  - DJ-044, DJ-074: the PostgreSQL UNNEST bulk-insert path truncated strings (the same bug bulk_update had already fixed), and a fix then disabled the path for every model with a foreign key;
  - DJ-019 (review): a deferred-SQL shortcut returned early and dropped a pending unique constraint.
- **Ask:** what does the general path do that this shortcut doesn't (signals, defaults, casts, joins, renames)? Is there an input where the two answers differ?
- **Prove it:** a differential test. Run the same inputs through the shortcut and through the general path (bulk vs one at a time, optimised vs unoptimised query, skip vs do the work) and assert identical results, side effects and signals. Include `to_field`, nullable, max-length and renamed cases.
- **Checklist:** "Every shortcut is tested against the general path on the same inputs, and the answers match?"

#### D2. Compare and key in canonical form (approved as #48, 2026-10-31)
- **Tag:** `proposed:canonical-form`
- **Instinct:** when one thing has several spellings (name vs attname, `pk` vs the real field, quoted vs unquoted, case, padding, `_` vs `-`), every comparison, lookup and map normalises first. When different things are joined into one key (name + salt, codename without content type), the key must still tell them apart.
- **Missed (Django):**
  - DJ-070, DJ-071: constraint validation registered `field.name` only, and crashed on `author_id`. The fix covered one site, and the second site shipped as a new regression;
  - DJ-030 (review): `selected[0] != unquote(object_id)`, so one side was quoted and the other wasn't;
  - DJ-032 (review), DJ-080 (revert): permission renames keyed by codename alone, or matched by `model__icontains`, hit other models' permissions;
  - DJ-040: selected columns kept in a dict keyed by name, so two selections of one field collapsed;
  - DJ-081 (revert): alias strings tested for membership in a tuple of `Col` objects, so the test never matched;
  - DJ-098, DJ-100, DJ-102, DJ-106 (advisories): `key + salt` signer namespaces collided; `Private` and padded `Vary` tokens slipped past case- and space-sensitive checks; `X_Header` and `X-Header` landed on one META key.
- **Ask:** how many spellings can this name or value have, and does every comparison normalise them the same way? If two different things are joined into a key, can two different pairs produce the same key?
- **Prove it:** for each comparison or map key, a table test over every spelling (case, padding, quoted, attname, `pk`) expecting one result. For each composite key, two different inputs that would concatenate to the same string, expecting different keys.
- **Checklist:** "Every comparison normalises all spellings, and no two different inputs share a key?"

#### D3. Falsy, empty, None and "the database decides" are four different values (approved as #52, 2026-10-31)
- **Tag:** `proposed:falsy-is-not-none`
This extends #4 (missing is not blank) from forms to code.
- **Instinct:** `if x:` asks whether x is truthy, not whether it was given. An empty `Q()`, `0`, `""`, `[]`, `None`, SQL NULL, JSON null and a sentinel like `DatabaseDefault` each mean something different, and each needs its own test.
- **Missed (Django):**
  - DJ-027 (review), DJ-064: an empty `Q()` filter, which is falsy but not None, was turned into None. It was caught in one review and shipped in another place as a crash in admin facets;
  - DJ-042, DJ-043: `None` saved as JSON null instead of SQL NULL; the fix then made a filter condition use SQL NULL where JSON null was meant;
  - DJ-048: the `DatabaseDefault` sentinel read as "pk not set", so the Python default overrode the database's;
  - DJ-052: `srid=None`, which used to crash, became a valid parameter and silently stored NULL;
  - DJ-028, DJ-031 (reviews): a check that handled both-None and neither-None but crashed on one-None; a sentinel handled in one branch of a display function and newly rejected by validation.
- **Ask:** what does each falsy value mean here: empty, zero, None, NULL, JSON null, "not given", "database decides"? Does `if x:` mean the one I intend?
- **Prove it:** a parametrised test over `None`, empty containers, `0`, `False`, an empty `Q()` and every sentinel the code accepts, with a distinct expected result for each.
- **Checklist:** "Every truthiness test was checked against empty, zero, None and each sentinel, and each gives its own result?"

#### D4. An override point is an API (approved as #57, 2026-10-31)
- **Tag:** `proposed:extension-points-are-api`
- **Instinct:** a method subclasses override, a template block projects extend, an attribute third-party code reads, a type someone pickles, and a default that forms rely on are all contracts, documented or not. Changing their signature, call path, return type, name or default breaks code you can't see.
- **Missed (Django):**
  - DJ-051: every query path started calling `from_db(..., fetch_mode=...)`, and every model overriding the documented signature crashed;
  - DJ-038: a bug fix changed `log_actions()`'s signature and return type;
  - DJ-063: a hard-coded required check overrode subclasses' `required=False`;
  - DJ-059: an internal-looking `params` attribute used by a large third-party project was repurposed;
  - DJ-061: a namedtuple's typename differed from its module name, so email messages could no longer be pickled for task queues;
  - DJ-066, DJ-008 (review): the async path skipped subclasses' overridden `process_request()` and sync cache methods;
  - DJ-084 (revert): moving the `object-tools` block broke projects' admin templates.
- **Ask:** who overrides, extends, subclasses, pickles or reads this from outside? Does the change keep their code working, or warn them first?
- **Prove it:** a compatibility test per extension point: a subclass with the old override signature, a template that extends the old block, a pickle round trip, and a third-party-style read of the attribute. Each passes, or gets a deprecation warning, before the old shape is removed.
- **Checklist:** "Every override point, template block, pickled type and widely read attribute the change touches has an old-shape compatibility test?"

#### D5. List every type the value can be (approved as #54, 2026-10-31)
- **Tag:** `proposed:every-type-it-can-be`
- **Instinct:** a "string" argument can arrive as a str subclass (SafeString), a lazy translation proxy, bytes (valid UTF-8 or not), an int, an ipaddress object or None. A check written for one of them (`isinstance(x, str)`, `startswith`, `force_str`) decides wrongly for the others.
- **Missed (Django):**
  - DJ-072: `isinstance(path, str)` also caught SafeString, so `mark_safe` assets were percent-encoded;
  - DJ-055: a route built with `gettext_lazy` failed `str.startswith`;
  - DJ-083 (revert): `hmac.compare_digest` replaced a wrapper that had accepted mixed bytes and str;
  - DJ-057: `force_str` on bytes passwords that were not UTF-8;
  - DJ-002 (review), DJ-062: validators crashed on non-str values after a length guard was added;
  - DJ-053: every `Value` treated as JSON text, though only `Value(..., JSONField())` is;
  - DJ-089 (advisory): a blocklist checked str and dict but let bytes reach a network fetch.
- **Ask:** what types can actually arrive here, from callers, templates, translations and the network? Does this check handle each one the way I mean?
- **Prove it:** a parametrised test feeding each realistic type (str, SafeString, lazy str, UTF-8 bytes, non-UTF-8 bytes, int, None, the domain object) and asserting the intended branch.
- **Checklist:** "Each type check was tested with str subclasses, lazy strings, bytes, None and the domain object?"

#### D6. Don't change what you were handed
- **Tag:** `proposed:dont-mutate-inputs`
- **Instinct:** a function that edits a list, dict or object it was passed, or state owned by the object it is compiling, changes its caller's data. Copy first, or own the data.
- **Missed (Django):**
  - DJ-001 (review): `fields.remove(field)` on the query's own field list during compilation;
  - DJ-007 (review): `filtered_relation.condition = ...` on the caller's FilteredRelation;
  - DJ-067: `attrs["class"] += ...` on the caller's dict, so each call appended the class again.
  - In the same window, two unmerged PRs got the same review comment ("this mutates the queryset in place", "clone it before altering select").
- **Ask:** does this write to anything it didn't create? What happens when the same object is used a second time?
- **Prove it:** call the function twice with the same argument object and assert the argument is unchanged and both results are equal.
- **Checklist:** "Every function leaves its arguments unchanged, proven by calling it twice with the same object?"

---

## Smaller candidates (one or two Django rows each, not drafted)
- An iterator can be read once (DJ-049: `any()` consumed an rhs iterator before its real use). Related: an unmerged PR in the same window had two loops over one exhausted iterator.
- Overwrite truncates (DJ-045: `os.open` for an overwrite with no `O_TRUNC` kept the old tail).
- Cleanup deletes only what it created (DJ-077: a destructor unlinked network rasters once accepted inputs widened).
- A parameter is not a scratch variable (DJ-035: `fields` reassigned in one branch, read later as the caller's).
- Every branch runs once in a test (DJ-011: `connection` undefined in a new loop).
- Every combination of independent switches (DJ-024, DJ-085: format x natural keys; two sidebars at once).
- Position is not identity (DJ-025: `returning_fields[0]` assumed to be the auto field).
- A new warning is tested on the valid cases too (DJ-078: a system check warned that `null` has no effect where it did, and was reverted).
- Denylists grow one character per advisory: the column-alias pattern gained `#` (DJ-123), then control characters (DJ-117), then `$` on PostgreSQL (DJ-119), and a `$` regex anchor repeated a 2021 validator bug (DJ-097). These already fit #9 and #27, so this is a candidate amendment to L9 ("allowlist identifiers") rather than a new draft.
