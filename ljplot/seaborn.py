
import seaborn as sns
import matplotlib.pyplot as plt

from IPython.display import display, HTML


def hbar(data, xcol, ycol, title=None, text_format="{:.1%}", fig_size=8.0,
        bar_color="#4f4f4f"):

    if title:
        display(HTML("<h2 style='width:100%; text-align: center; padding: 20px; color: #3f3f3f'>" + title + "</h2>"))

    NOMINAL_ROWS = 20.0
    NOMINAL_WIDTH = 8.0
    size_coef = fig_size / NOMINAL_WIDTH 
    h_coeff = len(data.index) / NOMINAL_ROWS


    sns.set(style="whitegrid", font_scale=1.5 * size_coef, rc={
        'grid.color': "1",
        'xtick.color': "1",
        'font.sans-serif': ['Open Sans', 'sans-serif']
    })


    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(fig_size, fig_size * h_coeff))

    # Plot the total crashes
    sns.set_color_codes("pastel")
    sns.barplot(x=xcol, y=ycol, data=data,
                label="", color=bar_color)


    # Add a legend and informative axis label
    #ax.legend(ncol=2, loc="lower right", frameon=True)

    max_value = max(data[xcol])
    text_label_margin = max_value * .015 * size_coef


    ax.set(xlim=(0, None), ylabel="", xlabel="")
    ax.patch.set_alpha(0.0)

    for i, p in enumerate(ax.patches):
        width = p.get_width()
        # - .19 * size_coef
        ax.text(width + text_label_margin, p.get_y() + p.get_height()  , text_format.format(width), verticalalignment="bottom", fontsize=15.0 * size_coef)
        #ax.text(width + text_label_margin, p.get_y() + p.get_height() - .15  , text_format.format(width), size= 15 * size_coef)
        
    #if(title):
    #    sns.plt.title(title)

    sns.despine(left=True, bottom=True)
    #sns.plt.show()
