import base64
import io
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.patches import RegularPolygon


def gen_hex_plot(data: list = None, side: str = 'top') -> str:

    _num_rows = 5
    _num_cols = 8
    if not data:
        temperature_values = [i for i in range(20, 43, 1)]
    else:
        temperature_values = data
    # create figure and axe
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')

    # hexagon centre coordinates calculation
    coords = []
    radius = 1
    x_init = radius * np.sqrt(3) / 2
    y_init = radius
    dx = radius * np.sqrt(3)
    dy = radius * 1.5
    for row in range(_num_rows):
        for column in range(_num_cols):
            x = x_init + column * dx
            y = y_init + row * dy
            if row % 2 == 1:
                x += x_init
            coords.append([x, y])
    bottom_heatsink_coords_index = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 18, 19, 20, 21, 22, 27, 28, 29, 37]
    top_heatsink_coords_index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 25, 26, 27, 34]
    if side == 'top':
        heatsink_coords = [coords[i] for i in top_heatsink_coords_index]
    elif side == 'bottom':
        heatsink_coords = [coords[i] for i in bottom_heatsink_coords_index]
    else:
        raise 'side can be "top" or "bottom"'
        # return None
    # add hexagons with own color
    min_temp = min(temperature_values)
    max_temp = max(temperature_values)
    norm = Normalize(vmin=min_temp, vmax=max_temp)
    for center, temperature in zip(heatsink_coords, temperature_values):
        hexagon = RegularPolygon(
            center,
            numVertices=6,
            radius=radius,
            edgecolor='black',
            facecolor=plt.cm.plasma(norm(temperature)))  # normalization
        ax.add_patch(hexagon)
        ax.text(center[0], center[1], str(temperature), ha='center', va='center', color='black', fontsize=6)

    # shift plot from axis
    ax.set_xlim(-0.5, _num_cols * dx + x_init + 0.5)
    ax.set_ylim(-0.5, _num_rows * dy + y_init + 0.5)
    ax.axis('off')  # turn off axis

    # add colorbar
    sm = plt.cm.ScalarMappable(cmap='plasma')
    sm.set_array(temperature_values)
    plt.colorbar(sm, ax=ax, orientation='vertical', label=f'Temperature {side} side (°C)')

    if __name__ == '__main__':
        fig.show()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    png_data = base64.b64encode(buf.read()).decode()
    return png_data


if __name__ == '__main__':
    gen_hex_plot(side='bottom')
