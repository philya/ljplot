import math

from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape


def distance(ar, br, a, b, ab):
    return (ar + br) * (a + b - ab) / (a + b)

def svg_animate(**kwargs):
    return """
        <animate 
           xlink:href="#{oid}"
           attributeName="{attr}"
           from="{fr}"
           to="{to}" 
           dur="{dur}s"
           begin="{begin}s"
           repeatCount="1"
           fill="freeze" 
           id="{aid}"/>""".format(**kwargs)

def svg_venn_circles_animation(df,
        chart_width=800,
        margin=50,
        title_height=60,
        timeline_height=100,
        step_duration=3

    ):

    max_value = max(list(df[['a', 'b']].max()))

    content_area_width = chart_width - margin * 2
    max_radius = content_area_width / 4

    content_area_height = max_radius * 2

    chart_height = content_area_height + margin * 2 + title_height + timeline_height

    # offset
    xo = margin
    yo = margin + title_height + timeline_height

    pi = math.pi

    max_area = pi * max_radius ** 2

    def value_radius(value):
        value_area = value * max_area / max_value
        return math.sqrt(value_area / pi)


    df = df.assign(ar = list(map(value_radius, df.a)))
    df = df.assign(br = list(map(value_radius, df.b)))
    df = df.assign(distance = list(map(distance, df.ar, df.br, df.a, df.b, df.ab)))
    df = df.assign(ax = list(map(lambda x: (content_area_width - x) / 2, df.distance)))
    df = df.assign(bx = list(map(lambda x: (content_area_width + x) / 2, df.distance)))


    elements = []
    
    for i in range(1, len(df.index)):
        
        timing = dict(
            dur=step_duration,
            begin=(i - 1) * step_duration)
        
        elements.append(svg_animate(
            aid="anim_ar_{}".format(i),
            oid="circle1",
            attr="r",
            fr=df.iloc[i - 1,].ar,
            to=df.iloc[i,].ar,
            **timing
        ))
        
        elements.append(svg_animate(
            aid="anim_ax_{}".format(i),
            oid="circle1",
            attr="cx",
            fr=df.iloc[i - 1,].ax + xo,
            to=df.iloc[i,].ax + xo,
            **timing
        ))
        
        elements.append(svg_animate(
            aid="anim_br_{}".format(i),
            oid="circle2",
            attr="r",
            fr=df.iloc[i - 1,].br,
            to=df.iloc[i,].br,
            **timing
        ))
        
        elements.append(svg_animate(
            aid="anim_bx_{}".format(i),
            oid="circle2",
            attr="cx",
            fr=df.iloc[i - 1,].bx + xo,
            to=df.iloc[i,].bx + xo,
            **timing
        ))

    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('venn_circles.svg')

    vc_svg = template.render(
        chart_width=chart_width,
        chart_height=chart_height,
        label = df.iloc[0,].label,
        ax = df.iloc[0,].ax + xo,
        bx = df.iloc[0,].bx + xo,
        ar = df.iloc[0,].ar,
        br = df.iloc[0,].br,
        cy=content_area_height / 2 + yo,
        elements = elements,
    )

    return vc_svg

