import rpy2.robjects as robjects

def get_shortest_path(
    start_id,
    end_id,
    gpkg,
    filename
):

    r = robjects.r

    r('library(hfsubsetR)')
    get_shortest_path_fn = r['get_shortest_path']
    get_shortest_path_fn(
        start_id=start_id, 
        end_id=end_id,
        gpkg=gpkg,
        filename=filename,
    )

