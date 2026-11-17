"""Style the snake's contribution-style grid with decorative green squares.

Illustrative artwork only; NOT a record of the user's GitHub contributions.
This post-processes generated SVGs while retaining the animated snake.
"""
from pathlib import Path
import re

STYLE = """
.c.decor0{fill:#0e4429}
.c.decor1{fill:#006d32}
.c.decor2{fill:#26a641}
.c.decor3{fill:#39d353}
"""

for path in (
    Path("dist/github-contribution-grid-snake.svg"),
    Path("dist/github-contribution-grid-snake-dark.svg"),
):
    svg = path.read_text(encoding="utf-8")

    def decorate(match):
        x, y = int(match.group(1)), int(match.group(2))
        column, row = (x - 2) // 16, (y - 2) // 16
        # Fill ~75% of empty days; stay deterministic across regenerations.
        value = (column * 37 + row * 43 + column * row * 7 + 11) % 101
        if value >= 76:
            return match.group(0)
        shade = (column * 3 + row * 5) % 4
        return f'<rect class="c decor{shade}" x="{x}" y="{y}"'

    svg = re.sub(r'<rect class="c" x="(\d+)" y="(\d+)"', decorate, svg)
    svg = svg.replace("</style>", STYLE + "</style>", 1)
    svg = svg.replace(
        "</desc>",
        " — decorative green cells; not actual GitHub contribution counts</desc>",
        1,
    )
    path.write_text(svg, encoding="utf-8")
