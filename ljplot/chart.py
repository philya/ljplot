

from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape

from ljplot.svg import svg_text, svg_line, svg_polygon, svg_text, svg_polyline, svg_circle, svg_polyline_path, svg_rect

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
        padding=0,
        padding_top=None,
        padding_bottom=None,
        padding_left=None,
        padding_right=None,
        force_min_value=None,
        label_height=40,
        value_label_x_offset=-0,
        value_label_y_offset=-20,
        colors=COLORS,
        template_loader=FileSystemLoader('templates'),
        xlabel_format="{:.0f}",
        value_label_format="{:,.0f}",
        #value_label_format="{:.1%}",
        connect_shape="line", # line or path
        path_curve=0.5,

        title_height = 38,
        line_legend_x_padding=20,

        twitter=None,
        signature=None,

        template_name="base_chart.svg",


        # Stacked line properties
        line_legend_y_shift=0,
        line_label_x_padding=20,
        


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
        self.title_height = title_height

        self.padding = padding
        self.padding_top = padding_top
        self.padding_bottom = padding_bottom
        self.padding_left = padding_left
        self.padding_right = padding_right

        self.line_legend_x_padding = line_legend_x_padding

        self.twitter = twitter
        self.signature = signature

        self.template_name = template_name


        self.line_legend_y_shift = line_legend_y_shift
        self.line_label_x_padding = line_label_x_padding


        



class Chart:

    def __init__(self, chart_settings, **kwargs):

        self.s = chart_settings

        self._init_padding()

        for name, value in kwargs.items():
            setattr(self, name, value)


        env = Environment(loader=self.template_loader)
        self.template = env.get_template(self.template_name)


    def _init_padding(self):

        for d in ['left', 'right', 'top', 'bottom']:
            an = 'padding_' + d
            if getattr(self, an) == None:
                setattr(self, an, self.padding)


    def __getattr__(self, name):
        return getattr(self.s, name)



    def plot_svg(self):

        left = self.margin + self.padding_left
        right = self.chart_width - self.margin - self.padding_right
        top = self.margin + self.padding_top # + title_height
        bottom = self.chart_height - self.margin - self.padding_bottom #- footer_height - self.label_height 

        elements = self.content_elements(left, right, top, bottom)

        if hasattr(self, "title"):

            #title_y = self.margin + (self.padding_top + self.title_height) / 2
            #title_y = self.margin + self.padding_top / 2
            title_y = self.margin
            elements.append(svg_text(self.margin, title_y, 'title', self.title))
        
        if hasattr(self, "subtitle"):
            elements.append(svg_text(self.margin, title_y + 60 , 'subtitle', self.subtitle))


        if self.signature:

            if type(self.signature) is list:
                content = ""

                for i, sline in enumerate(self.signature):
                    content += "<tspan x='{}' dy='{:.1f}em'>{}</tspan>".format(left, i * 1.5, sline)

            else:
                content = self.signature
            
            elements.append(svg_text(left, self.chart_height - self.margin, 'signature', content))

        # if logo_url:
        #     elements.append("<image xlink:href='{src}' height='{lh}' width='{lw}' x='{x}' y='{y}' />".format(lh=logo_height, lw=logo_width, src=logo_url, x=chart_width - logo_width - margin, y=chart_height - logo_height - margin))

        if self.twitter:
            tm = self.margin
            h = 22
            elements.append(svg_text(self.chart_width - tm - h * 1.1, self.chart_height - tm, "twitter", "@" + self.twitter))
            elements.append("<image xlink:href='{}' x='{}' y='{}' height='{}' class='twitter_logo'/>".format(
                "https://upload.wikimedia.org/wikipedia/fr/c/c8/Twitter_Bird.svg",
                self.chart_width - tm - h,
                self.chart_height - tm - h * .9,
                h,
            ))


        return self.template.render(width=self.chart_width, height=self.chart_height, elements=elements)

