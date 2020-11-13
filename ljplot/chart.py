

from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape

from ljplot.svg import svg_text, svg_line, svg_polygon, svg_text, svg_polyline, svg_circle, svg_polyline_path

from millify import millify

COLORS = [
    "#33a02c",
    "#1f78b4",
    "#fb9a99",
    "#e31a1c",
    "#fdbf6f",
    "#a6cee3",
    "#b2df8a",
]



class ChartSettings:

    def __init__(self,
        chart_width=800,
        chart_height=600,
        margin=60,
        force_min_value=None,
        label_height=40,
        value_label_x_offset=-0,
        value_label_y_offset=-20,
        colors=COLORS,
        template_loader=FileSystemLoader('templates'),
        xlabel_format="{:.0f}",
        value_label_format="{:.1%}",
        connect_shape="line", # line or path
        path_curve=0.5,
    ):

        self.chart_width = chart_width
        self.chart_height = chart_height
        self.margin = margin
        self.force_min_value = force_min_value
        self.label_height = label_height
        self.value_label_x_offset = value_label_x_offset
        self.value_label_y_offset = value_label_y_offset
        self.colors = colors

        self.template_loader = template_loader

        self.xlabel_format = xlabel_format
        self.value_label_format = value_label_format
        self.connect_shape = connect_shape
        self.path_curve = path_curve





class Chart:

    def __init__(self, chart_settings, **kwargs):

        self.s = chart_settings

        for name, value in kwargs.items():
            setattr(self, name, value)


        env = Environment(loader=self.template_loader)

        self.template = env.get_template('area_one.svg')

        self.labels = []
        self.lines = []


    def __getattr__(self, name):
        return getattr(self.s, name)


    #def __setattr__(self, name, value):
    #    if hasattr(self, name):

    #    return getattr(self.s, name)



    # def add_line(self, name, values):
    #     self.labels.append(name)
    #     elf.lines.append(values)

    def add_data_frame(self, df):
        self.df = df


    def get_svg(self):
        pass


    def line_chart(self,        
        ):



        left = self.margin
        right = self.chart_width - self.margin
        top = self.margin # + title_height
        bottom = self.chart_height - self.margin #- footer_height - self.label_height 


        steps = len(self.df)
        step_width = (right - left) / (steps - 1)

        line_names = list(self.df.columns[1:])
        #line_names = self.labels

        max_value = max(self.df.iloc[:, 1:].max())
        if self.force_min_value is not None:
            min_value = self.force_min_value
        else:
            min_value = min(self.df.iloc[:, 1:].min())

        plot_area_height = bottom - top
        value_range = max_value - min_value

        elements = []

        line_points = [[] for x in range(len(line_names))]

        for j in range(len(self.df)):
            row = self.df.iloc[j]

            step_x = left + step_width * j

            elements.append(svg_text(step_x, self.margin/5 + bottom + self.label_height / 2.0, "xlabel", self.xlabel_format.format(row[0])))

            elements.append(svg_line(step_x, self.margin/5 + bottom, step_x, self.margin/5 + bottom + 5, 'xtick'))

            for i, line_name in enumerate(line_names):
                color = self.colors[i]

                value = row[i + 1]

                y = plot_area_height * (value - min_value) / value_range

                line_points[i].append((step_x, bottom - y))
                
                elements.append(svg_circle(step_x, bottom - y, 4, color, color, "linechart_dot"))

                elements.append(svg_text(step_x + self.value_label_x_offset, bottom - y + self.value_label_y_offset, "value_label", self.value_label_format.format(value)))


        for i, lp in enumerate(line_points):
            color = self.colors[i]
            # if self.connect_shape == 'line':
            #     elements.insert(0, svg_polyline(lp, color, "linechart_line"))
            # elif self.connect_shape == 'path':
            elements.insert(0, svg_polyline_path(lp, color, "linechart_line", step_width * self.path_curve))




        return self.template.render(width=self.chart_width, height=self.chart_height, elements=elements)

