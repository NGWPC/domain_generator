import argparse
from pathlib import Path

from domain_generator import get_shortest_path

def parse_args():
    parser = argparse.ArgumentParser(description='Find the shortest path between two NHD COMIDs')
    parser.add_argument(
        '--start-id', 
        type=int,
        help='Starting NHD COMID',
        required=True
    )
    parser.add_argument(
        '--end-id', 
        type=int,
        help='Ending NHD COMID',
        required=True
    )
    parser.add_argument(
        '--gpkg', 
        type=str, 
        default=str(Path.cwd() / "data/conus_nextgen.gpkg"),
        help='Path to the GeoPackage file'
    )
    parser.add_argument(
        '--filename', 
        type=str,
        help='Output filename'
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    get_shortest_path(
        start_id=args.start_id,
        end_id=args.end_id,
        gpkg=args.gpkg,
        filename=args.filename
    )
