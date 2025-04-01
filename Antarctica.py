import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def plot_antarctica_basemap():
    """
    Creates a minimal basemap of Antarctica using a South Polar Stereographic projection.
    The map includes only coastlines.
    """
    # Use a South Polar Stereographic projection
    projection = ccrs.SouthPolarStereo()

    # Create figure and axis with the defined projection
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': projection})

    # Add coastlines
    ax.add_feature(cfeature.COASTLINE, linewidth=1, edgecolor="black")

    # Set the extent to show Antarctica properly
    ax.set_extent([-180, 180, -90, -60], crs=ccrs.PlateCarree())

    # Add gridlines (latitude circles & meridians)
    gl = ax.gridlines(draw_labels=True, linestyle="--", alpha=0.5)
    gl.top_labels = False  # Hide labels at the top
    gl.right_labels = False  # Hide labels on the right

    # Set title
    ax.set_title("Antarctica Basemap (South Polar Stereographic)")

    # Show the map
    plt.show()

# Run the function
plot_antarctica_basemap()