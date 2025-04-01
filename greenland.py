# mapping for Greenland basemap
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def plot_greenland_basemap():
    """
    Creates a minimal basemap of Greenland using a Polar Stereographic projection.
    The map includes only coastlines (no colors or filled land areas).
    """
    # Define the projection: Polar Stereographic centered on Greenland
    projection = ccrs.Stereographic(central_longitude=-45, central_latitude=75)

    # Create the figure and axis with the defined projection
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': projection})

    # Add coastlines (no land shading)
    ax.add_feature(cfeature.COASTLINE, linewidth=1, edgecolor="black")

    # Set the map extent to focus on Greenland
    ax.set_extent([-75, -10, 60, 85], crs=ccrs.PlateCarree())

    # Add gridlines for reference
    gl = ax.gridlines(draw_labels=True, linestyle="--", alpha=0.5)
    gl.top_labels = False  # Hide top labels
    gl.right_labels = False  # Hide right-side labels

    # Set title
    ax.set_title("Greenland (Polar Stereographic)")

    # Show the map
    plt.show()

