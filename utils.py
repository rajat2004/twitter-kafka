def check_location(coordinates, rectangle):
    """Check if point lies inside rectangle"""
    return (coordinates[0] > rectangle[0] and coordinates[0] < rectangle[2] \
            and coordinates[1] > rectangle[1] and coordinates[1] < rectangle[3])
