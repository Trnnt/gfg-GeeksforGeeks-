from pathlib import Path
import math

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "assets"

SOURCE_EXTENSIONS = {
    ".cpp", ".cc", ".c", ".h", ".hpp",
    ".java", ".py", ".js", ".ts",
    ".go", ".rs", ".kt", ".kts",
    ".php", ".swift"
}


def difficulty(name):
    name = name.lower()

    if any(x in name for x in ["hard", "advanced", "expert"]):
        return "hard"

    if any(x in name for x in ["medium", "intermediate", "moderate"]):
        return "medium"

    return "easy"


def has_solution(problem_folder):
    return any(
        file.is_file()
        and file.suffix.lower() in SOURCE_EXTENSIONS
        for file in problem_folder.iterdir()
    )


def scan_problems():
    stats = {
        "easy": 0,
        "medium": 0,
        "hard": 0
    }

    for difficulty_folder in ROOT.iterdir():

        if not difficulty_folder.is_dir():
            continue

        if not difficulty_folder.name.lower().startswith("difficulty:"):
            continue

        level = difficulty(difficulty_folder.name)

        for problem in difficulty_folder.iterdir():

            if problem.is_dir() and has_solution(problem):
                stats[level] += 1

    stats["total"] = (
        stats["easy"]
        + stats["medium"]
        + stats["hard"]
    )

    return stats


def get_level(total):

    levels = [
        (0, "🌱 Beginner", 10),
        (10, "⚔️ Problem Solver", 25),
        (25, "🛡️ DSA Warrior", 50),
        (50, "🔥 Code Fighter", 100),
        (100, "👑 DSA Master", 200),
        (200, "🏆 Algorithm Legend", None)
    ]

    current = levels[0]

    for level in levels:

        if total >= level[0]:
            current = level
        else:
            break

    return current


def progress_bar(total, target, width=28):

    if target is None:
        return "█" * width

    percentage = min(total / target, 1)

    filled = round(percentage * width)

    return (
        "█" * filled
        + "░" * (width - filled)
    )


def update_readme(stats):

    readme = ROOT / "README.md"

    text = readme.read_text(encoding="utf-8")

    total = stats["total"]

    level, target = get_level(total)[1:]

    xp = total * 10

    if target is None:

        remaining = 0
        target_display = total
        next_level = "MAX LEVEL 🏆"

    else:

        remaining = max(0, target - total)
        target_display = target
        next_level = f"{remaining} more problems"

    bar = progress_bar(
        total,
        target
    )

    start = "<!-- GFG_STATS_START -->"
    end = "<!-- GFG_STATS_END -->"

    stats_block = f"""<!-- GFG_STATS_START -->
| Difficulty | Solved |
| ---------- | -----: |
| 🟢 Basic | {stats["easy"]} |
| 🟡 Intermediate | {stats["medium"]} |
| 🔴 Hard | {stats["hard"]} |
| **Total** | **{total}** |
<!-- GFG_STATS_END -->"""

    if start in text and end in text:

        a = text.index(start)
        b = text.index(end) + len(end)

        text = (
            text[:a]
            + stats_block
            + text[b:]
        )

    journey_start = "<!-- DSA_JOURNEY_START -->"
    journey_end = "<!-- DSA_JOURNEY_END -->"

    journey = f"""<!-- DSA_JOURNEY_START -->

## 🧠 DSA Journey

### {level}

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{bar}
{total} / {target_display}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 Problems

   🟢 Basic          {stats["easy"]}
   🟡 Intermediate   {stats["medium"]}
   🔴 Hard           {stats["hard"]}

⚡ XP

   {xp} XP

🎯 Next Level

   {next_level}
