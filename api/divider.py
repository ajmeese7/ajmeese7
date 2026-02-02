import os
import re

from flask import Flask, Response, request

DEFAULT_WIDTH = 1200
DEFAULT_HEIGHT = 36
DEFAULT_STROKE = "2a2a2a"
DEFAULT_ACCENT = "f5f5f5"
DEFAULT_DURATION = 6.0
DEFAULT_THICKNESS = 2

HEX_COLOR_PATTERN = re.compile(r"^[0-9a-fA-F]{6}$")

app = Flask(__name__)


def clamp_int(value, default, minimum, maximum):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return max(minimum, min(parsed, maximum))


def clamp_float(value, default, minimum, maximum):
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    return max(minimum, min(parsed, maximum))


def validate_hex_color(color, default):
    if color and HEX_COLOR_PATTERN.match(color):
        return color.lower()
    return default


def build_divider_svg(width, height, stroke_color, accent_color, duration, thickness):
    y = height // 2
    line_length = width - 40
    dash_on = max(24, width // 30)
    dash_off = max(100, line_length - dash_on)
    dash_total = dash_on + dash_off

    return f"""<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{width}\" height=\"{height}\" viewBox=\"0 0 {width} {height}\" role=\"img\" aria-labelledby=\"title desc\">
  <title id=\"title\">Divider</title>
  <desc id=\"desc\">Animated divider line</desc>
  <style>
    .line {{ stroke: #{stroke_color}; stroke-width: {thickness}; stroke-linecap: round; }}
    .pulse {{
      stroke: #{accent_color};
      stroke-dasharray: {dash_on} {dash_off};
      animation: sweep {duration}s ease-in-out infinite;
    }}
    @keyframes sweep {{
      0% {{ stroke-dashoffset: 0; opacity: 0.2; }}
      50% {{ stroke-dashoffset: -{dash_total // 2}; opacity: 0.9; }}
      100% {{ stroke-dashoffset: -{dash_total}; opacity: 0.2; }}
    }}
  </style>
  <line class=\"line\" x1=\"20\" y1=\"{y}\" x2=\"{width - 20}\" y2=\"{y}\" />
  <line class=\"line pulse\" x1=\"20\" y1=\"{y}\" x2=\"{width - 20}\" y2=\"{y}\" />
</svg>"""


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    width = clamp_int(request.args.get("width"), DEFAULT_WIDTH, 400, 2000)
    height = clamp_int(request.args.get("height"), DEFAULT_HEIGHT, 16, 120)
    thickness = clamp_int(request.args.get("thickness"), DEFAULT_THICKNESS, 1, 6)
    stroke_color = validate_hex_color(request.args.get("stroke"), DEFAULT_STROKE)
    accent_color = validate_hex_color(request.args.get("accent"), DEFAULT_ACCENT)
    duration = clamp_float(request.args.get("duration"), DEFAULT_DURATION, 2.0, 12.0)

    svg = build_divider_svg(width, height, stroke_color, accent_color, duration, thickness)
    resp = Response(svg, mimetype="image/svg+xml")
    resp.headers["Cache-Control"] = "s-maxage=300"
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=int(os.getenv("PORT", 5000)))
