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
    <td align="center" width="25%"><img src="readme/Accra_Ghana.png?raw=true" alt="Accra_Ghana" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Algiers_Algeria.png?raw=true" alt="Algiers_Algeria" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Asmara_Eritrea.png?raw=true" alt="Asmara_Eritrea" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Banjul_Gambia.png?raw=true" alt="Banjul_Gambia" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Accra (Ghana)</b></td>
    <td align="center"><b>Algiers (Algeria)</b></td>
    <td align="center"><b>Asmara (Eritrea)</b></td>
    <td align="center"><b>Banjul (Gambia)</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Bangui_CAR.png?raw=true" alt="Bangui_CAR" width="220"/></td>
    <td align="center"><img src="readme/Cairo_Egypt.png?raw=true" alt="Cairo_Egypt" width="220"/></td>
    <td align="center"><img src="readme/Kampala_Uganda.png?raw=true" alt="Kampala_Uganda" width="220"/></td>
    <td align="center"><img src="readme/Kinshasa_DRC.png?raw=true" alt="Kinshasa_DRC" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Bangui (Central African Republic)</b></td>
    <td align="center"><b>Cairo (Egypt)</b></td>
    <td align="center"><b>Kampala (Uganda)</b></td>
    <td align="center"><b>Kinshasa (DR Congo)</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Lagos_Nigeria.png?raw=true" alt="Lagos_Nigeria" width="220"/></td>
    <td align="center"><img src="readme/N'Djamena_Chad.png?raw=true" alt="N'Djamena_Chad" width="220"/></td>
    <td align="center"><img src="readme/Tunis_Tunisia.png?raw=true" alt="Tunis_Tunisia" width="220"/></td>
    <td align="center"><img src="readme/Zanzibar_Tanzania.png?raw=true" alt="Zanzibar_Tanzania" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Lagos (Nigeria)</b></td>
    <td align="center"><b>N'Djamena (Chad)</b></td>
    <td align="center"><b>Tunis (Tunisia)</b></td>
    <td align="center"><b>Zanzibar (Tanzania)</b></td>
  </tr>
</table>


#### Asia

<table width="100%">
  <tr>
    <td align="center" width="25%"><img src="readme/Almaty_Kazakhstan.png?raw=true" alt="Almaty_Kazakhstan" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Baghdad_Iraq.png?raw=true" alt="Baghdad_Iraq" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Baku_Azerbaijan.png?raw=true" alt="Baku_Azerbaijan" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Beijing_China.png?raw=true" alt="Beijing_China" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Almaty (Kazakhstan)</b></td>
    <td align="center"><b>Baghdad (Iraq)</b></td>
    <td align="center"><b>Baku (Azerbaijan)</b></td>
    <td align="center"><b>Beijing (China)</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Bangkok_Thailand.png?raw=true" alt="Bangkok_Thailand" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Colombo_SriLanka.png?raw=true" alt="Colombo_SriLanka" width="220"/></td>
    <td align="center"><img src="readme/Damascus_Syria.png?raw=true" alt="Damascus_Syria" width="220"/></td>
    <td align="center"><img src="readme/Dhaka_Bangladesh.png?raw=true" alt="Dhaka_Bangladesh" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Bangkok (Thailand)</b></td>
    <td align="center"><b>Colombo (Sri Lanka)</b></td>
    <td align="center"><b>Damascus (Syria)</b></td>
    <td align="center"><b>Dhaka (Bangladesh)</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Doha_Qatar.png?raw=true" alt="Doha_Qatar" width="220"/></td>
    <td align="center"><img src="readme/Dubai_UAE.png?raw=true" alt="Dubai_UAE" width="220"/></td>
    <td align="center"><img src="readme/Istanbul_Turkey.png?raw=true" alt="Istanbul_Turkey" width="220"/></td>
    <td align="center"><img src="readme/Jakarta_Indonesia.png?raw=true" alt="Jakarta_Indonesia" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Doha (Qatar)</b></td>
    <td align="center"><b>Dubai (UAE)</b></td>
    <td align="center"><b>Istanbul (Turkey)</b></td>
    <td align="center"><b>Jakarta (Indonesia)</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Kabul_Afghanistan.png?raw=true" alt="Kabul_Afghanistan" width="220"/></td>
    <td align="center"><img src="readme/Karachi_Pakistan.png?raw=true" alt="Karachi_Pakistan" width="220"/></td>
    <td align="center"><img src="readme/Kathmandu_Nepal.png?raw=true" alt="Kathmandu_Nepal" width="220"/></td>
    <td align="center"><img src="readme/KualaLumpur_Malaysia.png?raw=true" alt="KualaLumpur_Malaysia" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Kabul (Afghanistan)</b></td>
    <td align="center"><b>Karachi (Pakistan)</b></td>
    <td align="center"><b>Kathmandu (Nepal)</b></td>
    <td align="center"><b>Kuala Lumpur (Malaysia)</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Malé_Maldives.png?raw=true" alt="Malé_Maldives" width="220"/></td>
    <td align="center"><img src="readme/Mumbai_India.png?raw=true" alt="Mumbai_India" width="220"/></td>
    <td align="center"><img src="readme/Muscat_Oman.png?raw=true" alt="Muscat_Oman" width="220"/></td>
    <td align="center"><img src="readme/PhnomPenh_Cambodia.png?raw=true" alt="PhnomPenh_Cambodia" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Malé (Maldives)</b></td>
    <td align="center"><b>Mumbai (India)</b></td>
    <td align="center"><b>Muscat (Oman)</b></td>
    <td align="center"><b>Phnom Penh (Cambodia)</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Pyongyang_NorthKorea.png?raw=true" alt="Pyongyang_NorthKorea" width="220"/></td>
    <td align="center"><img src="readme/Riyadh_SaudiArabia.png?raw=true" alt="Riyadh_SaudiArabia" width="220"/></td>
    <td align="center"><img src="readme/Seoul_SouthKorea.png?raw=true" alt="Seoul_SouthKorea" width="220"/></td>
    <td align="center"><img src="readme/Tehran_Iran.png?raw=true" alt="Tehran_Iran" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Pyongyang (North Korea)</b></td>
    <td align="center"><b>Riyadh (Saudi Arabia)</b></td>
    <td align="center"><b>Seoul (South Korea)</b></td>
    <td align="center"><b>Tehran (Iran)</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/TelAviv_Israel.png?raw=true" alt="TelAviv_Israel" width="220"/></td>
    <td align="center"><img src="readme/Tokyo_Japan.png?raw=true" alt="Tokyo_Japan" width="220"/></td>
    <td align="center"><img src="readme/Yangon_Myanmar.png?raw=true" alt="Yangon_Myanmar" width="220"/></td>
    <td align="center"></td>
  </tr>
  <tr>
    <td align="center"><b>Tel Aviv (Israel)</b></td>
    <td align="center"><b>Tokyo (Japan)</b></td>
    <td align="center"><b>Yangon (Myanmar)</b></td>
    <td align="center"></td>
  </tr>
