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
- **`videos`**: Directory containing the videos generated from Veo3.
- **`mapping`**: CSV file containg the information about the cities.
- **`data`**: Directory containing the YOLO output.
- **`snaps`**: Directory containing the first frame from each generated video file.
- **`confidence`**: Sets the confidence threshold parameter for YOLO.
- **`model`**: Specifies the YOLO model to use; supported/tested versions include `v8x` and `v11x`.
- **`tracking_mode`**: Configures YOLO for object tracking.
- **`always_analyse`**: Always conduct analysis even when pickle files are present (good for testing).
- **`display_frame_tracking`**: Displays the frame tracking during analysis.
- **`save_annotated_img`**: Saves the annotated frames produced by YOLO.
- **`save_tracked_img`**: Saves the tracked frames produced by YOLO.
- **`delete_labels`**: Deletes label files from YOLO output.
- **`delete_frames`**: Deletes frames from YOLO output.
- **`delete_runs_files`**: Deletes files containing YOLO output after analysis.
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
Distribution of objects detected in the videos, first grouped by continent and then sorted by average values within each continent.

### Sound from the videos of different cities
[![Sound from the videos](figures/sound.png?raw=true)](https://htmlpreview.github.io/?https://github.com/Shaadalam9/llm-traffic-scene/blob/main/figures/sound.html)
Sound from different countries (measured in dB).

### First frame from Veo 3 generated videos

#### Africa

<table width="100%">
  <tr>
    <td align="center" width="25%"><img src="readme/Cairo.png?raw=true" alt="Cairo" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Kampala.png?raw=true" alt="Kampala" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Accra.png?raw=true" alt="Accra" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Algiers.png?raw=true" alt="Algiers" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Cairo</b></td>
    <td align="center"><b>Kampala</b></td>
    <td align="center"><b>Accra</b></td>
    <td align="center"><b>Algiers</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Lagos.png?raw=true" alt="Lagos" width="220"/></td>
    <td align="center"><img src="readme/Tunis.png?raw=true" alt="Tunis" width="220"/></td>
    <td align="center"><img src="readme/Asmara.png?raw=true" alt="Asmara" width="220"/></td>
    <td align="center"><img src="readme/Banjul.png?raw=true" alt="Banjul" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Lagos</b></td>
    <td align="center"><b>Tunis</b></td>
    <td align="center"><b>Asmara</b></td>
    <td align="center"><b>Banjul</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Bangui.png?raw=true" alt="Bangui" width="220"/></td>
    <td align="center"><img src="readme/N' Djamena.png?raw=true" alt="N'Djamena" width="220"/></td>
    <td align="center"><img src="readme/Kinshasa.png?raw=true" alt="Kinshasa" width="220"/></td>
    <td align="center"><img src="readme/Zanzibar.png?raw=true" alt="Zanzibar" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Bangui</b></td>
    <td align="center"><b>N'Djamena</b></td>
    <td align="center"><b>Kinshasa</b></td>
    <td align="center"><b>Zanzibar</b></td>
  </tr>
</table>


#### Asia

<table width="100%">
  <tr>
    <td align="center" width="25%"><img src="readme/Kabul.png?raw=true" alt="Kabul" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Dhaka.png?raw=true" alt="Dhaka" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Beijing.png?raw=true" alt="Beijing" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Karachi.png?raw=true" alt="Karachi" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Kabul</b></td>
    <td align="center"><b>Dhaka</b></td>
    <td align="center"><b>Beijing</b></td>
    <td align="center"><b>Karachi</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Tel Aviv.png?raw=true" alt="Tel Aviv" width="220"/></td>
    <td align="center"><img src="readme/Jerusalem.png?raw=true" alt="Jerusalem" width="220"/></td>
    <td align="center"><img src="readme/Tehran.png?raw=true" alt="Tehran" width="220"/></td>
    <td align="center"><img src="readme/Muscat.png?raw=true" alt="Muscat" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Tel Aviv</b></td>
    <td align="center"><b>Jerusalem</b></td>
    <td align="center"><b>Tehran</b></td>
    <td align="center"><b>Muscat</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Damascus.png?raw=true" alt="Damascus" width="220"/></td>
    <td align="center"><img src="readme/Tokyo.png?raw=true" alt="Tokyo" width="220"/></td>
    <td align="center"><img src="readme/Seoul.png?raw=true" alt="Seoul" width="220"/></td>
    <td align="center"><img src="readme/Pyongyang.png?raw=true" alt="Pyongyang" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Damascus</b></td>
    <td align="center"><b>Tokyo</b></td>
    <td align="center"><b>Seoul</b></td>
    <td align="center"><b>Pyongyang</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Colombo.png?raw=true" alt="Colombo" width="220"/></td>
    <td align="center"><img src="readme/Kathmandu.png?raw=true" alt="Kathmandu" width="220"/></td>
    <td align="center"><img src="readme/Baku.png?raw=true" alt="Baku" width="220"/></td>
    <td align="center"><img src="readme/Bangkok.png?raw=true" alt="Bangkok" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Colombo</b></td>
    <td align="center"><b>Kathmandu</b></td>
    <td align="center"><b>Baku</b></td>
    <td align="center"><b>Bangkok</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Kuala Lumpur.png?raw=true" alt="Kuala Lumpur" width="220"/></td>
    <td align="center"><img src="readme/Dubai.png?raw=true" alt="Dubai" width="220"/></td>
    <td align="center"><img src="readme/Doha.png?raw=true" alt="Doha" width="220"/></td>
    <td align="center"></td>
  </tr>
  <tr>
    <td align="center"><b>Kuala Lumpur</b></td>
    <td align="center"><b>Dubai</b></td>
    <td align="center"><b>Doha</b></td>
    <td align="center"></td>
  </tr>
</table>

#### Europe

<table width="100%">
  <tr>
    <td align="center" width="25%"><img src="readme/Amsterdam.png?raw=true" alt="Amsterdam" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Paris.png?raw=true" alt="Paris" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Oslo.png?raw=true" alt="Oslo" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Tirana.png?raw=true" alt="Tirana" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Amsterdam</b></td>
    <td align="center"><b>Paris</b></td>
    <td align="center"><b>Oslo</b></td>
    <td align="center"><b>Tirana</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Brussels.png?raw=true" alt="Brussels" width="220"/></td>
    <td align="center"><img src="readme/Sofia.png?raw=true" alt="Sofia" width="220"/></td>
    <td align="center"><img src="readme/Berlin.png?raw=true" alt="Berlin" width="220"/></td>
    <td align="center"><img src="readme/Moscow.png?raw=true" alt="Moscow" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Brussels</b></td>
    <td align="center"><b>Sofia</b></td>
    <td align="center"><b>Berlin</b></td>
    <td align="center"><b>Moscow</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Kyiv.png?raw=true" alt="Kyiv" width="220"/></td>
    <td align="center"><img src="readme/London.png?raw=true" alt="London" width="220"/></td>
    <td align="center"><img src="readme/Rome.png?raw=true" alt="Rome" width="220"/></td>
    <td align="center"><img src="readme/Barcelona.png?raw=true" alt="Barcelona" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Kyiv</b></td>
    <td align="center"><b>London</b></td>
    <td align="center"><b>Rome</b></td>
    <td align="center"><b>Barcelona</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Zurich.png?raw=true" alt="Zurich" width="220"/></td>
    <td align="center"><img src="readme/Stockholm.png?raw=true" alt="Stockholm" width="220"/></td>
    <td align="center"><img src="readme/Copenhagen.png?raw=true" alt="Copenhagen" width="220"/></td>
    <td align="center"><img src="readme/Helsinki.png?raw=true" alt="Helsinki" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Zurich</b></td>
    <td align="center"><b>Stockholm</b></td>
    <td align="center"><b>Copenhagen</b></td>
    <td align="center"><b>Helsinki</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Warsaw.png?raw=true" alt="Warsaw" width="220"/></td>
    <td align="center"><img src="readme/Lisbon.png?raw=true" alt="Lisbon" width="220"/></td>
    <td align="center"><img src="readme/Athens.png?raw=true" alt="Athens" width="220"/></td>
    <td align="center"><img src="readme/Dubrovnik.png?raw=true" alt="Dubrovnik" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Warsaw</b></td>
    <td align="center"><b>Lisbon</b></td>
    <td align="center"><b>Athens</b></td>
    <td align="center"><b>Dubrovnik</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Vatican City.png?raw=true" alt="Vatican City" width="220"/></td>
    <td align="center"></td>
    <td align="center"></td>
    <td align="center"></td>
  </tr>
  <tr>
    <td align="center"><b>Vatican City</b></td>
    <td align="center"></td>
    <td align="center"></td>
    <td align="center"></td>
  </tr>
</table>

#### North America

<table width="100%">
  <tr>
    <td align="center" width="25%"><img src="readme/New York City.png?raw=true" alt="New York" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Toronto.png?raw=true" alt="Toronto" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Mexico City.png?raw=true" alt="Mexico City" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Havana.png?raw=true" alt="Havana" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>New York</b></td>
    <td align="center"><b>Toronto</b></td>
    <td align="center"><b>Mexico City</b></td>
    <td align="center"><b>Havana</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Panama City.png?raw=true" alt="Panama City" width="220"/></td>
    <td align="center"></td>
    <td align="center"></td>
    <td align="center"></td>
  </tr>
  <tr>
    <td align="center"><b>Panama City</b></td>
    <td align="center"></td>
    <td align="center"></td>
    <td align="center"></td>
  </tr>
</table>

#### Oceania

<table width="100%">
  <tr>
    <td align="center" width="25%"><img src="readme/Auckland.png?raw=true" alt="Auckland" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Suva.png?raw=true" alt="Suva" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Funafuti.png?raw=true" alt="Funafuti" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Bali.png?raw=true" alt="Bali" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Auckland</b></td>
    <td align="center"><b>Suva</b></td>
    <td align="center"><b>Funafuti</b></td>
    <td align="center"><b>Bali</b></td>
  </tr>
</table>


#### South America

<table width="100%">
  <tr>
    <td align="center" width="25%"><img src="readme/Rio de Janeiro.png?raw=true" alt="Rio de Janeiro" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Buenos Aires.png?raw=true" alt="Buenos Aires" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Lima.png?raw=true" alt="Lima" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Santiago.png?raw=true" alt="Santiago" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Rio de Janeiro</b></td>
    <td align="center"><b>Buenos Aires</b></td>
    <td align="center"><b>Lima</b></td>
    <td align="center"><b>Santiago</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Quito.png?raw=true" alt="Quito" width="220"/></td>
    <td align="center"><img src="readme/Montevideo.png?raw=true" alt="Montevideo" width="220"/></td>
    <td align="center"><img src="readme/Asuncion.png?raw=true" alt="Asunción" width="220"/></td>
    <td align="center"></td>
  </tr>
  <tr>
    <td align="center"><b>Quito</b></td>
    <td align="center"><b>Montevideo</b></td>
    <td align="center"><b>Asunción</b></td>
    <td align="center"></td>
  </tr>
</table>



## Contact
If you have any questions or suggestions, feel free to reach out to md_shadab_alam@outlook.com or pavlo.bazilinskyy@gmail.com.
