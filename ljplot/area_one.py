
from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape

from ljplot.svg import svg_text, svg_line, svg_polygon

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


        """
        tick_half_length = 5
        ruler_label_padding = tick_half_length * 2

        if (i + 1 > len(labels) / 2) and ruler_label_always_in:
            ruler_label_align = " left"
            ruler_label_x = step_x - ruler_label_padding
        else:
            ruler_label_align = " right"
            ruler_label_x = step_x + ruler_label_padding

        elements.append("<g class='ruler" + ruler_label_align + "'>" + \
            svg_line(step_x, top, step_x, bottom + label_height, 'area_line') + \
            svg_line(step_x, top, step_x, bottom, 'ruler_line') + \
            svg_line(step_x - tick_half_length, crack_top, step_x + tick_half_length, crack_top, "ruler_tick") + \
            svg_line(step_x - tick_half_length, crack_bottom, step_x + tick_half_length, crack_bottom, "ruler_tick") + \
            svg_text(ruler_label_x, top + (bar_100 - b[i] * coeff) / 2, "ruler_label", "{:.1%}".format(top_share)) + \
            svg_text(ruler_label_x, bottom - (bar_100 - a[i] * coeff) / 2, "ruler_label", "{:.1%}".format(bottom_share)) + \
            svg_text(ruler_label_x, (crack_bottom + crack_top) / 2, "ruler_label", "{:.1%}".format(crack_share)) + \
            "</g>")
        """


    elements.insert(0, svg_polygon(area_polygon, color, "none", ""))


    elements.append(svg_text(margin, margin, 'title', title))
    elements.append(svg_text(margin, title_height, 'subtitle', subtitle))


    if logo_url:
        elements.append("<image xlink:href='{src}' height='{lh}' width='{lw}' x='{x}' y='{y}' />".format(lh=logo_height, lw=logo_width, src=logo_url, x=chart_width - logo_width - margin, y=chart_height - logo_height - margin))


    return template.render(width=chart_width, height=chart_height, elements=elements)