
from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape

def svg_polyline(points, stroke, clss, fill="none"):

    return '<polyline points="{}" fill="{}" stroke="{}" class="{}"/>'.format(
        ' '.join(['{},{}'.format(*p) for p in points]),
        fill,
        stroke,
        clss
    )

def svg_circle(x, y, r, stroke, fill, clss):

    return '<circle cx="{}" cy="{}" r="{}" stroke="{}" fill="{}" class="{}"/>'.format(
        x,
        y,
        r,
        stroke,
        fill,
        clss
    )

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

def safe_svg_str(s):
    return s.replace('&', '&amp;')


def venn_trend(labels, a, b, ab,
        a_color = "#00a86d",
        b_color = "#4472c4", 
        chart_width=800,
        chart_height=600,
        margin=60,
        title_height=32,
        footer_height=30,
        label_height=60,
        value_format="{:g}",
        signature="",
        title="",
        ruler_label_always_in=False,
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
        display_position=True,
        signature="",
        title="",
        subtitle="",
        bar_opacity=.9,
        colors={'bar': '#ff8b6a', 'negative': "#4281A4"},
        logo_url=None,
        logo_height=70,
        logo_width=70,
        center_zero=False,
        omit_value_sign=False,
        positive_label="",
        negative_label="",
    ):

    #env = Environment(loader=PackageLoader('ljplot', 'templates'))
    env = Environment(loader=FileSystemLoader('templates'))

    template = env.get_template('chart.svg')

    if chart_height is None:
        chart_height = len(values) * (item_padding + bar_height) + margin * 2.0 + title_height + footer_height


    max_value = max(values)
    min_value = min(values)
    max_abs = max([abs(v) for v in values])
    if min_value > 0:
        min_value = 0


    bar_left_x = margin + label_col_width
    if min_value < 0:
        bar_left_x += value_col_width

    bar_right_x = chart_width - margin - value_col_width

    bar_100 = bar_right_x - bar_left_x

    
    value_diff = max_value - min_value
    if center_zero:
        zero_x = bar_left_x + bar_100 / 2
    else:
        zero_x = (abs(min_value) / value_diff) * bar_100 + bar_left_x

    if min_value < 0:
        label_x = bar_left_x - item_padding - value_col_width
    else:
        label_x = bar_left_x - item_padding

    #label_x = zero_x - item_padding

    elements = []
    for i, label in enumerate(labels):
        #print(label, values[i])
        y_position = margin + title_height + i * (bar_height + item_padding)

        if center_zero:
            bar_width = (bar_100 / 2) * (values[i] / max_abs)
        else:
            bar_width = bar_100 * values[i] / value_diff

        if bar_width > 0: 
            elements.append(svg_rect(zero_x, y_position,  bar_width, bar_height, "bar"))
        else: 
            elements.append(svg_rect(zero_x + bar_width, y_position, abs(bar_width), bar_height, "bar negative"))


        elements.append(svg_text(label_x, y_position + bar_height * 0.5, "label", safe_svg_str(label)))

        if bar_width > 0:
            value_label_x = zero_x + bar_width + item_padding
            value_label_class = "value_label right"
        else:
            value_label_x = zero_x + bar_width - item_padding
            value_label_class = "value_label left"

        if omit_value_sign:
            value = abs(values[i])
        else:
            value = values[i]
        elements.append(svg_text(value_label_x, y_position + bar_height * .5, value_label_class, value_format.format(value)))

        if display_position:
            elements.append(svg_text(bar_left_x + item_padding, y_position + bar_height * .5, "place_label", "{:g}".format(i + 1)))


    elements.append(svg_text(bar_left_x, chart_height - margin, 'signature', signature))

    elements.append(svg_text(bar_left_x, margin, 'title', title))
    elements.append(svg_text(bar_left_x, title_height, 'subtitle', subtitle))

    elements.append(svg_text(bar_left_x + bar_100 / 4, title_height + margin / 2, 'direction_label left', negative_label))
    elements.append(svg_text(bar_right_x - bar_100 / 4, title_height + margin / 2, 'direction_label right', positive_label))

    if logo_url:
        elements.append("<image xlink:href='{src}' height='{lh}' width='{lw}' x='{x}' y='{y}' />".format(lh=logo_height, lw=logo_width, src=logo_url, x=chart_width - logo_width - margin, y=chart_height - logo_height - margin))


    return template.render(bar_opacity=bar_opacity, colors=colors, width=chart_width, height=chart_height, elements=elements)



    
