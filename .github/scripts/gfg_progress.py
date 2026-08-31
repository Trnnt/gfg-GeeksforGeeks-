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

    ratio = min(total / target, 1)

    filled = round(ratio * width)

    return (
        "█" * filled
        + "░" * (width - filled)
    )


def replace_section(
    text,
    start_marker,
    end_marker,
    replacement
):

    if start_marker not in text:
        return text

    if end_marker not in text:
        return text

    start = text.index(start_marker)

    end = (
        text.index(end_marker)
        + len(end_marker)
    )

    return (
        text[:start]
        + replacement
        + text[end:]
    )


def update_readme(stats):

    readme = ROOT / "README.md"

    text = readme.read_text(
        encoding="utf-8"
    )

    total = stats["total"]

    _, level, target = get_level(total)

    xp = total * 10

    if target is None:

        target_display = total
        next_level = "MAX LEVEL 🏆"

    else:

        target_display = target

        next_level = (
            f"{target - total} more problems"
        )

    bar = progress_bar(
        total,
        target
    )

    stats_block = "\n".join([
        "<!-- GFG_STATS_START -->",
        "| Difficulty | Solved |",
        "| ---------- | -----: |",
        f"| 🟢 Basic | {stats['easy']} |",
        f"| 🟡 Intermediate | {stats['medium']} |",
        f"| 🔴 Hard | {stats['hard']} |",
        f"| **Total** | **{total}** |",
        "<!-- GFG_STATS_END -->"
    ])

    text = replace_section(
        text,
        "<!-- GFG_STATS_START -->",
        "<!-- GFG_STATS_END -->",
        stats_block
    )

    journey_lines = [
        "<!-- DSA_JOURNEY_START -->",
        "",
        "## 🧠 DSA Journey",
        "",
        f"### {level}",
        "",
        "```text",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        bar,
        f"{total} / {target_display}",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
        "📚 Problems",
        "",
        f"   🟢 Basic          {stats['easy']}",
        f"   🟡 Intermediate   {stats['medium']}",
        f"   🔴 Hard           {stats['hard']}",
        "",
        "⚡ XP",
        "",
        f"   {xp} XP",
        "",
        "🎯 Next Level",
        "",
        f"   {next_level}",
        "```",
        "",
        "<!-- DSA_JOURNEY_END -->"
    ]

    journey_block = "\n".join(
        journey_lines
    )

    if (
        "<!-- DSA_JOURNEY_START -->"
        in text
        and
        "<!-- DSA_JOURNEY_END -->"
        in text
    ):

        text = replace_section(
            text,
            "<!-- DSA_JOURNEY_START -->",
            "<!-- DSA_JOURNEY_END -->",
            journey_block
        )

    else:

        marker = "## 🐍 GFG Solution Snake"

        if marker in text:

            text = text.replace(
                marker,
                journey_block
                + "\n\n"
                + marker,
                1
            )

    readme.write_text(
        text,
        encoding="utf-8"
    )


def path_points(
    count,
    width=900,
    height=220
):

    if count <= 0:
        return []

    cols = min(
        12,
        max(
            5,
            math.ceil(
                math.sqrt(count)
            )
        )
    )

    rows = math.ceil(
        count / cols
    )

    left = 70
    right = width - 70

    top = 105
    bottom = height - 20

    points = []

    for row in range(rows):

        if rows == 1:

            y = top

        else:

            y = (
                top
                + (bottom - top)
                * row
                / (rows - 1)
            )

        xs = [
            left
            + (right - left)
            * col
            / max(cols - 1, 1)

            for col in range(cols)
        ]

        if row % 2:

            xs.reverse()

        for x in xs:

            if len(points) >= count:
                break

            points.append(
                (x, y)
            )

    return points


