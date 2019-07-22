
from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape

def svg_rect(x, y, width, height, clss):
    return '<rect x="{}" y="{}" width="{}" height="{}" class="{}"/>'.format(x, y, width, height, clss)

def svg_text(x, y, clss, text):
    return '<text x="{}" y="{}" class="{}">{}</text>'.format(x, y, clss, text)

def hbar(labels, values, color="#252525",
        chart_width=980,
        chart_height=None,
        bar_height=30,
        margin=50,
        title_height=100,
        footer_height=50,
        item_padding=10,
        label_col_width=200,
        value_format="{:g}"
    ):

    #env = Environment(loader=PackageLoader('ljplot', 'templates'))
    env = Environment(loader=FileSystemLoader('/Users/chilemba/projects/ljplot/templates'))

    template = env.get_template('chart.svg')

    if chart_height is None:
        chart_height = len(values) * (item_padding + bar_height) + margin * 2.0 + title_height + footer_height


    bar_left_x = margin + label_col_width
    bar_right_x = chart_width - margin

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


    return template.render(width=chart_width, height=chart_height, elements=elements)



    


    