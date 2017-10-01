import sqlite3
import os
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.collections import LineCollection

# Database setup
dir_path = os.path.dirname(os.path.abspath(__file__))
db = sqlite3.connect(os.path.join(dir_path, 'data.db'))
cursor = db.cursor()

# Map setup
map = Basemap(projection='cyl',resolution='c')
map.drawmapboundary(fill_color='#424242')
map.fillcontinents(color='#636363')

def get_sublist(plots):
    current = []
    plots = iter(plots)
    try:
        while True:
            try:
                current.append(next(plots))
                if ((abs(abs(current[-1][0]) - abs(current[-2][0])) > 0.5 ) or
                   ((abs(abs(current[-1][1]) - abs(current[-2][1])) > 0.5 ) or
                   (abs(current[-1][1]) + abs(current[-2][1]) > 359.))):
                    last = current.pop()
                    yield current.copy()
                    current = [last]
                else:
                    pass
            except IndexError:
                pass
    except StopIteration:
        yield current

# Clear any empty data which will cause the program to crash
cursor.execute('DELETE FROM plots WHERE lat IS NULL OR lat = \'\';')
db.commit()

cursor.execute('SELECT DISTINCT vid FROM plots;')
vids = [x[0] for x in cursor.fetchall()]

for vid in vids:
    cursor.execute('SELECT lat, lon, alt FROM plots WHERE vid = ?;', (vid,))
    data = cursor.fetchall()
    data = list(get_sublist(data))

    for seg in data:
        lat, lon, alt = zip(*seg)
        alt = np.array(alt)

        points = np.array([lon, lat]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        lc = LineCollection(segments, cmap=plt.get_cmap('ocean'),
                            norm=plt.Normalize(-20., 60000.))
        lc.set_array(alt)
        lc.set_linewidth(1.0)

        plt.gca().add_collection(lc)

db.close()
plt.show()
