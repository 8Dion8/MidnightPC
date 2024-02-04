import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re

from dbutils.db import Database

db = Database()
db.init_tables()

main_link = "https://en.wikipedia.org/wiki/List_of_Intel_Core_processors"

response = requests.get(main_link)
soup = BeautifulSoup(response.content, "html.parser")

print("Parsing...")

links = []

tables = soup.find_all("table")
for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        columns = row.find_all('td')
        for col in columns:
            try:
                model_link = col.find('a')['href']
                if "intel.com/content" in model_link:
                    links.append(model_link)
            except:
                pass

print(f"Found {len(links)} specification links")

to_db = []

for link in tqdm(links):

    name_display = name_brand = name_series = name_generation = name_sku = name_prefix = name_suffix = name_codename = architecture = msrp = launch_date = socket = n_cores_total = intel_n_cores_perf = intel_n_cores_eff = n_threads = max_turbo_freq = base_freq = intel_thermal_velocity_boost_freq = intel_turbo_boost_max30_freq = intel_perf_max_turbo_freq = intel_eff_max_turbo_freq = intel_perf_base_freq = intel_eff_base_freq = intel_smart_cache_total = cache_l1 = cache_l2 = cache_l3 = tdp_base = tdp_max = tjunc_temp = overclocking = memory_max = memory_types = memory_channels = memory_bandwith = ecc_support = igpu_name_display = igpu_base_freq = igpu_max_freq = igpu_capabilities = igpu_cores = igpu_max_resolution_hdmi = igpu_max_resolution_dp = igpu_max_resolution_edp = igpu_directx = igpu_opengl = igpu_opencl = igpu_n_codec_engines = igpu_max_displays = dmi_version = dmi_lanes = pcie_version = pcie_config = pcie_max = ""

    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")
    sections = soup.find_all("ul", class_="specs-list")
    for section in sections:
        rows = section.find_all("li")
        for row in rows:
            name = row.find("span", class_="label").text.strip()
            value = row.find("span", class_="value").text.strip()
            match name:
                case "Product Collection":
                    if re.match(r"\d+\w+ Generation Intel® Core™ i\d Processors", value):
                        name_generation = re.search(r"\d+", value).group()
                        name_brand = "Intel Core"
                        name_series = re.search(r"i\d", value).group()
                    elif value == "Legacy Intel® Core™ Processors":
                        name_brand = "Intel Core"
                    else:
                        print(value, link)
                case "Processor Number":
                    if re.match(r"([a-zA-Z]*)(\d+)([a-zA-Z]*)", value):
                        name_prefix, num, name_postfix = re.search(r"([a-zA-Z]*)(\d+)([a-zA-Z]*)", value).groups()
                        name_generation = num[0]
                        name_sku = num[1:]
                    else:
                        print(value, link)
                case "Lithography":
                    architecture = value

    to_db.append((name_display, name_brand, name_series, name_generation, name_sku, name_suffix, name_codename, architecture, msrp, launch_date, socket, n_cores_total, intel_n_cores_perf, intel_n_cores_eff, n_threads, max_turbo_freq, base_freq, intel_thermal_velocity_boost_freq, intel_turbo_boost_max30_freq, intel_perf_max_turbo_freq, intel_eff_max_turbo_freq, intel_perf_base_freq, intel_eff_base_freq, intel_smart_cache_total, cache_l1, cache_l2, cache_l3, tdp_base, tdp_max, tjunc_temp, overclocking, memory_max, memory_types, memory_channels, memory_bandwith, ecc_support, igpu_name_display, igpu_base_freq, igpu_max_freq, igpu_capabilities, igpu_cores, igpu_max_resolution_hdmi, igpu_max_resolution_dp, igpu_max_resolution_edp, igpu_directx, igpu_opengl, igpu_opencl, igpu_n_codec_engines, igpu_max_displays, dmi_version, dmi_lanes, pcie_version, pcie_config, pcie_max))    

                    
db.add_rows("cpu", to_db)

