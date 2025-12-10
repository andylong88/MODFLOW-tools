import os
import numpy as np
import matplotlib.pyplot as plt
import flopy
import pickle

# NOTE: run import_model.py once before running this script.

# Set parameters
modflow_layer = 7
layer_index = modflow_layer - 1 # Python counts from 0
interval = 100 # Set the contour interval
min_threshold = 0  # Choose your minimum allowed head for plots
max_threshold = 1800  # Choose your maximum allowed head for plots

# -------------------------------------------------------------------
# 1. Open the imported model (ml) from import_model.py
# -------------------------------------------------------------------
with open("SES_ss_model.pkl", "rb") as f:
    ml = pickle.load(f)

# -------------------------------------------------------------------
# 2. Load heads from the MODFLOW binary head file
# -------------------------------------------------------------------
hds_path = os.path.join("../../../output/output.SES_ss", "SES_ss.hds")  # adjust filename if needed
hds = flopy.utils.HeadFile(hds_path)

times = hds.get_times()
print("Available times:", times)
head = hds.get_data(totim=times[-1])   # last time step

print("Head array shape:", head.shape)

# -------------------------------------------------------------------
# 3. Select layer and compute contour levels
# -------------------------------------------------------------------
# layer_index = 8     # layer 9 in modflow
head2d = head[layer_index, :, :]

vmin = np.nanmin(head2d)
vmax = np.nanmax(head2d)
print("Layer", layer_index + 1, "head range:", vmin, vmax)

vmax = min(vmax, max_threshold)
vmin = max(vmin, min_threshold)
print("Layer", layer_index + 1, "new head range with thresholds:", vmin, vmax)

# If vmin == vmax, there is nothing to contour
if np.isclose(vmin, vmax):
    raise ValueError("Selected layer has uniform head; no contours can be drawn.")

# -------------------------------------------------------------------
# 4. Set up map view and plot
# -------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect("equal")

mapview = flopy.plot.PlotMapView(model=ml, layer=layer_index)

# Filled head colors
cf = mapview.plot_array(head2d, alpha=0.9, cmap="viridis")

# enforce same limits as contours
cf.set_clim(vmin, vmax)   # where vmax already includes your threshold
# or, if you only cap the top:
# cf.set_clim(vmin, max_threshold)

# Establish the contour levels
start = np.floor(vmin / interval) * interval
end   = np.ceil(vmax / interval) * interval
levels = np.arange(start, end + interval, interval)

# Alternatively set the number of contours within the range
# ncontours = 20 
# levels = np.linspace(vmin, vmax, ncontours)

contours = mapview.contour_array(
    head2d,
    levels=levels,
    colors="white",      # high contrast on most colormaps
    linewidths=1.0
)

mapview.plot_grid(colors="k", alpha=0.2)

plt.colorbar(cf, ax=ax, label="Head (m)")
plt.clabel(contours, inline=1, fontsize=8, colors="white")
ax.set_title(f"Head contours, layer {layer_index + 1}")

plt.tight_layout()
fig.savefig("heads_layer9.png", dpi=300)
plt.show()