</table>



#### Europe

<table width="100%">
  <tr>
    <td align="center" width="25%"><img src="readme/Amsterdam_The Netherlands.png?raw=true" alt="Amsterdam_The Netherlands" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Athens_Greece.png?raw=true" alt="Athens_Greece" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Barcelona_Spain.png?raw=true" alt="Barcelona_Spain" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Berlin_Germany.png?raw=true" alt="Berlin_Germany" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Amsterdam (The Netherlands)</b></td>
    <td align="center"><b>Athens (Greece)</b></td>
    <td align="center"><b>Barcelona (Spain)</b></td>
    <td align="center"><b>Berlin (Germany)</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Brussels_Belgium.png?raw=true" alt="Brussels_Belgium" width="220"/></td>
    <td align="center"><img src="readme/Copenhagen_Denmark.png?raw=true" alt="Copenhagen_Denmark" width="220"/></td>
    <td align="center"><img src="readme/Dubrovnik_Croatia.png?raw=true" alt="Dubrovnik_Croatia" width="220"/></td>
    <td align="center"><img src="readme/Helsinki_Finland.png?raw=true" alt="Helsinki_Finland" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Brussels (Belgium)</b></td>
    <td align="center"><b>Copenhagen (Denmark)</b></td>
    <td align="center"><b>Dubrovnik (Croatia)</b></td>
    <td align="center"><b>Helsinki (Finland)</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Kyiv_Ukraine.png?raw=true" alt="Kyiv_Ukraine" width="220"/></td>
    <td align="center"><img src="readme/Lisbon_Portugal.png?raw=true" alt="Lisbon_Portugal" width="220"/></td>
    <td align="center"><img src="readme/London_United Kingdom.png?raw=true" alt="London_United Kingdom" width="220"/></td>
    <td align="center"><img src="readme/Moscow_Russia.png?raw=true" alt="Moscow_Russia" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Kyiv (Ukraine)</b></td>
    <td align="center"><b>Lisbon (Portugal)</b></td>
    <td align="center"><b>London (United Kingdom)</b></td>
    <td align="center"><b>Moscow (Russia)</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Oslo_Norway.png?raw=true" alt="Oslo_Norway" width="220"/></td>
    <td align="center"><img src="readme/Paris_France.png?raw=true" alt="Paris_France" width="220"/></td>
    <td align="center"><img src="readme/Rome_Italy.png?raw=true" alt="Rome_Italy" width="220"/></td>
    <td align="center"><img src="readme/Sofia_Bulgaria.png?raw=true" alt="Sofia_Bulgaria" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Oslo (Norway)</b></td>
    <td align="center"><b>Paris (France)</b></td>
    <td align="center"><b>Rome (Italy)</b></td>
    <td align="center"><b>Sofia (Bulgaria)</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Stockholm_Sweden.png?raw=true" alt="Stockholm_Sweden" width="220"/></td>
    <td align="center"><img src="readme/Tirana_Albania.png?raw=true" alt="Tirana_Albania" width="220"/></td>
    <td align="center"><img src="readme/Vatican City_Vatican.png?raw=true" alt="Vatican City_Vatican" width="220"/></td>
    <td align="center"><img src="readme/Warsaw_Poland.png?raw=true" alt="Warsaw_Poland" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Stockholm (Sweden)</b></td>
    <td align="center"><b>Tirana (Albania)</b></td>
    <td align="center"><b>Vatican City (Vatican)</b></td>
    <td align="center"><b>Warsaw (Poland)</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Zurich_Switzerland.png?raw=true" alt="Zurich_Switzerland" width="220"/></td>
    <td align="center"></td>
    <td align="center"></td>
    <td align="center"></td>
  </tr>
  <tr>
    <td align="center"><b>Zurich (Switzerland)</b></td>
    <td align="center"></td>
    <td align="center"></td>
    <td align="center"></td>
  </tr>
