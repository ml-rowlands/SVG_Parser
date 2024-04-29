import streamlit as st 
import xml.etree.ElementTree as ET

st.set_page_config(layout="wide", page_title="SVG Shape Counter")

st.write("## Count the Number of Shapes and Colors in your SVG File")
st.write(
    "Try uploading a SVG file to get a count of the number of distinct shapes and colors used in the file. :grin:"
)
st.sidebar.write("## Upload :gear:")

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def parse_svg(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Collect all path elements
    paths = root.findall('.//{http://www.w3.org/2000/svg}path')
    
    unique_colors = set()
    unique_shapes = set()
    
    for path in paths:
        # Get the 'd' attribute to identify unique shapes
        shape = path.get('d')
        if shape:
            unique_shapes.add(shape)
        
        # Get fill and stroke colors
        fill = path.get('fill')
        stroke = path.get('stroke')
        
        if fill:
            unique_colors.add(fill)
        if stroke:
            unique_colors.add(stroke)

    none_null_cols = [x for x in unique_colors if x != 'none']
    return len(unique_shapes), list(unique_colors), len(none_null_cols)



col1, col2 = st.columns(2)
my_upload = st.sidebar.file_uploader("Upload a SVG File", type=["svg"])

if my_upload is not None:
    if my_upload.size > MAX_FILE_SIZE:
        st.error("The uploaded file is too large. Please upload a file smaller than 10MB.")
    else:
        shape_count, colors, non_none_color_count = parse_svg(my_upload)
        st.write(f"Number of unique shapes: {shape_count}")
        st.write(f"Unique colors used: {colors}")
        st.write(f'Number of unique, non-"none", colors: {non_none_color_count}')
else:
    #parse_svg('EarthyElegance_Abstract1_4x4.svg')
    st.write("Please upload a file to analyze.")