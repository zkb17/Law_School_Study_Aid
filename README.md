# Law Study Hub · Nebraska 2L Edition

A GitHub Pages–ready, local-first law school **study** dashboard. It provides active recall, multiple-choice tests, spaced flashcards, issue spotting, rule recall, and progress analytics. It deliberately **does not write assignments, legal briefs, memos, or course outlines**.

**Independent educational prototype, not affiliated with the University of Nebraska.** Questions summarize general U.S. legal principles and must be checked against current sources and course-specific teaching. Jurisdiction-specific rules and legal developments can differ.

## What's included in this beta

- **70** selectable law school subjects, based on common upper-level topics and Nebraska Law's broad elective curriculum. Not all are required in 2L.
- **804** built-in multiple-choice questions: the original 104 plus **700 newly authored, doctrine-focused questions (10 supplemental per subject)**. Each has four legally real choices and per-choice feedback.
- **128** built-in recall/flashcards, including rules, definitions, and elements.
- **12** multi-select issue-spotting hypotheticals.
- Subject and difficulty filters, timed sessions, optional weak-topic weighting, immediate grading.
- Spaced repetition ratings (Again / Hard / Good / Easy), typed rule recall, topic-level analytics.
- Import from pasted notes, TXT, Markdown, PDF, and DOCX; local extraction of definitions and legal rule statements for practice cards. If the source contains at least four distinct definitions, it also builds local MCQs.
- IndexedDB storage for study state and source text, plus export/import JSON backups.
- Optional server-side AI question generation (requires **separate** Cloudflare Worker setup and an API key; it is not enabled by default).

**Important:** The 700 additions are **independently authored doctrine-identification/application prompts**, not copied commercial exam items. They are not faculty-reviewed, bar-certified, or equivalent to 700 full-length essay-style hypotheticals. Their wrong answers are real competing concepts from the same course, and each explanation says what that alternative addresses. The app links to governing statutes/rules when identifiable and otherwise to an authoritative research starting point; links should not be mistaken for verified pinpoint legal support. Jurisdiction, statute versions, and legal developments can differ.

**Expanded study content files:**
- `expanded-bank.js` loads 700 questions directly into the app (no setup/API necessary).
- `expanded-question-bank.json` contains all 700 new records in portable structured form.
- `expanded-question-bank.csv` makes the entire new bank reviewable in spreadsheet software.
- `concepts.txt` holds 700 authored topic/problem/citation seeds; `build_bank.py` rebuilds the JS/JSON/CSV consistently.
- Existing local study progress and IDs from the previous 104 questions remain intact; the expansion adds new IDs without changing old ones.

**Quality checks performed:** per-subject minimum of 10 new questions, unique IDs/stems, four distinct choices, exactly one keyed answer, one feedback explanation per choice, citation text, HTTPS reference links, course-ID matching, application script parse tests and browser interaction tests. These are mechanical checks plus a manual spot review, **not independent expert verification of every legal answer**.

## Try it locally

Open `index.html` in a modern browser (Chrome, Edge, Firefox, Safari). No installation, build tools, API keys, or account required. You can also serve this directory from any static server.

The core study app and TXT/Markdown/pasted-note imports need no network. To read **PDF** or **DOCX** files, the browser dynamically downloads open-source parsing libraries (PDF.js and Mammoth) from jsDelivr. Internet access is needed when importing those file types. The documents are parsed in the browser; they are not uploaded to a server by this code.

## Host with GitHub Pages — public frontend

1. Create a new GitHub repository (e.g., `law-study-hub`).
2. Upload all of the **root-level site files** (`index.html`, `styles.css`, `app.js`, `data.js`, `cards.js`, `expanded-bank.js`, `favicon.svg`, and this README). Uploading the optional worker folder is fine; GitHub Pages does not execute it.
3. In the GitHub repository, open **Settings → Pages**. Under **Build and deployment → Source**, choose **Deploy from a branch**. Select `main` and `/(root)`, then save.
4. Once published, open `https://YOUR-USERNAME.github.io/law-study-hub/` (replace username and repo name as appropriate).
5. Save this URL as a bookmark. Data is stored **on that browser/device**. The same URL on a different device does **not** share progress.

