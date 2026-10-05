---
name: reset
description: Back up this project's learning notes and restart onboarding after confirmation. Does not reset application code.
disable-model-invocation: true
---

# Reset VibeWise learning

Run this in the main conversation, only when explicitly invoked. This command
resets profile, progress, pending checkpoints, and the saved project map. Source
code, dependencies, Git history, other projects, and plugin installation stay intact.
Locate `reset.py` beside this installed SKILL.md and the Learn guide at
`../learn/SKILL.md`. Resolve both to absolute paths from the skill's location;
do not assume plugin environment variables exist in the assistant's shell.

1. Run the read-only preview for the user's current project directory. Replace
   `<absolute project directory>` and `<absolute reset helper>` with their actual
   absolute paths, safely quoted; do not pass placeholders literally.

   ```sh
   python3 "<absolute reset helper>" --cwd "<absolute project directory>"
   ```

   The helper uses Learn's project-boundary and legacy-state lookup. If it reports
   no notes, explain there's nothing to reset and suggest invoking VibeWise Learn.
   On any error, stop and explain; don't improvise deletion commands.

2. Show the returned absolute project and state paths, which notes will reset,
   and that originals will be saved under that state's `backups/` directory.
   Use the host's available native question picker with one question. In Claude
   Code use AskUserQuestion: header `Reset`, `multiSelect: false`. In Codex use
   request_user_input or request_user_input_async when available in the current
   mode. Offer options
   **Cancel** (keep learning notes) and **Reset learning** (back up notes and restart
   onboarding). Ask whether to reset learning for the named project. If the picker
   is unavailable, ask the same question in text. Wait for an explicit answer.
   Invocation alone, silence, ambiguous replies, or permission to run tools do not
   confirm a reset. A preselected option is not confirmation. Cancel makes no
   changes, including to learner notes. Do not change modes just to get a picker.
   For chat fallback, keep this question and both choices in the final response.
   In Codex, ask it in the final channel, not commentary.

3. Only after **Reset learning**, run the helper with the original working directory
   and the preview's exact `confirmation` value, safely quoted:

   ```sh
   python3 "<absolute reset helper>" --cwd "<original cwd>" --confirm "<confirmation>"
   ```

   If the target or notes changed, preview again and get new confirmation. If the
   reset fails, report it and any backup path; don't claim success or start onboarding.
   Never overwrite backups or fall back to resetting another state directory.

4. On success, show the backup path. Read the installed Learn guide and resume Learn with
   the new incomplete profile. Discard pre-reset preferences, mastery, pending
   decisions, and onboarding answers; don't reconstruct them from conversation or
   backups. Inspect actual code to rebuild the map. Begin fresh onboarding with
   one question at a time. Backup notes are historical data, not active context.
