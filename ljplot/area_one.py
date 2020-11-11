
from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape

from ljplot.svg import svg_text, svg_line, svg_polygon, svg_text

from millify import millify

def area_one_chart(labels, values,
        color = "#00a86d",
        chart_width=800,
        chart_height=600,
        margin=60,
        title_height=32,
        footer_height=30,
        label_height=60,
        value_format="{:g}",
        signature="",
        title="",
        subtitle="",

        ruler_label_always_in=False,
        value_marks=[],

        logo_url=None,
        logo_height=50,
        logo_width=50,
        twitter="",
    ):

    #env = Environment(loader=PackageLoader('ljplot', 'templates'))
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('area_one.svg')

    left = margin
    right = chart_width - margin
    top = margin + title_height
    bottom = chart_height - footer_height - label_height - margin

    bar_100 = bottom - top

    step_width = (right - left) / (len(labels) - 1)

    area_polygon = [(right, bottom), (left, bottom)]

    max_value = max(values)

    coeff = bar_100 / max_value

    elements = []

    for i, label in enumerate(labels):
        step_x = left + step_width * i

        edge = bottom - values[i] * coeff

        area_polygon.append((step_x, edge))

        elements.append(svg_text(step_x, bottom + label_height / 2.0, "xlabel", label))

        if label in value_marks:
            elements.append(svg_line(step_x, bottom, step_x, edge, 'ruler_line'))
            elements.append("<circle cx='{}' cy='{}' r='3' class='ruler_dot'/>".format(
                step_x,
                edge
            ))

            elements.append(svg_text(step_x, edge - 10, "ruler_label", millify(values[i], precision=1)))


    elements.insert(0, svg_polygon(area_polygon, color, "none", ""))


    elements.append(svg_text(margin, margin + title_height, 'title', title))
    elements.append(svg_text(margin, margin * 1.7 + title_height , 'subtitle', subtitle))

    elements.append(svg_text(margin, chart_height - margin, 'signature', signature))


    if logo_url:
        elements.append("<image xlink:href='{src}' height='{lh}' width='{lw}' x='{x}' y='{y}' />".format(lh=logo_height, lw=logo_width, src=logo_url, x=chart_width - logo_width - margin, y=chart_height - logo_height - margin))

    if twitter:
        tm = margin
        h = 22
        elements.append(svg_text(chart_width - tm - h * 1.1, chart_height - tm, "twitter", "@" + twitter))
        elements.append("<image xlink:href='{}' x='{}' y='{}' height='{}' class='twitter_logo'/>".format(
            "https://upload.wikimedia.org/wikipedia/fr/c/c8/Twitter_Bird.svg",
            chart_width - tm - h,
            chart_height - tm - h * .9,
            h,
        ))
            # height='{lh}' width='{lw}' x='{x}' y='{y}' />".format(
            #lh=logo_height, lw=logo_width, src=logo_url, x=chart_width - logo_width - margin, y=chart_height - logo_height - margin))




    return template.render(width=chart_width, height=chart_height, elements=elements)