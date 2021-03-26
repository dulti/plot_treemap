# @dulti
# usalev@gmail.com

def plot_treemap(data, x, y, annot=True):
    """
    Plots an R-like treemap diagram.
    Plots a visual relationship of two independent categorical variables.
    X and Y axes show proportions of the size of the respective variables
    by categories. Resulting squares area can be used to compare the size of
    the groups in the intersection of categories.
    Resembles a stacked barchart, but the width of the bars shows the relative
    size of the x-values.
    
    Keyword arguments:
    data  -- a pandas dataframe
    x, y  -- column names. Have to be converted to type 'category';
            no type-checking is done.
    
    annot -- display data absolute values in the squares
    
    Строит график наподобии TreeMap в R. По осям x и y отложены пропорции данных в целом (от 0 до 1).
    Аргументы:
    data - датафрейм pandas с данными
    x - данные для построения на оси x (название столбца в data), строка
    y - данные для построения на оси y, (название столбца в data), строка
    annot=True - отображать подписи абсолютных значений в квадратах.
    """
    
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import pandas as pd
    import numpy as np
    
    # group the dataframe
    df_plot = data.groupby([x, y]).size().reset_index().pivot(index=x, columns=y, values=0)
    
    # calculate additional values
    num_cols, num_bars = df_plot.shape
    sum_cols = df_plot.sum(axis=1).values
    cols_ratio = sum_cols / sum(sum_cols)
    cols_ratio_cum = np.cumsum(cols_ratio)
    
    # set the colormap
    colors=np.random.rand(num_cols)
    cmap = plt.cm.Set2
    c = cmap(colors)
    
    # create subplots()
    _, ax = plt.subplots()
    
    # draw rectangles
    for num_col in range(num_cols):
        cur_row = df_plot.iloc[num_col, :].values
        cur_row_ratio = cur_row / sum(cur_row)
        cur_row_ratio_cum = np.cumsum(cur_row_ratio)
        for num_bar in range(num_bars): 
            rect = patches.Rectangle((cols_ratio_cum[num_col] - cols_ratio[num_col], 1 - cur_row_ratio_cum[num_bar]), 
                                     cols_ratio[num_col], cur_row_ratio[num_bar], 
                                     linewidth=1, edgecolor='k', facecolor=c[num_col], \
                                     alpha=((num_bar + 1) * (1 / num_bars)), fill=True)      
            ax.add_patch(rect)
            
            # if annot=True, draw the values
            if annot:
                text_x = rect.get_width() / 2 + rect.get_x()
                text_y = rect.get_height() / 2 + rect.get_y()
                plt.text(text_x, text_y, df_plot.iloc[num_col, num_bar], ha='center', va='center')
    
    # create labels
    axT = ax.twinx()
    axT.set_yticks([1 - (y1 + (y2 - y1) / 2) for (y1, y2) in zip(np.insert(cur_row_ratio_cum, 0, 0), cur_row_ratio_cum)])
    axT.set_yticklabels(df_plot.columns)
    axR = ax.twiny()
    axR.set_xticks([x1 + (x2 - x1) / 2 for (x1, x2) in zip(np.insert(cols_ratio_cum, 0, 0), cols_ratio_cum)])
    axR.set_xticklabels(df_plot.index)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    plt.title(f'Distribution of {y} relative to {x}.')
    plt.show()