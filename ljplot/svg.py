
from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape

def svg_rect(x, y, width, height, clss):
    return '<rect x="{}" y="{}" width="{}" height="{}" class="{}"/>'.format(x, y, width, height, clss)

def svg_text(x, y, clss, text):
    return '<text x="{}" y="{}" class="{}">{}</text>'.format(x, y, clss, text)

def svg_polygon(points, fill, stroke, clss):

    return '<polygon points="{}" fill="{}" stroke="{}" class="{}"/>'.format(
        ' '.join(['{},{}'.format(*p) for p in points]),
        fill,
        stroke,
        clss
    )

def svg_line(x1, y1, x2, y2, clss):
    return '<line x1="{}" y1="{}" x2="{}" y2="{}" class="{}"/>'.format(x1, y1, x2, y2, clss)


def venn_trend(labels, a, b, ab,
        a_color = "#00a86d",
        b_color = "#4472c4", 
        chart_width=800,
        chart_height=600,
        margin=50,
        title_height=32,
        footer_height=30,
        label_height=60,
        value_format="{:g}",
        signature="",
        title=""
    ):
    #env = Environment(loader=PackageLoader('ljplot', 'templates'))
    env = Environment(loader=FileSystemLoader('/Users/chilemba/projects/ljplot/templates'))
    template = env.get_template('venn_trend.svg')

    left = margin
    right = chart_width - margin
    top = margin + title_height
    bottom = chart_height - footer_height - label_height - margin

    bar_100 = bottom - top

    step_width = (right - left) / (len(labels) - 1)

    top_polygon = [(right, top), (left, top)]
    bottom_polygon = [(right, bottom), (left, bottom)]
    elements = []

    for i, label in enumerate(labels):
        step_total = a[i] + b[i] - ab[i]
        coeff = bar_100 / step_total

        step_x = left + step_width * i

        crack_top = bottom - b[i] * coeff
        crack_bottom = top + a[i] * coeff

        top_share = (step_total - b[i]) / step_total
        bottom_share = (step_total - a[i]) / step_total
        crack_share = ab[i] / step_total

        top_polygon.append((step_x, crack_bottom))
        bottom_polygon.append((step_x, crack_top))

        elements.append(svg_text(step_x, bottom + label_height / 2.0, "xlabel", label))

        tick_half_length = 5
        ruler_label_padding = tick_half_length * 2

        if i + 1 > len(labels) / 2:
            ruler_label_align = " left"
            ruler_label_x = step_x - ruler_label_padding
        else:
            ruler_label_align = " right"
            ruler_label_x = step_x + ruler_label_padding

        elements.append("<g class='ruler" + ruler_label_align + "'>" + \
            svg_line(step_x, top, step_x, bottom, 'area_line') + \
            svg_line(step_x, top, step_x, bottom, 'ruler_line') + \
            svg_line(step_x - tick_half_length, crack_top, step_x + tick_half_length, crack_top, "ruler_tick") + \
            svg_line(step_x - tick_half_length, crack_bottom, step_x + tick_half_length, crack_bottom, "ruler_tick") + \
            svg_text(ruler_label_x, top + (bar_100 - b[i] * coeff) / 2, "ruler_label", "{:.1%}".format(top_share)) + \
            svg_text(ruler_label_x, bottom - (bar_100 - a[i] * coeff) / 2, "ruler_label", "{:.1%}".format(bottom_share)) + \
            svg_text(ruler_label_x, (crack_bottom + crack_top) / 2, "ruler_label", "{:.1%}".format(crack_share)) + \
            "</g>")


    elements.insert(0, svg_polygon(top_polygon, a_color, "none", ""))
    elements.insert(1, svg_polygon(bottom_polygon, b_color, "none", ""))

    return template.render(width=chart_width, height=chart_height, elements=elements)

def hbar(labels, values, color="#252525",
        chart_width=980,
        chart_height=None,
        bar_height=30,
        margin=50,
        title_height=32,
        footer_height=30,
        item_padding=10,
        label_col_width=160,
        value_col_width=40,
        value_format="{:g}",
        signature="Philip Olenyk for Prophy.Science © 2019",
        title="Researchers Per 100k Population"
    ):

    #env = Environment(loader=PackageLoader('ljplot', 'templates'))
    env = Environment(loader=FileSystemLoader('/Users/chilemba/projects/ljplot/templates'))

    template = env.get_template('chart.svg')

    if chart_height is None:
        chart_height = len(values) * (item_padding + bar_height) + margin * 2.0 + title_height + footer_height


    bar_left_x = margin + label_col_width
    bar_right_x = chart_width - margin - value_col_width

    bar_100 = bar_right_x - bar_left_x

    max_value = max(values)


    elements = []
    for i, label in enumerate(labels):
        #print(label, values[i])
        y_position = margin + title_height + i * (bar_height + item_padding)

        bar_width = bar_100 * values[i] / max_value
        elements.append(svg_rect(bar_left_x, y_position,  bar_width, bar_height, "bar"))


        elements.append(svg_text(bar_left_x - item_padding, y_position + bar_height * 0.5, "label", label))

        elements.append(svg_text(bar_left_x + bar_width + item_padding, y_position + bar_height * .5, "value_label", value_format.format(values[i])))

        elements.append(svg_text(bar_left_x + item_padding, y_position + bar_height * .5, "place_label", "{:g}".format(i + 1)))


    elements.append(svg_text(bar_left_x, chart_height - margin, 'signature', signature))

    elements.append(svg_text(bar_left_x, margin, 'title', title))

    #elements.append(svg_text(bar_left_x, margin + margin , 'subtitle', subtitle))



    return template.render(width=chart_width, height=chart_height, elements=elements)



    


    