def hbar_stacked(df,
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
        display_position=True,
        signature="",
        title="",
        subtitle="",
        bar_opacity=.9,
        colors={'bar': '#ff8b6a', 'negative': "#4281A4"},
        logo_url=None,
        logo_height=70,
        logo_width=70,
        center_zero=False,
        omit_value_sign=False,
        positive_label="",
        negative_label="",
        logo_x=None,
        logo_y=None,
        max_values=None,
        min_values=None,
        line_width=0,
        value_label_always_right=False,
    ):

    labels = list(df.iloc[:, 0])
    

    #env = Environment(loader=PackageLoader('ljplot', 'templates'))
    env = Environment(loader=FileSystemLoader('templates'))

    template = env.get_template('chart.svg')

    if chart_height is None:
        chart_height = len(labels) * (item_padding + bar_height) + margin * 2.0 + title_height + footer_height

    elements = []

    columns = len(df.columns[1:])

    bar_window_left = margin + label_col_width
    bar_window_right = chart_width - margin
    bar_window_width = bar_window_right - bar_window_left
    bar_column_width = bar_window_width / columns

    label_x = bar_window_left - item_padding * 2

    def get_y_position(i):
        return margin + title_height + i * (bar_height + item_padding)

    for i, label in enumerate(labels):
        y_position = get_y_position(i)
        elements.append(svg_text(label_x, y_position + bar_height * 0.5, "label", safe_svg_str(label)))
        elements.append("<line x1='{}' y1='{}' x2='{}' y2='{}' stroke-width='{}' class='ruler_line'/>".format(bar_window_left, y_position + bar_height * 0.5, bar_window_right, y_position + bar_height * 0.5, line_width))



    for coli, column_name in enumerate(list(df.columns[1:])):

        values = list(df.iloc[:, coli + 1])

        if max_values and max_values[coli]:
            max_value = max_values[coli]
        else:
            max_value = max(values)

        if min_values and min_values[coli]:
            min_value = min_values[coli]
        else:
            min_value = min(values)

        #max_abs = max([abs(v) for v in values])
        max_abs = max([abs(min_value), abs(max_value)])
        if min_value > 0:
            min_value = 0


        bar_left_x = bar_window_left + coli * bar_column_width
        if min_value < 0 and not value_label_always_right:
            bar_left_x += value_col_width

        bar_right_x = bar_window_left + (coli + 1) * bar_column_width - value_col_width

        bar_100 = bar_right_x - bar_left_x

        
        value_diff = max_value - min_value
        if center_zero and (min_value < 0):
            zero_x = bar_left_x + bar_100 / 2
        else:
            zero_x = (abs(min_value) / value_diff) * bar_100 + bar_left_x

        #if min_value < 0:
        #    label_x = bar_left_x - item_padding - value_col_width
        #else:
        #    label_x = bar_left_x - item_padding

        #label_x = zero_x - item_padding

        elements.append(svg_text(bar_left_x + bar_100 / 2, title_height + margin / 4, 'column_label', safe_svg_str(column_name)))

        
        for i, label in enumerate(labels):
            #print(label, values[i])
            y_position = get_y_position(i)

            if center_zero and (min_value < 0):
                bar_width = (bar_100 / 2) * (values[i] / max_abs)
            else:
                bar_width = bar_100 * values[i] / value_diff

            if bar_width > 0: 
                elements.append(svg_rect(zero_x, y_position,  bar_width, bar_height, "bar"))
            else: 
                elements.append(svg_rect(zero_x + bar_width, y_position, abs(bar_width), bar_height, "bar negative"))


            if bar_width > 0:
                value_label_x = zero_x + bar_width + item_padding
                value_label_class = "value_label right"
            else:
                if value_label_always_right:
                    value_label_x = zero_x + item_padding
                    value_label_class = "value_label right"
                else:
                    value_label_x = zero_x + bar_width - item_padding
                    value_label_class = "value_label left"

            if omit_value_sign:
                value = abs(values[i])
            else:
                value = values[i]
            elements.append(svg_text(value_label_x, y_position + bar_height * .5, value_label_class, value_format.format(value)))

            if display_position:
                elements.append(svg_text(bar_left_x + item_padding, y_position + bar_height * .5, "place_label", "{:g}".format(i + 1)))




    elements.append(svg_text(bar_window_left, chart_height - margin, 'signature', signature))

    elements.append(svg_text(bar_window_left, margin, 'title', title))
    elements.append(svg_text(bar_window_left, title_height, 'subtitle', subtitle))

    #elements.append(svg_text(bar_window_left + bar_100 / 4, title_height + margin / 2, 'direction_label left', negative_label))
    #elements.append(svg_text(bar_window_right - bar_100 / 4, title_height + margin / 2, 'direction_label right', positive_label))



    if logo_url:
        elements.append("<image xlink:href='{src}' height='{lh}' width='{lw}' x='{x}' y='{y}' />".format(lh=logo_height, lw=logo_width, src=logo_url, x=chart_width - logo_width - margin, y=chart_height - logo_height - margin))


    return template.render(bar_opacity=bar_opacity, colors=colors, width=chart_width, height=chart_height, elements=elements)


    