"""
Ian Sargent

Shared Altair theme and general chart helper functions
"""
import os
import altair as alt

# Color Constants (for importing)
ORANGE, NAVY, BLUE, GRAY, LIGHT = "#fc5d26", "#1f3864", "#2e75b6", "#e7e6e6", "#f2f2f2"
TEXT_GRAY = "#595959"
MUTED = "#9dc3e6"
CHART_W, CHART_H = 730, 400

# Disable altair max row limit
alt.data_transformers.disable_max_rows()

# Setting the color theme (altair)
def _theme_config():
    return {
        "config": {
            "background": "white",
            "view": {"stroke": None},
            "font": "Arial",
            "title": {"font": "Arial", "fontSize": 18, "fontWeight": "bold",
                      "color": NAVY, "anchor": "start", "offset": 12},
            "axis": {"labelFont": "Arial", "titleFont": "Arial",
                     "labelFontSize": 12, "titleFontSize": 13,
                     "labelColor": TEXT_GRAY, "titleColor": TEXT_GRAY,
                     "gridColor": GRAY, "domainColor": GRAY, "tickColor": GRAY},
            "legend": {"labelFont": "Arial", "titleFont": "Arial",
                       "labelFontSize": 12, "titleFontSize": 13, "orient": "top"},
            "range": {
                "category": [NAVY, BLUE, ORANGE, "#7f7f7f", MUTED],
                "ordinal": [LIGHT, MUTED, BLUE, NAVY],
                "ramp": [LIGHT, BLUE, NAVY],
            },
            "bar": {"color": NAVY},
            "line": {"color": NAVY, "strokeWidth": 3},
            "point": {"color": NAVY, "filled": True},
        }
    }

try:
    @alt.theme.register("precision", enable=True)
    def precision_theme() -> alt.theme.ThemeConfig:
        return _theme_config()
except AttributeError:
    alt.themes.register("precision", _theme_config)
    alt.themes.enable("precision")

# General chart helpers!
def save_chart(chart, name, folder="figures", scale=2, fmt="png"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{name}.{fmt}")
    chart.save(path, scale_factor=scale) if fmt == "png" else chart.save(path)
    print(f"Saved {path}")
    return path


def bar_chart(df, x, y, title, highlight=None, horizontal=True,
              x_title=None, y_title=None, value_format=".0f", labels=True,
              sort="-x", width=CHART_W, height=CHART_H):
    hl = [highlight] if highlight is not None and not isinstance(highlight, (list, tuple, set)) else list(highlight or [])
    color = (alt.condition(alt.FieldOneOfPredicate(field=x, oneOf=hl), alt.value(ORANGE), alt.value(NAVY))
             if hl else alt.value(NAVY))

    if horizontal:
        enc = dict(y=alt.Y(f"{x}:N", sort=sort, title=y_title if y_title is not None else None),
                   x=alt.X(f"{y}:Q", title=x_title or y))
        text_kw = dict(align="left", dx=4)
    else:
        enc = dict(x=alt.X(f"{x}:N", sort=sort.replace("-x", "-y") if sort else None, title=x_title),
                   y=alt.Y(f"{y}:Q", title=y_title or y))
        text_kw = dict(baseline="bottom", dy=-4)

    base = alt.Chart(df).encode(**enc)
    layers = base.mark_bar().encode(color=color)
    if labels:
        layers += base.mark_text(color=TEXT_GRAY, fontSize=12, **text_kw).encode(
            text=alt.Text(f"{y}:Q", format=value_format))
    return layers.properties(title=title, width=width, height=height)


def line_chart(df, x, y, title, group=None, highlight=None,
               x_title=None, y_title=None, x_type="T", width=CHART_W, height=CHART_H):
    enc = dict(x=alt.X(f"{x}:{x_type}", title=x_title),
               y=alt.Y(f"{y}:Q", title=y_title or y))
    if group:
        if highlight is not None:
            enc["color"] = alt.condition(alt.datum[group] == highlight, alt.value(ORANGE), alt.value(MUTED))
            enc["detail"] = alt.Detail(f"{group}:N")
        else:
            enc["color"] = alt.Color(f"{group}:N", title=None)
    return (alt.Chart(df).mark_line(point=True, strokeWidth=3)
            .encode(**enc).properties(title=title, width=width, height=height))