The GitHub repository and GitHub Pages website can be public, but **do not put uploaded notes, client information, API keys, or backup files in the repository**. They should stay in private, browser-local storage. For a private hosted site, consider a hosting platform with authentication; GitHub Pages alone does not provide login-gated data sync.

## Optional AI-generated practice questions (advanced)

Local generation already works for explicit definitions and rule statements. Richer AI-generated questions from arbitrary course materials require a secure backend endpoint. An example **Cloudflare Worker** is in `optional-ai-worker/`.

1. Have a Cloudflare account, OpenAI API account with billing and permission to use the selected model, and Wrangler CLI.
2. Set `ALLOWED_ORIGIN` in `optional-ai-worker/wrangler.toml` to your GitHub Pages origin. Example: `https://example.github.io` (**origin only**; no repository path).
3. In `optional-ai-worker`, run `npx wrangler secret put OPENAI_API_KEY`, then `npx wrangler secret put STUDY_ACCESS_TOKEN` using **a different strong random secret** for the study endpoint.
4. Deploy with `npx wrangler deploy`.
5. In the hosted dashboard, open **Settings & Backup**, enter your worker HTTPS URL, and save it. When invoking AI generation, enter the *study access token*, not the OpenAI key.
6. Only click **Generate with AI endpoint** on materials the user is authorized to send to that service. The extracted text will be transmitted to your Worker and AI provider. Do not send privileged/confidential client records.

**Production caution:** A public, paid AI endpoint needs additional safeguards: Cloudflare rate limits, monitoring/budget limits, authentication controls, and ideally user-specific access. The example only includes an origin allowlist and shared secret. It is a starting point, not production-grade multiuser security. API responses can be wrong; review generated legal questions before relying on them.

## Local data and backups

The app uses **IndexedDB** if available and falls back to localStorage for lightweight state. Browser storage can be deleted or evicted; use **Settings & Backup → Export all data** regularly. Exported JSON includes study history and all locally saved extracted document text. Treat backups as private. Importing a backup replaces the current state. There is no cloud synchronization in this version.

## Study methods

- **Multiple choice:** four options, immediate result, complete explanation per option, timed practice, prioritized weak concepts.
- **Flashcards:** front/back retrieval, self-rated interval scheduling. The simple scheduling implementation is inspired by spaced repetition, not a certified SM-2 implementation.
- **Rule recall:** answer in free text, reveal verified reference phrasing, and self-evaluate instead of trusting weak automatic semantic grading.
- **Issue spotting:** multi-select common doctrines from a hypothetical and see missing or irrelevant issues.
- **My Materials:** heuristic extraction generates review cards with reference to the source text line/excerpt; optional backend adds document-grounded MCQs and cards.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | Site entry point |
| `styles.css` | Responsive dashboard UI |
| `app.js` | Interactive application, storage and study modes |
| `data.js` | Original 104 questions and subject catalog |
| `expanded-bank.js` | New 700-question dataset loaded into the app |
| `expanded-question-bank.json` | Portable data export of the 700 questions |
| `expanded-question-bank.csv` | Spreadsheet review of question text, answers, feedback and references |
| `QUESTION_BANK_COVERAGE.md` | Course-by-course question counts and quality-method notes |
| `concepts.txt` / `build_bank.py` | Editable authored seeds and reproducible generation script |
| `cards.js` | Flashcards and issue-spotting problems |
| `favicon.svg` | App icon |
| `optional-ai-worker/` | Optional Cloudflare Worker for AI generation |

## Next improvements

- Expanded expert-reviewed question banks for individual subjects and professor-specific sets.
- More varied factual application and mixed issue-spotting question types.
- Automated validity checks and stronger citations for all generated items.
- Interactive doctrinal decision trees.
- Optional authenticated cross-device syncing, ideally with a secure managed backend.
- Full accessibility audit and real-user browser testing.

## Academic references

- [Nebraska Law JD curriculum](https://catalog.unl.edu/law/juris-doctor-jd/)
- [Nebraska Law curriculum](https://law.unl.edu/prospective/curriculum/)
- Federal Rules of Evidence, Federal Rules of Civil Procedure, U.S. Code, ABA Model Rules of Professional Conduct, and the primary cases/statutes cited within individual study questions.
