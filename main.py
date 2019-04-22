import arcpy

# settings
project_base_path = r"C:\Projects\Applications\GIS\Maps\data\MyProject\MyProject"
export_path = r"C:\Projects\Applications\GIS\Maps\data\png\\"
symbol_layer_template_name = "sym_blk"
circle_size = "75 miles"
csv_url = r"C:\Projects\Applications\GIS\Maps\data\csv\all_data.csv"

# Constants
geocodeUrl = 'https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/ArcGIS World Geocoding Service'
aprx_path = project_base_path + ".aprx"
gdb_path = project_base_path + ".gdb"
city_data_layer_name = "cityData"
city_buffer_layer_name = "cityBuffer"

date_ranges = [
    "November_1_5",
    "November_6_10",
    "November_11_15",
    "November_16_20",
    "November_21_25",
    "November_26_30",
    "December_1_5",
    "December_6_10",
    "December_11_15",
    "December_16_20",
    "December_21_25",
    "December_26_30",
    "December_31_January_4",
    "January_5_9",
    "January_10_14",
    "January_15_19",
    "January_20_24",
    "January_25_29",
    "January_30_February_3",
    "February_4_8",
    "February_9_13",
    "February_14_18",
    "February_19_23",
    "February_24_28_29",
    "March_1_5",
    "March_6_10",
    "March_11_15",
    "March_16_20",
    "March_21_25",
    "March_26_31"]

date_ranges_text = [
    "November 1-5",
    "November 6-10",
    "November 11-15",
    "November 16-20",
    "November 21-25",
    "November 26-30",
    "December 1-5",
    "December 6-10",
    "December 11-15",
    "December 16-20",
    "December 21-25",
    "December 26-30",
    "December 31-January 4",
    "January 5-9",
    "January 10-14",
    "January 15-19",
    "January 20-24",
    "January 25-29",
    "January 30-February 3",
    "February 4-8",
    "February 9-13",
    "February 14-18",
    "February 19-23",
    "February 24-28/29",
    "March 1-5",
    "March 6-10",
    "March 11-15",
    "March 16-20",
    "March 21-25",
    "March 26-31"]

data_ranges = [
    "TMax10",
    "TMin10",
    "TMax90",
    "TMin90"]

data_ranges_text = [
    "TMax 10%",
    "TMin 10%",
    "TMax 90%",
    "TMin 90%"]


def project_path(path):
    if path == "current":
        return path
    return gdb_path + "\\" + path


gis_project = arcpy.mp.ArcGISProject(aprx_path)
gis_map = gis_project.listMaps()[0]
gis_layout = gis_project.listLayouts()[0]

table = gis_map.addDataFromPath(csv_url)
arcpy.GeocodeAddresses_geocoding(table, geocodeUrl, "SingleLine City VISIBLE NONE", project_path(city_data_layer_name), 'STATIC', 'US', 'ADDRESS_LOCATION', 'City')
arcpy.Buffer_analysis(project_path(city_data_layer_name), project_path(city_buffer_layer_name), circle_size, 'FULL', 'ROUND', 'NONE')
city_buffer_layer = gis_map.addDataFromPath(project_path(city_buffer_layer_name))
symbol_template_layer = gis_map.listLayers(symbol_layer_template_name)[0]

for data_index in range(len(data_ranges)):
    for date_index in range(len(date_ranges)):
        data_field = "USER_" + data_ranges[data_index] + "_" + date_ranges[date_index]
        arcpy.ApplySymbologyFromLayer_management(city_buffer_layer, symbol_template_layer, [["VALUE_FIELD", "USER_Field2", data_field]], 'MAINTAIN')

        t_text = gis_layout.listElements("TEXT_ELEMENT", "title_text")[0]
        t_text.text = data_ranges_text[data_index] + " " + date_ranges_text[date_index]

        gis_layout.exportToPNG(export_path + data_ranges[data_index] + "_" + date_ranges[date_index] + ".png")