</table>


#### North America

<table width="100%">
  <tr>
    <td align="center" width="25%"><img src="readme/Havana_Cuba.png?raw=true" alt="Havana_Cuba" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Mexico City_Mexico.png?raw=true" alt="Mexico City_Mexico" width="220"/></td>
    <td align="center" width="25%"><img src="readme/New York City_USA.png?raw=true" alt="New York City_USA" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Panama City_Panama.png?raw=true" alt="Panama City_Panama" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Havana (Cuba)</b></td>
    <td align="center"><b>Mexico City (Mexico)</b></td>
    <td align="center"><b>New York City (USA)</b></td>
    <td align="center"><b>Panama City (Panama)</b></td>
  </tr>
  <tr>
    <td align="center" width="25%"><img src="readme/Toronto_Canada.png?raw=true" alt="Toronto_Canada" width="220"/></td>
    <td align="center"></td>
    <td align="center"></td>
    <td align="center"></td>
  </tr>
  <tr>
    <td align="center"><b>Toronto (Canada)</b></td>
    <td align="center"></td>
    <td align="center"></td>
    <td align="center"></td>
  </tr>
</table>


#### Oceania

<table width="100%">
  <tr>
    <td align="center" width="25%"><img src="readme/Auckland_NewZealand.png?raw=true" alt="Auckland_NewZealand" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Funafuti_Tuvalu.png?raw=true" alt="Funafuti_Tuvalu" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Jakarta_Indonesia.png?raw=true" alt="Jakarta_Indonesia" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Suva_Fiji.png?raw=true" alt="Suva_Fiji" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Auckland (New Zealand)</b></td>
    <td align="center"><b>Funafuti (Tuvalu)</b></td>
    <td align="center"><b>Jakarta (Indonesia)</b></td>
    <td align="center"><b>Suva (Fiji)</b></td>
  </tr>
</table>

#### South America

<table width="100%">
  <tr>
    <td align="center" width="25%"><img src="readme/Asunción_Paraguay.png?raw=true" alt="Asunción_Paraguay" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Buenos Aires_Argentina.png?raw=true" alt="Buenos Aires_Argentina" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Lima_Peru.png?raw=true" alt="Lima_Peru" width="220"/></td>
    <td align="center" width="25%"><img src="readme/Montevideo_Uruguay.png?raw=true" alt="Montevideo_Uruguay" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><b>Asunción (Paraguay)</b></td>
    <td align="center"><b>Buenos Aires (Argentina)</b></td>
    <td align="center"><b>Lima (Peru)</b></td>
    <td align="center"><b>Montevideo (Uruguay)</b></td>
  </tr>
  <tr>
    <td align="center"><img src="readme/Quito_Ecuador.png?raw=true" alt="Quito_Ecuador" width="220"/></td>
    <td align="center"><img src="readme/Rio de Janeiro_Brazil.png?raw=true" alt="Rio de Janeiro_Brazil" width="220"/></td>
    <td align="center"><img src="readme/Santiago_Chile.png?raw=true" alt="Santiago_Chile" width="220"/></td>
    <td align="center"></td>
  </tr>
  <tr>
    <td align="center"><b>Quito (Ecuador)</b></td>
    <td align="center"><b>Rio de Janeiro (Brazil)</b></td>
    <td align="center"><b>Santiago (Chile)</b></td>
    <td align="center"></td>
  </tr>
</table>




## Contact
If you have any questions or suggestions, feel free to reach out to md_shadab_alam@outlook.com or pavlo.bazilinskyy@gmail.com.
