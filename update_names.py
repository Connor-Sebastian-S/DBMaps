import json

input_file = "buildings_master.geojson"
output_file = "buildings_updated.geojson"

with open(input_file, "r", encoding="utf-8") as f:
    geojson = json.load(f)

count = 0

for feature in geojson["features"]:
    properties = feature["properties"]

    if properties.get("btype") == "greenhouse":
        properties["name"] = "Greenhouse"
        count += 1

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(geojson, f, indent=2, ensure_ascii=False)

print(f"Updated {count} features.")