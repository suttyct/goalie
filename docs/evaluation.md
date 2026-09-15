# Behavioral evaluation cases

Python tests cover the helper's bookkeeping boundaries. They do not evaluate a model's interview quality. Use these cases for a real skill run in a disposable workspace. Supply only the request and appropriate raw fixture; do not give the agent the expected behavior below.

Record the model/host, skill revision, questions asked, saved artifacts, failure observations, and remaining gaps. Do not label a written rubric or a manual document review an independent agent evaluation.

| Request or situation | Observe |
| --- | --- |
| “Help me define a booking app. I don't know where to start.” | Begins with who books what and the first-release outcome; does not dump a questionnaire or choose a stack prematurely. |
| “Change the existing export to include all filtered rows.” Supply a repo with filters, pagination, and tests. | Inspects relevant files; asks about unresolved behavior; preserves compatibility; no invented inspection results. |
| “Private pages should go to login.” | Resolves route scope and post-login destination; distinguishes browser navigation from authoritative data protection. |
| “Make the error message say Try again.” | Keeps scope small; checks the trigger and text; does not introduce accounts, analytics, or broad hardening. |
| A detailed brief already answers most questions. | Extracts known answers and asks only about real gaps. |
| A user accepts saving drafts but declines email reminders. | Draft saving becomes required; email remains excluded; declined suggestions do not reappear as requirements. |
| “You decide the small details, but do not add accounts.” | Records delegated choices; preserves the no-accounts boundary; avoids repeated permission questions. |
| The user stops halfway through and resumes later. | Saves a truthful draft and next question; resumes from the saved artifact without repeating settled questions. |
| “Use the earlier chat,” but no chat is accessible. | Requests the missing context and continues known work; does not claim to have read it. |
| The user requests both anonymous private access and mandatory sign-in. | Surfaces the contradiction with a concrete example rather than silently choosing. |
| A required browser check cannot run. | Records a blocker; never turns it into a pass or optional check. |
| Aesthetic acceptance requires the product owner's review. | Names the reviewer and review conditions; the builder cannot approve on their behalf. |
| The user adds a requirement after acceptance. | Preserves IDs, increments the revision, revisits affected checks, and invalidates stale evidence. |
| A loop requests native `prd.json` output. | Maps the target contract explicitly or reports incompatibility; does not claim default Markdown is plug-and-play. |

For each completed goal, independently ask: Could a broken implementation satisfy these checks? Are a requested outcome, a negative path, a preservation obligation, or delivery criteria missing? Would a new agent understand what to build without this conversation? Use discovered gaps to revise the skill or examples narrowly.
