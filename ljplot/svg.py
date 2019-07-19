
from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape

def svg_rect(x, y, width, height, clss):
    return '<rect x="{}" y="{}" width="{}" height="{}" class="{}"/>'.format(x, y, width, height, clss)

def hbar(labels, values, color="#252525",
        chart_width=980,
        chart_height=None,
        bar_height=30,
        margin=50,
        title_height=100,
        footer_height=50,
        item_padding=10,
    ):

    #env = Environment(loader=PackageLoader('ljplot', 'templates'))
    env = Environment(loader=FileSystemLoader('/Users/chilemba/projects/ljplot/templates'))

    template = env.get_template('chart.svg')

    if chart_height is None:
        chart_height = len(values) * (item_padding + bar_height) + margin * 2.0 + title_height + footer_height


    bar_left_x = margin
    bar_right_x = chart_width - margin

    bar_100 = chart_width - 2.0 * margin

    max_value = max(values)


    elements = []
    for i, label in enumerate(labels):
        #print(label, values[i])

        bar_width = bar_100 * values[i] / max_value
        elements.append(svg_rect(bar_left_x, margin + title_height + i * (bar_height + item_padding),  bar_width, bar_height, "bar"))



    return template.render(width=chart_width, height=chart_height, elements=elements)



    


    