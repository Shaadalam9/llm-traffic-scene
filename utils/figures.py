# by Shadab Alam <md_shadab_alam@outlook.com>
import common
from custom_logger import CustomLogger
from logmod import logs
import warnings
import os
import pandas as pd
import shutil
import plotly as py
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import defaultdict
from utils.information import Video_info

# Suppress the specific FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning, module="plotly")

logger = CustomLogger(__name__)  # use custom logger


# Colours in graphs
bar_colours = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA",
               "#FFA15A", "#19D3F3", "#FF6692"]

keys_of_interest = ["Persons", "Cars", "Bicycles", "Motorbikes",
                    "Buses", "Trucks", "Traffic lights"]

key_to_colour = {k: bar_colours[i] for i, k in enumerate(keys_of_interest)}

# Consts
BASE_HEIGHT_PER_ROW = 30  # Adjust as needed
FLAG_SIZE = 12
TEXT_SIZE = 12
SCALE = 1  # scale=3 hangs often


class Plots():
    def __init__(self) -> None:
        self.info = Video_info()  # For gathering video information/statistics

    def add_vertical_legend_annotations(self, fig, legend_items, x_position, y_start, spacing=0.03, font_size=50):
        for i, item in enumerate(legend_items):
            fig.add_annotation(
                x=x_position,  # Use the x_position provided by the user
                y=y_start - i * spacing,  # Adjust vertical position based on index and spacing
                xref='paper', yref='paper', showarrow=False,
                text=f'<span style="color:{item["color"]};">&#9632;</span> {item["name"]}',  # noqa:E501
                font=dict(size=font_size),
                xanchor='left', align='left'  # Ensure the text is left-aligned
            )

    def save_plotly_figure(self, fig, filename, width=1600, height=900, scale=SCALE, save_final=True, save_png=True,
                           save_pdf=True):
        """
        Saves a Plotly figure as HTML, PNG, SVG, and EPS formats.

        Args:
            fig (plotly.graph_objs.Figure): Plotly figure object.
            filename (str): Name of the file (without extension) to save.
            width (int, optional): Width of the PNG and EPS images in pixels. Defaults to 1600.
            height (int, optional): Height of the PNG and EPS images in pixels. Defaults to 900.
            scale (int, optional): Scaling factor for the PNG image. Defaults to 3.
            save_final (bool, optional): whether to save the "good" final figure.
            save_png (bool, optional): whether to save a PNG image.
            save_pdf (bool, optional): whether to save a PDF image.
        """
        # Create directory if it doesn't exist
        output_folder = "_output"
        output_final = "figures"
        os.makedirs(output_folder, exist_ok=True)
        os.makedirs(output_final, exist_ok=True)

        # Save as HTML
        logger.info(f"Saving html file for {filename}.")
        py.offline.plot(fig, filename=os.path.join(output_folder, filename + ".html"))
        # also save the final figure
        if save_final:
            py.offline.plot(fig, filename=os.path.join(output_final, filename + ".html"),  auto_open=False)

        # Save static formats independently so one failure does not prevent the
        # other output, and include the underlying error in the log.
        if save_png:
            try:
                logger.info(f"Saving png file for {filename}.")
                fig.write_image(os.path.join(output_folder, filename + ".png"), width=width, height=height,
                                scale=scale)
                # also save the final figure
                if save_final:
                    shutil.copy(os.path.join(output_folder, filename + ".png"),
                                os.path.join(output_final, filename + ".png"))
            except Exception as error:
                logger.error(f"Could not save PNG image {filename}: {error}.")

        if save_pdf:
            try:
                logger.info(f"Saving pdf file for {filename}.")
                fig.write_image(os.path.join(output_folder, filename + ".pdf"), width=width, height=height)
                # also save the final figure
                if save_final:
                    shutil.copy(os.path.join(output_folder, filename + ".pdf"),
                                os.path.join(output_final, filename + ".pdf"))
            except Exception as error:
                logger.error(f"Could not save PDF image {filename}: {error}.")

    def stack_plot(self, final_dict, df_mapping, order_by, title_text, filename, font_size_captions=40,
                   x_axis_title_height=110, legend_x=0.92, legend_y=0.015, legend_spacing=0.02, left_margin=10,
                   right_margin=10):
        """
        Plots a stacked bar graph based on the provided data and configuration.

        Parameters:
            df_mapping (dict): A dictionary mapping categories to their respective DataFrames.
            order_by (str): Criterion to order the bars, e.g., 'alphabetical' or 'average'.
            title_text (str): The title of the plot.
            filename (str): The name of the file to save the plot as.
            font_size_captions (int, optional): Font size for captions. Default is 40.
            x_axis_title_height (int, optional): Vertical space for x-axis title. Default is 110.
            legend_x (float, optional): X position of the legend. Default is 0.92.
            legend_y (float, optional): Y position of the legend. Default is 0.015.
            legend_spacing (float, optional): Spacing between legend entries. Default is 0.02.

        Returns:
            None
        """

        # Define log messages in a structured way
        log_messages = {
            ("alphabetical"): "Plotting speed to cross by alphabetical order during day time.",
            ("average"): "Plotting speed to cross by average during day time.",
        }

        message = log_messages.get((order_by))

        if message:
            logger.info(message)

        if order_by == "alphabetical":
            cities_ordered = sorted(
                [
                    city for city in final_dict.keys()
                    if any(final_dict[city].get(k, 0) > 0 for k in keys_of_interest)
                ],
                key=lambda city: city
            )

        elif order_by == "average":
            cities_ordered = sorted(
                [
                    city for city in final_dict.keys()
                    if any(final_dict[city].get(k, 0) > 0 for k in keys_of_interest)
                ],
                key=lambda city: (
                    sum(final_dict[city].get(k, 0) for k in keys_of_interest) / len(keys_of_interest)
                ),
                reverse=True
            )

        elif order_by == "continent_average":
            # Group cities by continent
            continent_cities = defaultdict(list)
            for city in final_dict:
                if any(final_dict[city].get(k, 0) > 0 for k in keys_of_interest):
                    continent = final_dict[city].get('continent') or 'Unknown'
                    continent_cities[continent].append(city)

            # Sort cities within each continent by average
            for continent in continent_cities:
                continent_cities[continent].sort(
                    key=lambda city: (
                        sum(final_dict[city].get(k, 0) for k in keys_of_interest) / len(keys_of_interest)
                    ),
                    reverse=True
                )

            # Flatten the result, sorting continents alphabetically
            cities_ordered = []
            for continent in sorted(continent_cities):
                cities_ordered.extend(continent_cities[continent])

        # Determine how many cities will be in each column
        num_cities_per_col = len(cities_ordered) // 2 + len(cities_ordered) % 2  # Split cities into two groups

        # Define a base height per row and calculate total figure height
        TALL_FIG_HEIGHT = num_cities_per_col * BASE_HEIGHT_PER_ROW

        fig = make_subplots(
            rows=num_cities_per_col, cols=2,  # Two columns
            vertical_spacing=0.0005,  # Reduce the vertical spacing
            horizontal_spacing=0.01,  # Reduce horizontal spacing between columns
            row_heights=[1.0] * (num_cities_per_col),
        )

        # Plot left column (first half of cities)
        for i, city in enumerate(cities_ordered[:num_cities_per_col]):

            iso_code = self.info.get_value(df_mapping, "City", city, None, None, "ISO")

            # build up textual label for left column
            city_label = self.info.iso2_to_flag(self.info.iso3_to_iso2(
                iso_code)) + " " + city + " " + "(" + iso_code + ")"  # type: ignore

            # Row for day and night
            row = i + 1

            # Sum of all keys of interest for this city
            total_value = sum(final_dict[city].get(k, 0) for k in keys_of_interest)
            y_label = f'{city_label} {int(total_value)}'

            # Add a bar for each key, stacking them
            cumulative = 0
            for key in keys_of_interest:
                value = final_dict[city].get(key, 0)
                if value > 0:
                    fig.add_trace(go.Bar(
                        x=[value], y=[y_label], orientation='h',
                        name=f"{key.title()}",
                        marker=dict(color=key_to_colour[key]),
                        text=[f"{int(value)}"],
                        textposition='inside',
                        showlegend=(i == 0),
                        textfont=dict(size=14, color='white'),
                    ), row=row, col=1)
                    cumulative += value

            # Add city label at the end of the bar
            fig.add_annotation(
                x=cumulative + 0.5,
                y=y_label,
                text=y_label,
                showarrow=False,
                font=dict(size=14, color="black"),
                xanchor="left",
                yanchor="middle",
                row=row,
                col=1
            )

        for i, city in enumerate(cities_ordered[num_cities_per_col:]):
            # parts = city_country.split("_")
            # city = "_".join(parts[:-1])

            iso_code = self.info.get_value(df_mapping, "City", city, None, None, "ISO")

            # build up textual label for left column
            city_label = self.info.iso2_to_flag(self.info.iso3_to_iso2(
                iso_code)) + " " + city + " " + "(" + iso_code + ")"  # type: ignore
            row = i + 1

            # Sum of all keys of interest for this city
            total_value = sum(final_dict[city].get(k, 0) for k in keys_of_interest)
            y_label = f'{city_label} {int(total_value)}'

            # Add a bar for each key, stacking them
            cumulative = 0
            for key in keys_of_interest:
                value = final_dict[city].get(key, 0)
                if value > 0:
                    fig.add_trace(go.Bar(
                        x=[value], y=[y_label], orientation='h',
                        name=f"{key.title()}",
                        marker=dict(color=key_to_colour[key]),
                        text=[f"{int(value)}"],
                        textposition='inside',
                        showlegend=(i == 0),
                        textfont=dict(size=14, color='white'),
                    ), row=row, col=2)
                    cumulative += value

            # Add city label at the end of the bar
            fig.add_annotation(
                x=cumulative + 0.5,
                y=y_label,
                text=y_label,
                showarrow=False,
                font=dict(size=14, color="black"),
                xanchor="left",
                yanchor="middle",
                row=row,
                col=2
            )

        max_value = max(
            sum(final_dict[city].get(k, 0) for k in keys_of_interest)
            for city in cities_ordered
        ) if cities_ordered else 0
        max_value += 18

        # Identify the last row for each column where the last city is plotted
        last_row_left_column = num_cities_per_col * 2  # The last row in the left column
        last_row_right_column = (len(cities_ordered) - num_cities_per_col) * 2  # The last row in the right column
        first_row_left_column = 1  # The first row in the left column
        first_row_right_column = 1  # The first row in the right column

        # Update the loop for updating x-axes based on max values for speed and time
        for i in range(1, num_cities_per_col * 2 + 1):  # Loop through all rows in both columns
            # Update x-axis for the left column
            if i % 2 == 1:  # Odd rows
                fig.update_xaxes(
                    range=[0, max_value],
                    row=i,
                    col=1,
                    showticklabels=(i == first_row_left_column),
                    side='top', showgrid=False
                )
            else:  # Even rows (representing time)
                fig.update_xaxes(
                    range=[0, max_value],
                    row=i,
                    col=1,
                    showticklabels=(i == last_row_left_column),
                    side='bottom', showgrid=False
                )

            # Update x-axis for the right column
            if i % 2 == 1:  # Odd rows
                fig.update_xaxes(
                    range=[0, max_value],
                    row=i,
                    col=2,  # Use speed max value for top axis
                    showticklabels=(i == first_row_right_column),
                    side='top', showgrid=False
                )
            else:  # Even rows (representing time)
                fig.update_xaxes(
                    range=[0, max_value],
                    row=i,
                    col=2,  # Use time max value for bottom axis
                    showticklabels=(i == last_row_right_column),
                    side='bottom', showgrid=False
                )

        # Set the x-axis labels (title_text) only for the last row and the first row
        fig.update_xaxes(
            title=dict(text=title_text,
                       font=dict(size=font_size_captions)),
            tickfont=dict(size=font_size_captions),
            ticks='outside',
            ticklen=10,
            tickwidth=2,
            tickcolor='black',
            row=1,
            col=1
        )

        fig.update_xaxes(
            title=dict(text=title_text,
                       font=dict(size=font_size_captions)),
            tickfont=dict(size=font_size_captions),
            ticks='outside',
            ticklen=10,
            tickwidth=2,
            tickcolor='black',
            row=1,
            col=2
        )

        # Update both y-axes (for left and right columns) to hide the tick labels
        fig.update_yaxes(showticklabels=False)

        # Ensure no gridlines are shown on x-axes and y-axes
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)

        # Update layout to hide the main legend and adjust margins
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            barmode='stack',
            height=TALL_FIG_HEIGHT,
            width=2480,
            showlegend=False,  # Hide the default legend
            margin=dict(t=150, b=150),
            bargap=0,
            bargroupgap=0
        )

        # Define gridline generation parameters
        # start, step, count = 10, 10, 100

        # Generate gridline positions
        # x_grid_values = [start + i * step for i in range(count)]

        # for x in x_grid_values:
        #     fig.add_shape(
        #         type="line",
        #         x0=x,
        #         y0=0,
        #         x1=x,
        #         y1=1,  # Set the position of the gridlines
        #         xref='x',
        #         yref='paper',  # Ensure gridlines span the whole chart (yref='paper' spans full height)
        #         line=dict(color="darkgray", width=1),  # Customize the appearance of the gridlines
        #         layer="above"  # Draw the gridlines above the bars
        #     )

        # # Manually add gridlines using `shapes` for the right column (x-axis 'x2')
        # for x in x_grid_values:
        #     fig.add_shape(
        #         type="line",
        #         x0=x,
        #         y0=0,
        #         x1=x,
        #         y1=1,  # Set the position of the gridlines
        #         xref='x2',
        #         yref='paper',  # Apply to right column (x-axis 'x2')
        #         line=dict(color="darkgray", width=1),  # Customize the appearance of the gridlines
        #         layer="above"  # Draw the gridlines above the bars
        #     )

        legend_items = [
            {"name": key.capitalize(), "color": bar_colours[i]}
            for i, key in enumerate(keys_of_interest)
        ]

        # Add the vertical legends at the top and bottom
        self.add_vertical_legend_annotations(fig,
                                             legend_items,
                                             x_position=legend_x,
                                             y_start=legend_y,
                                             spacing=legend_spacing,
                                             font_size=font_size_captions)

        # Add a box around the first column (left side)
        fig.add_shape(
            type="rect",
            xref="paper",
            yref="paper",
            x0=0,
            y0=1,
            x1=0.495,
            y1=0.0,
            line=dict(color="black", width=2)  # Black border for the box
        )

        # Add a box around the second column (right side)
        fig.add_shape(
            type="rect",
            xref="paper",
            yref="paper",
            x0=0.505,
            y0=1,
            x1=1,
            y1=0.0,
            line=dict(color="black", width=2)  # Black border for the box
        )

        fig.update_yaxes(
            tickfont=dict(size=TEXT_SIZE, color="black"),
            showticklabels=False,  # Ensure city names are visible
            ticklabelposition='inside',  # Move the tick labels inside the bars
        )
        fig.update_xaxes(
            tickangle=0,  # No rotation or small rotation for the x-axis
        )

        # update font family
        fig.update_layout(font=dict(family=common.get_configs('font_family')))

        # Final adjustments and display
        fig.update_layout(margin=dict(l=left_margin, r=right_margin, t=x_axis_title_height, b=10))
        self.save_plotly_figure(fig=fig,
                                filename=filename,
                                width=1800,
                                height=TALL_FIG_HEIGHT,
                                scale=SCALE,
                                save_pdf=True,
                                save_final=True)

    def plot_choropleth(self, data_dict, value_key=None, title_text=None, filename=None):
        """
        Reads a CSV file with country sound data and plots a choropleth map.

        Parameters:
            csv_path (str): Path to the CSV file containing 'Country', 'iso', and 'sound' columns.
        """
        try:
            # Convert dict to DataFrame
            df = pd.DataFrame.from_dict(data_dict, orient='index').reset_index()
            df = df.rename(columns={'index': 'City', 'country': 'Country', 'iso': 'ISO'})

            # Only keep rows with valid ISO and value
            df_clean = df[['City', 'Country', 'ISO', value_key]].dropna(subset=['ISO', value_key])

            fig = px.choropleth(
                df_clean,
                locations="ISO",
                color=value_key,
                hover_name="Country",
                color_continuous_scale="Inferno_r",
                projection="natural earth",
                title=title_text
            )

            fig.update_layout(
                geo=dict(showframe=False, showcoastlines=True),
                margin={"r": 0, "t": 50, "l": 0, "b": 0},
                coloraxis_colorbar=dict(title=value_key)
            )

            self.save_plotly_figure(fig=fig,
                                    filename=filename,
                                    scale=SCALE,
                                    save_pdf=True,
                                    save_final=True)

        except Exception as e:
            logger.error(f"Error generating choropleth map: {e}")

    def plot_city_stacked_bars(self, df, title_text, filename, font_size_captions, legend_x,
                               legend_y, left_margin, right_margin, stack_cols=None):
        """
        Plots a grouped stacked bar chart, with cities sorted by the sum of stack_cols (increasing).
        """

        if stack_cols is None:
            stack_cols = keys_of_interest

        if "Bicycles" not in df.columns and "Cycles" in df.columns:
            df = df.copy()
            df["Bicycles"] = df["Cycles"]

        # Extract city group (name without number)
        df['CityGroup'] = df['City'].str.replace(r'\d+$', '', regex=True).str.strip()

        # Compute row-wise sum for sorting within each city
        df['row_sum'] = df[stack_cols].sum(axis=1)

        # Prepare for plotting
        # Group by city and sort within group
        # sorted_dfs = []
        # city_groups = df['CityGroup'].unique()
        # for city in city_groups:
        #     city_df = df[df['CityGroup'] == city].sort_values('row_sum')
        #     sorted_dfs.append(city_df)
        # df_sorted = pd.concat(sorted_dfs, ignore_index=True)

        # Extract number at the end of the city name
        df['CityNum'] = df['City'].str.extract(r'(\d+)$').astype(float)

        # Sort by city group, then by the number (ascending)
        df_sorted = df.sort_values(['CityGroup', 'CityNum']).reset_index(drop=True)

        city_groups = df_sorted['CityGroup'].unique()

        # Compute x positions and city label ticks
        x = []
        tickvals = []
        ticktext = []
        idx = 0
        gap = 1  # gap between clusters
        for city in city_groups:
            n = (df['CityGroup'] == city).sum()
            for _ in range(n):
                x.append(idx)
                idx += 1

            # Center label under the cluster
            cluster_center = idx - n/2 - 0.5
            tickvals.append(cluster_center)
            ticktext.append(city)
            idx += gap

        fig = go.Figure()
        stack_cols_sorted = keys_of_interest
        for col in stack_cols_sorted:
            fig.add_trace(go.Bar(
                x=x,
                y=df_sorted[col],
                name=col,
                width=0.9,
                marker_color=key_to_colour[col],
                text=df_sorted[col],
                textposition='inside',
                textfont=dict(color='white'),
                insidetextanchor='middle',
            ))

        # Add the sum labels using the exact same x
        fig.add_trace(go.Scatter(
            x=x,
            y=df_sorted['row_sum'],
            mode='text',
            text=df_sorted['row_sum'].astype(int),
            textposition='top center',
            textfont=dict(size=font_size_captions, color='black'),
            showlegend=False,
            hoverinfo='skip'
        ))

        y_max = df_sorted['row_sum'].max()

        fig.update_layout(
            barmode='stack',
            title=title_text,
            xaxis=dict(
                title='',
                title_font=dict(size=font_size_captions),    # Size of the x-axis label
                tickfont=dict(size=font_size_captions),      # Size of the x-axis ticks
                tickmode='array',
                tickvals=tickvals,
                ticktext=ticktext,
                showgrid=False,
                zeroline=False
            ),
            yaxis=dict(
                title='Count',
                title_font=dict(size=font_size_captions),    # Size of the y-axis label
                tickfont=dict(size=font_size_captions),      # Size of the y-axis ticks
                range=[0, y_max * 1.08],
                ),
            legend=dict(
                x=legend_x,   # X position (fraction of plot width)
                y=legend_y,   # Y position (fraction of plot height)
                xanchor='left',  # How to anchor the x position ('left', 'center', 'right')
                yanchor='top',   # How to anchor the y position ('top', 'middle', 'bottom')
                font=dict(size=18),
                title='',  # Optional, for clarity
            ),
            template=common.get_configs("plotly_template"),
            bargap=0.2
        )
        self.save_plotly_figure(fig=fig,
                                filename=filename,
                                scale=SCALE,
                                save_pdf=True,
                                save_final=True)