class LineChart(Chart):

    def __init__(self, chart_settings, **kwargs):

        super().__init__(chart_settings, **kwargs)

        self.labels = []
        self.lines = []

    def set_data(self, df, line_legends=None):
        self.line_legends = line_legends
        self.df = df


    def content_elements(self, left, right, top, bottom):

        elements = []


        steps = len(self.df)
        step_width = (right - left) / (steps - 1)

        if self.line_legends:
            line_names = self.line_legends
        else:
            line_names = list(self.df.columns[1:])
        #line_names = self.labels

        max_value = max(self.df.iloc[:, 1:].max())
        if self.force_min_value is not None:
            min_value = self.force_min_value
        else:
            min_value = min(self.df.iloc[:, 1:].min())

        plot_area_height = bottom - top
        value_range = max_value - min_value

        line_points = [[] for x in range(len(line_names))]

        label_elements = []

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

                font_height = 17

                #elements.append(svg_rect(step_x + self.value_label_x_offset - step_width * .7, bottom - y + self.value_label_y_offset - font_height + 2, step_width * .7, font_height, "value_label_whiteout"))
                label_elements.append(svg_text(step_x + self.value_label_x_offset, bottom - y + self.value_label_y_offset, "value_label white_shadow", self.value_label_format.format(value)))
                label_elements.append(svg_text(step_x + self.value_label_x_offset +1, bottom - y + self.value_label_y_offset, "value_label white_shadow", self.value_label_format.format(value)))
                label_elements.append(svg_text(step_x + self.value_label_x_offset -1, bottom - y + self.value_label_y_offset, "value_label white_shadow", self.value_label_format.format(value)))
                label_elements.append(svg_text(step_x + self.value_label_x_offset, 1 + bottom - y + self.value_label_y_offset, "value_label white_shadow", self.value_label_format.format(value)))
                label_elements.append(svg_text(step_x + self.value_label_x_offset, -1 + bottom - y + self.value_label_y_offset, "value_label white_shadow", self.value_label_format.format(value)))

                label_elements.append(svg_text(step_x + self.value_label_x_offset, bottom - y + self.value_label_y_offset, "value_label", self.value_label_format.format(value)))
                

        elements = elements + label_elements

        #elements.append(svg_text(margin, chart_height - margin, 'signature', signature))

        for i, lp in enumerate(line_points):
            color = self.colors[i]
            # if self.connect_shape == 'line':
            #     elements.insert(0, svg_polyline(lp, color, "linechart_line"))
            # elif self.connect_shape == 'path':
            elements.insert(0, svg_polyline_path(lp, color, "linechart_line", step_width * self.path_curve))



            elements.insert(0, svg_text(self.chart_width - self.margin - self.padding_right + self.line_legend_x_padding, lp[-1][1], "line_legend", line_names[i]))

            # Another way to smoothen the polyline:
            # https://medium.com/@francoisromain/smooth-a-svg-path-with-cubic-bezier-curves-e37b49d46c74

        return elements


class StackedLineChart(Chart):


    def __init__(self, chart_settings, **kwargs):

        super().__init__(chart_settings, **kwargs)

        self.labels = []
        self.lines = []

    def set_data(self, df, line_legends=None, line_labels=None):
        self.line_legends = line_legends
        self.line_labels = line_labels
        self.df = df


    def content_elements(self, left, right, top, bottom):

        elements = []


        steps = len(self.df)
        step_width = (right - left) / (steps - 1)

        if self.line_legends:
            line_names = self.line_legends
        else:
            line_names = list(self.df.columns[1:])
        #line_names = self.labels

        max_value = self.df.iloc[:, 1:].sum(axis=1).max()

        min_value = 0

        # if self.force_min_value is not None:
        #     min_value = self.force_min_value
        # else:
        #     min_value = min(self.df.iloc[:, 1:].min())

        plot_area_height = bottom - top
        value_range = max_value - min_value

        line_points = [[] for x in range(len(line_names))]

        for j in range(len(self.df)):
            row = self.df.iloc[j]

            step_x = left + step_width * j

            elements.append(svg_text(step_x, self.margin/5 + bottom + self.label_height / 2.0, "xlabel", self.xlabel_format.format(row[0])))

            elements.append(svg_line(step_x, self.margin/5 + bottom, step_x, self.margin/5 + bottom + 5, 'xtick'))

            step_y = 0

            for i, line_name in enumerate(line_names):
                #color = self.colors[i]

                value = step_y + row[i + 1]

                y = plot_area_height * (value - min_value) / value_range

                line_points[i].append((step_x, bottom - y))

                step_y = value
                
                #elements.append(svg_circle(step_x, bottom - y, 4, color, color, "linechart_dot"))

                #font_height = 17

                #elements.append(svg_rect(step_x + self.value_label_x_offset - step_width * .7, bottom - y + self.value_label_y_offset - font_height + 2, step_width * .7, font_height, "value_label_whiteout"))
                #elements.append(svg_text(step_x + self.value_label_x_offset, bottom - y + self.value_label_y_offset, "value_label", self.value_label_format.format(value)))

        #elements.append(svg_text(margin, chart_height - margin, 'signature', signature))

        prev_rightmost_y = bottom

        for i, lp in enumerate(line_points):
            color = self.colors[i]
            # if self.connect_shape == 'line':
            #     elements.insert(0, svg_polyline(lp, color, "linechart_line"))
            # elif self.connect_shape == 'path':
            #elements.insert(0, svg_polyline_path(lp, color, "linechart_line", step_width * self.path_curve))

            area_polygon = [(right, bottom), (left, bottom)] + lp

            elements.insert(0, svg_polygon(area_polygon, color, "none", ""))


            line_legend_y = (prev_rightmost_y + lp[-1][1]) / 2 + self.line_legend_y_shift
            elements.insert(0, svg_text(self.chart_width - self.margin - self.padding_right + self.line_legend_x_padding, line_legend_y, "line_legend", line_names[i]))
            if self.line_labels:
                #elements.append(svg_text(self.chart_width - self.margin - self.padding_right - 10, line_legend_y, "line_label line_label_dark", self.line_labels[i]))
                elements.append(svg_text(self.chart_width - self.margin - self.padding_right - self.line_label_x_padding, line_legend_y, "line_label", self.line_labels[i]))


            prev_rightmost_y = lp[-1][1]

            # Another way to smoothen the polyline:
            # https://medium.com/@francoisromain/smooth-a-svg-path-with-cubic-bezier-curves-e37b49d46c74

        return elements


