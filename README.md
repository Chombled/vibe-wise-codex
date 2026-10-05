<img src=".claude-plugin/icon.svg" alt="VibeWise brain with code brackets" width="96" height="96">

# VibeWise

**You build. AI writes.**

A plugin for Claude Code and local Codex desktop and CLI that puts learning first and keeps you in control while AI writes the code you designed. Your assistant **asks for your approach first**, helps you examine tradeoffs, and explains unfamiliar concepts. You shape the design and decide when it's ready to implement. The assistant writes the code, then explains what it changed and why.

For anyone who wants to learn as they build—whether you're an aspiring engineer, a junior developer, or an experienced engineer exploring an unfamiliar stack. Practice planning how the pieces fit together, anticipating failures, and checking the result while keeping ownership of the decisions.

This fork extends [Noah Kim's VibeWise](https://github.com/nykooi1/vibe-wise)
with Codex support. Both hosts use the same skills and local learning notes.

## Get started

You need Claude Code or a local Codex desktop/CLI installation, and
[Python 3](https://www.python.org/downloads/). VibeWise uses Python to restore
learning context and reset learning notes. No extra Python packages are needed.

### Claude Code

Install this fork in [Claude Code](https://code.claude.com/docs/en/setup)
through its GitHub marketplace:

Run these commands **one at a time** in Claude Code. First, add the marketplace:

```text
/plugin marketplace add Chombled/vibe-wise-codex
```

After it finishes, install the plugin:

```text
/plugin install vibe-wise@vibe-wise
```

**Enable automatic updates:** open `/plugin` → **Marketplaces** → **vibe-wise** →
**Enable auto-update**. This is off by default for third-party marketplaces.

Restart Claude Code in the project you want to work on, then run:

```text
/vibe-wise:learn
```

### Codex desktop and CLI

To test the Codex extension before publishing it, install from your local
checkout. Run these commands one at a time in your terminal, replacing the path
with your checkout's absolute path:

```sh
codex plugin marketplace add /absolute/path/to/vibe-wise-codex
codex plugin add vibe-wise@vibe-wise-codex
```

After the 0.1.44 changes are committed and pushed to the fork, GitHub installation
uses:

```sh
codex plugin marketplace add Chombled/vibe-wise-codex
codex plugin add vibe-wise@vibe-wise-codex
```

The marketplace name comes from its catalog, not the GitHub repository name.
If the first GitHub command reports `Added marketplace vibe-wise`, it fetched
the older Claude-only catalog. `vibe-wise@vibe-wise` selects that older release;
use the local checkout above to test the Codex changes instead.
The same repository marketplace exposes the plugin in the desktop Plugins
directory, under **VibeWise for Codex**, where you can install or enable it.
Restart Codex after installation and start a new chat in your project.

Review and trust the bundled session hook before expecting automatic restoration.
In the CLI, use `/hooks`; installing the plugin alone does not trust its hook.
If your desktop client doesn't offer hook review, review it through the CLI
using the same local Codex configuration, then start a new desktop chat.
Hook changes after an update need another review.
[Codex hook trust](https://learn.chatgpt.com/docs/hooks)

In the CLI, open `/skills` or type `$` and select **VibeWise Learn**. In desktop,
select the plugin's **VibeWise Learn** skill in the composer. Use **VibeWise Reset**
when you explicitly want to back up notes and restart onboarding.
Learn and Reset require explicit invocation; an ordinary build request does not
turn learning mode on in a fresh project.

Setup asks one question at a time. Use the native picker when available; otherwise
answer in chat. Pick **Use defaults** to skip preference setup. Then ask your
assistant to build something. Starting fresh or joining an unfamiliar repository
both work. For an existing repository, the assistant first inspects the code and
sketches a small system map. A preselected option or silence never approves a step.

Automatic restoration needs an enabled, trusted hook. If it hasn't been trusted,
you can still invoke Learn explicitly to reload saved notes. This extension targets
local desktop and CLI use; ordinary ChatGPT chat and cloud-only execution are outside
its verified scope.

## What it feels like

You're building a Notion-style notes app: users sign in, create and edit private
notes, and organize them into folders. Here, you're working through how notes and
folders relate—and what should happen when someone deletes a folder.

This condensed example is adapted from a real learning session. Later implementation
steps are illustrative; intervening design discussions are omitted.

**You:**

```text
A note can be in several folders. Deleting a folder should delete its notes.
```

**Claude:**

```text
✦ Build checkpoint: Deleting a shared note

"Trip ideas" is in both Travel and Summer. Deleting it removes it from both.

When someone deletes Travel, what should happen to that note in Summer?
```

**You:**

```text
Keep it in Summer. If it has no folders left, keep the note outside any folder.
```

**Claude:**

```text
That separates deleting a folder from deleting a note.

✦ Build checkpoint: Connecting notes and folders

How would you represent which folders a note belongs to, without copying the note?
```

**You:**

```text
A links table with note_id and folder_id. Deleting a folder removes its links,
not the notes.
```

**Claude:**

```text
Each link records one membership. Several links can point to the same note;
a note with no links is unfiled.

notes ← folder links → folders

✦ Design checkpoint: Folder membership

Proposed: store notes once and track folder membership in a links table.
Deleting a folder removes its links and keeps the notes. This supports multiple
folders per note; loading a folder's notes needs a lookup through those links.

Confirming records this design. We still need to work through access rules
and technology choices before writing code.

❯ 1. Confirm and continue
     This approach makes sense to me; move to the next piece.
  2. Discuss
     Ask questions or clarify anything that doesn't make sense before deciding.
```

**You:**

```text
Confirm and continue.
```

*Later, after the remaining choices for this step are worked through...*

**Claude:**

```text
✦ Implementation checkpoint: Folder membership

I'll add the agreed tables and folder-deletion operation, then test that deleting
a folder preserves its notes and their membership in other folders.
This step builds storage behavior; the UI comes later.

❯ 1. Implement this step
     This approach makes sense to me; write the code for this step.
  2. Discuss
     Ask questions or clarify anything that doesn't make sense before deciding.
```

**You:**

```text
Implement this step.
```

*Claude writes the code and runs the tests.*

**Claude:**

```text
✦ Implementation report: Folder membership

- Added the schema migration: each membership references one note and one folder.
- Added folder deletion: removes the folder and its links, preserving note content.
- Added and ran tests for shared notes and notes left without a folder; both passed.
```

The example above uses Claude Code; Codex follows the same learning loop.
You don't need to know the answer already. Your assistant can explain unfamiliar concepts, sketch the relevant pieces, and help you tackle a smaller question. You stay involved in forming the plan. Answer in plain English; ask for more help or say “skip” whenever you want.

Describing what you want sets the requirements. Build Checkpoints ask you to work
out how it should function; a feature preference doesn't approve an architecture.

| Checkpoint | What happens |
| --- | --- |
| **Build** | You reason through how to approach the problem with your assistant. |
| **Design** | Review the design. **Confirm and continue** records it and continues planning; no code yet. |
| **Implementation** | Review the specific code changes. **Implement this step** authorizes the assistant to make them. |

These aren't three mandatory stops. When ready to code, the Implementation
checkpoint also confirms the design, skipping a separate Design checkpoint.
Both confirmations offer **Discuss** to ask questions, clarify anything confusing,
or explore alternatives before deciding.

When the assistant proposes additional implementation details, it separates them from your
decisions in a short list or table explaining each addition and why it matters.
You can question or change any item before proceeding.

After implementation, the assistant briefly explains what changed, how the key code works,
why it fits your decision, any tests it added or updated and what they cover, and
which checks ran with their results. Ask to dig deeper anywhere it's unclear.

Small diagrams help you trace data, understand relationships, and see how the system fits together.

## Make it yours

Experience changes the support you get, not your ownership of decisions:

| Level | Teaching approach |
| --- | --- |
| Beginner | Explain unfamiliar pieces, use diagrams, ask smaller reasoning questions. |
| Intermediate | Less introductory context; explore interactions and tradeoffs. |
| Advanced | Probe difficult constraints, failure modes, and design assumptions. |

Everyone reasons first. The assistant adapts to what you demonstrate and how familiar you
are with the stack. Checkpoint frequency—Light, Normal, or Frequent—is separate.

- “Use fewer checkpoints.”
- “Focus on backend architecture.”
- “Use multiple-choice questions.”
- “Just implement this one.”
- “Pause learning.” Resume by invoking VibeWise Learn (`/vibe-wise:learn` in Claude Code).

Preferences, learning notes, and a project map live in `.vibe-wise/` in your project. Learning mode resumes in future sessions and after compaction. Add `.vibe-wise/` to your `.gitignore` to keep your notes out of Git; the plugin won't change it silently.

Claude Code and Codex share these notes when you switch assistants, including
preferences and pending approvals. Switching or restarting is not implementation
approval. Existing `.sensible-vibes/` notes continue to work without migration.
Use one assistant at a time for a project's notes; concurrent writes are not coordinated.

No extra account, backend, or telemetry. Saved notes are processed by the active
assistant under your normal Claude Code or Codex data settings.

To start learning this project from scratch, invoke VibeWise Reset
(`/vibe-wise:reset` in Claude Code). It shows the
project and asks **Cancel / Reset learning**. After confirmation, it backs up your
profile, progress, and project map inside the notes directory's `backups/` folder,
then restarts onboarding. Source code and other projects stay untouched. To change
your experience level or preferences, just tell your assistant; no reset is needed.

## Updating

### Claude Code

For automatic updates, open `/plugin` → **Marketplaces** → **vibe-wise** →
**Enable auto-update**. Auto-update is off by default for third-party marketplaces.
Claude Code notifies you after an update; restart Claude Code to load the new version.

To update manually, run these in your terminal:

```sh
claude plugin marketplace update vibe-wise
claude plugin update vibe-wise@vibe-wise
```

Then restart Claude Code. Your project learning notes stay intact; no reset is needed.
Run `claude plugin list` to check the installed version.
[More about plugin updates](https://code.claude.com/docs/en/discover-plugins#keep-plugins-updated).

### Codex

Refresh the marketplace and install the current version:

```sh
codex plugin marketplace upgrade vibe-wise-codex
codex plugin add vibe-wise@vibe-wise-codex
```

Restart Codex, review any changed hook definition, and use
`codex plugin list --marketplace vibe-wise-codex` to check the installed version.
Your project notes stay intact. For local development, refresh the local marketplace
and reinstall after editing; Codex runs the installed cached copy, not your checkout.
[Codex plugin packaging and marketplaces](https://developers.openai.com/plugins/build/plugins)

## License

[MIT](LICENSE). You can use, modify, and share this software, including commercially. Keep the license notice with copies. The software comes without a warranty.
