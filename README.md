# llm-traffic-scene

## Running analysis code
Tested with Python 3.9.23. To setup the environment run these two commands in a parent folder of the downloaded repository (replace `/` with `\` and possibly add `--user` if on Windows:

**Step 1:**
Clone the repository
```command line
git clone https://github.com/Shaadalam9/llm-traffic-scene
```

**Step 2:**
Create a new virtual environment
```command line
python -m venv venv
```

**Step 3:**
Activate the virtual environment
```command line
source venv/bin/activate
```

On Windows use
```command line
venv\Scripts\activate
```

**Step 4:**
Install dependencies
```command line
pip install -r requirements.txt
```

**Step 5:**
Ensure you have the required datasets in the data/ directory, including the mapping.csv file.

**Step 6:**
Run the code:
```command line
python3 analysis.py
```

### Configuration of project
Configuration of the project needs to be defined in `config`. Please use the `default.config` file for the required structure of the file. If no custom config file is provided, `default.config` is used. The config file has the following parameters:
- **`videos`**: Directories containing the videos generated from Veo3.
- **`prediction_mode`**: Configures YOLO for object detection.
- **`always_analyse`**: Always conduct analysis even when pickle files are present (good for testing).
- **`display_frame_tracking`**: Displays the frame tracking during analysis.
- **`save_annotated_img`**: Saves the annotated frames produced by YOLO.
- **`delete_labels`**: Deletes label files from YOLO output.
- **`delete_frames`**: Deletes frames from YOLO output.
- **`delete_runs_files`**: Deletes files containing YOLO output after analysis.
- **`model`**: Specifies the YOLO model to use; supported/tested versions include `v8x` and `v11x`.
- **`confidence`**: Sets the confidence threshold parameter for YOLO.
- **`font_family`**: Specifies the font family to be used in outputs.
- **`font_size`**: Specifies the font size to be used in outputs.
- **`plotly_template`**: Defines the template for Plotly figures.
- **`logger_level`**: Level of console output. Can be: debug, info, warning, error.

### Detection of objects
[![Alphabetical Sorting](figures/stack_alphabetical.png?raw=true)](https://htmlpreview.github.io/?https://github.com/Shaadalam9/llm-traffic-scene/blob/main/figures/stack_alphabetical.html)
Distribution of different objects detected in the videos, sorted in alphabetical order..

[![Average Value Sorting](figures/stack_average.png?raw=true)](https://htmlpreview.github.io/?https://github.com/Shaadalam9/llm-traffic-scene/blob/main/figures/stack_average.html)
Distribution of objects detected in the videos, sorted by the average values of object counts..

[![Continent and Average Value Sorting](figures/continent_average.png?raw=true)](https://htmlpreview.github.io/?https://github.com/Shaadalam9/llm-traffic-scene/blob/main/figures/continent_average.html)
Distribution of objects detected in the videos, first grouped by continent and then sorted by average values within each continent..


## Contact
If you have any questions or suggestions, feel free to reach out to md_shadab_alam@outlook.com or pavlo.bazilinskyy@gmail.com.