def write_svg(total):

    ASSETS.mkdir(
        parents=True,
        exist_ok=True
    )

    width = 900
    height = 280

    points = path_points(
        total
    )

    dots = "".join(
        f'<circle cx="{x:.1f}" '
        f'cy="{y:.1f}" '
        f'r="7" '
        f'fill="#22c55e"/>'

        for x, y in points
    )

    body_points = points[
        max(
            0,
            len(points) - 10
        ):
    ]

    body = "".join(
        f'<circle cx="{x:.1f}" '
        f'cy="{y:.1f}" '
        f'r="{max(5, 12 - i * 0.7):.1f}" '
        f'fill="#14b8a6"/>'

        for i, (x, y)
        in enumerate(body_points)
    )

    if points:

        head_x, head_y = points[-1]

    else:

        head_x = 70
        head_y = 160

    svg = f"""<svg
xmlns="http://www.w3.org/2000/svg"
width="{width}"
height="{height}"
viewBox="0 0 {width} {height}">

<rect
width="100%"
height="100%"
rx="18"
fill="#0d1117"/>

<text
x="40"
y="38"
fill="#f0f6fc"
font-family="Arial"
font-size="22"
font-weight="bold">

🐍 GFG Solution Snake

</text>

<text
x="40"
y="64"
fill="#8b949e"
font-family="Arial"
font-size="13">

Each green node represents one GFG solution.

</text>

<rect
x="30"
y="80"
width="840"
height="165"
rx="15"
fill="#161b22"
stroke="#30363d"/>

{dots}

{body}

<circle
cx="{head_x:.1f}"
cy="{head_y:.1f}"
r="14"
fill="#2dd4bf"
stroke="#d1fae5"
stroke-width="2"/>

<circle
cx="{head_x + 4:.1f}"
cy="{head_y - 4:.1f}"
r="2"
fill="#0d1117"/>

<text
x="40"
y="268"
fill="#8b949e"
font-family="Arial"
font-size="12">

Solutions tracked: {total}

</text>

</svg>
"""

    (
        ASSETS
        / "gfg-solution-snake.svg"
    ).write_text(
        svg,
        encoding="utf-8"
    )


def write_gif(total):

    from PIL import Image, ImageDraw

    ASSETS.mkdir(
        parents=True,
        exist_ok=True
    )

    width = 900
    height = 280

    points = path_points(
        total
    )

    frames = []

    frame_count = max(
        1,
        len(points)
    )

    for head_index in range(
        frame_count
    ):

        image = Image.new(
            "RGB",
            (width, height),
            "#0d1117"
        )

        draw = ImageDraw.Draw(
            image
        )

        draw.rounded_rectangle(
            (30, 80, 870, 245),
            radius=15,
            fill="#161b22",
            outline="#30363d"
        )

        draw.text(
            (40, 18),
            "GFG Solution Snake",
            fill="#f0f6fc"
        )

        draw.text(
            (40, 45),
            "Green dots = GFG solutions",
            fill="#8b949e"
        )

        for x, y in points:

            r = 7

            draw.ellipse(
                (
                    x - r,
                    y - r,
                    x + r,
                    y + r
                ),
                fill="#22c55e"
            )

        if points:

            start = max(
                0,
                head_index - 10
            )

            trail = points[
                start:
                head_index + 1
            ]

            for i, (x, y) in enumerate(
                trail
            ):

                r = max(
                    5,
                    int(12 - i * 0.7)
                )

                draw.ellipse(
                    (
                        x - r,
                        y - r,
                        x + r,
                        y + r
                    ),
                    fill="#14b8a6"
                )

            hx, hy = points[
                head_index
            ]

            r = 14

            draw.ellipse(
                (
                    hx - r,
                    hy - r,
                    hx + r,
                    hy + r
                ),
                fill="#2dd4bf",
                outline="#d1fae5",
                width=2
            )

            draw.ellipse(
                (
                    hx + 2,
                    hy - 6,
                    hx + 5,
                    hy - 3
                ),
                fill="#0d1117"
            )

        draw.text(
            (40, 258),
            f"Solutions tracked: {total}",
            fill="#8b949e"
        )

        frames.append(
            image
        )

    frames[0].save(
        ASSETS
        / "gfg-solution-snake.gif",
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0
    )


def main():

    stats = scan_problems()

    print(
        "GFG Statistics:",
        stats
    )

    update_readme(
        stats
    )

    write_svg(
        stats["total"]
    )

    write_gif(
        stats["total"]
    )


if __name__ == "__main__":

    main()
