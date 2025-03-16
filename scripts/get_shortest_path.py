from pathlib import Path

from domain_generator import get_shortest_path

if __name__ == "__main__":
    get_shortest_path(
        start_id = 4699143,
        end_id = 4700053,
        gpkg = str(Path.cwd() / "data/conus_nextgen.gpkg"),
        filename = "test"
    )
