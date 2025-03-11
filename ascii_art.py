import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def load_and_clean_data(file_path, lat_col="latitude", lon_col="longitude"):
    """
    Load the CSV data from the given file path and remove rows with invalid latitude or longitude values.
    
    Parameters:
        file_path (str): The path to the CSV file.
        lat_col (str): Column name for latitude values.
        lon_col (str): Column name for longitude values.
        
    Returns:
        pd.DataFrame: Cleaned DataFrame with valid latitude and longitude values.
    """
    df = pd.read_csv(file_path)
    df = df[(df[lat_col].between(-90, 90)) & (df[lon_col].between(-180, 180))]
    return df

def transform_coordinates(df, lat_col="latitude", lon_col="longitude", map_width=110, map_height=100):
    """
    Transform longitude and latitude values to x, y coordinates suitable for a Mercator projection.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        lat_col (str): Column name for latitude values.
        lon_col (str): Column name for longitude values.
        map_width (int): The width of the map in arbitrary units.
        map_height (int): The height of the map in arbitrary units.
        
    Returns:
        pd.DataFrame: DataFrame with additional 'x' and 'y' columns.
    """
    # Convert longitude to x coordinate.
    df["x"] = (df[lon_col] + 180) * (map_width / 360)
    
    # Convert latitude to Mercator y coordinate.
    lat_rad = np.radians(df[lat_col])
    merc_n = np.log(np.tan((np.pi / 4) + (lat_rad / 2)))
    df["y"] = (map_height / 2) - (map_width * merc_n / (2 * np.pi))
    
    return df

def plot_scatter(df, plot_filename="scatter_plot.png", figsize=(12, 10), aspect=1.1):
    """
    Create a scatter plot from the x, y coordinates and save the plot as an image.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing 'x' and 'y' columns.
        plot_filename (str): Filename to save the plot image.
        figsize (tuple): Figure size for the plot.
        aspect (float): Aspect ratio of the plot.
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.scatter(df["x"], df["y"], alpha=0.5, edgecolors='k')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    ax.set_aspect(aspect)
    ax.invert_yaxis()
    
    plt.savefig(plot_filename, bbox_inches='tight', pad_inches=0, dpi=300)
    plt.close()

def image_to_ascii(image_path, new_width=100, ascii_chars=None):
    """
    Convert an image to its ASCII art representation, adjusting for character aspect ratio.
    
    Parameters:
        image_path (str): Path to the image file.
        new_width (int): New width for the ASCII art.
        ascii_chars (list): List of ASCII characters (from darkest to lightest).
        
    Returns:
        str: A string representing the ASCII art.
    """
    if ascii_chars is None:
        ascii_chars = ['@']
    
    # Load image and convert to grayscale.
    image = Image.open(image_path).convert("L")
    image.save("grayscale_img.png")
    orig_width, orig_height = image.size
    # Calculate the original image aspect ratio.
    aspect_ratio = orig_height / orig_width
    char_aspect_ratio = 0.55  
    new_height = int(new_width * aspect_ratio * char_aspect_ratio)
    image = image.resize((new_width, new_height))
    
    if len(ascii_chars) == 1:
        ascii_chars.append(" ")
    # Calculate the step value for mapping pixel values to characters.
    base = 255 / (len(ascii_chars))
    
    # Convert pixels to ASCII.
    pixels = image.getdata()
    ascii_str = "".join([ascii_chars[min(int(pixel / base), len(ascii_chars) - 1)] for pixel in pixels])
    ascii_image = "\n".join([ascii_str[i:i+new_width] for i in range(0, len(ascii_str), new_width)])
    
    return ascii_image

def save_ascii_art(ascii_art, filename="ascii_image.txt"):
    """
    Save the ASCII art string to a text file.
    
    Parameters:
        ascii_art (str): The ASCII art to be saved.
        filename (str): The name of the file where the ASCII art is saved.
    """
    with open(filename, "w") as f:
        f.write(ascii_art)

def parse_args():
    """
    Parse command-line arguments.
    
    Returns:
        Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Scatter Plot to ASCII Art Converter"
    )
    
    parser.add_argument(
        "--chars",
        type=str,
        default='@',
        help="Comma separated list of ASCII characters to use."
    )
    
    parser.add_argument(
        "--sea",
        action="store_true",
        help="If provided, adds a '.' character to the ASCII character list. Would fill the ocean with period character"
    )
    
    parser.add_argument(
        "--file_path",
        type=str,
        default="ukpostcodes.csv",
        help="Path to the CSV file. Default is 'ukpostalcodes.csv'."
    )
    
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Parse ASCII characters from the provided comma-separated string.
    ascii_chars = args.chars.split(',')
    if args.sea:
        ascii_chars.append('.')
    
    # Load and clean the data.
    df = load_and_clean_data(args.file_path, lat_col="latitude", lon_col="longitude")
    
    # Transform coordinates.
    df = transform_coordinates(df, lat_col="latitude", lon_col="longitude", map_width=110, map_height=100)
    
    # Create and save scatter plot.
    plot_filename = "scatter_plot.png"
    plot_scatter(df, plot_filename=plot_filename, figsize=(12, 10), aspect=1.1)
    
    # Convert the saved plot image to ASCII art.
    ascii_art = image_to_ascii(plot_filename, new_width=100, ascii_chars=ascii_chars)
    print(ascii_art)
    
    # Save the ASCII art to a text file.
    save_ascii_art(ascii_art, filename="ascii_image.txt")

if __name__ == "__main__":
    main()