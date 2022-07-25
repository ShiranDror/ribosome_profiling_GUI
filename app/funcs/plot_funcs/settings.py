import matplotlib.pyplot as plt



def plot_settings():
    # this means the font must be present on this computer to view the text in the svg output
    # this also means that the text is output as <text> which can later be modified..
    plt.rcParams['svg.fonttype'] = 'none'

    plt.rcParams['font.family'] = 'Roboto'
    #plt.rcParams['font.family'] = 'sans-serif'
    # plt.rcParams['font.sans-serif'] = ["Roboto"]#,'Roboto-Regular','Roboto-Italic','Roboto-Bold'] # ['comics san', 'Roboto', 'Roboto-Regular','Roboto-Italic','Roboto-Bold', 'Microsoft Sans Serif','Calibri','Verdana','Lucida Grande','Tahoma' ] #['Helvetica','texgyreheroscn','texgyreheroscn-regular']
    #matplotlib("font", **{"sans-serif": ["Roboto"]})
    SMALL_SIZE = 12
    MEDIUM_SIZE = 15
    BIGGER_SIZE = 20
    FONT_WEIGHT = 800

    # controls default text sizes
    plt.rcParams['font.size'] = SMALL_SIZE
    # fontsize of the axes title
    plt.rcParams['axes.titlesize'] = BIGGER_SIZE
    # fontsize of the x and y labels
    plt.rcParams['axes.labelsize'] = MEDIUM_SIZE
    # fontsize of the tick labels
    plt.rcParams['xtick.labelsize'] = SMALL_SIZE
    # fontsize of the tick labels
    plt.rcParams['ytick.labelsize'] = SMALL_SIZE
    plt.rcParams['legend.fontsize'] = SMALL_SIZE    # legend fontsize
    # fontsize of the figure title
    plt.rcParams['figure.titlesize'] = BIGGER_SIZE

    plt.rcParams['font.weight'] = FONT_WEIGHT
    plt.rcParams['figure.titleweight'] = FONT_WEIGHT
    plt.rcParams['axes.titleweight'] = FONT_WEIGHT
    plt.rcParams['xtick.major.size'] = 5
    plt.rcParams['xtick.major.width'] = 1
    plt.rcParams['ytick.major.size'] = 5
    plt.rcParams['ytick.major.width'] = 1