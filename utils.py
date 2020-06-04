def check_location(coordinates, rectangle):
    """Check if point lies inside rectangle"""
    if coordinates[0] > rectangle[0] and coordinates[0] < rectangle[2] \
        and coordinates[1] > rectangle[1] and coordinates[1] < rectangle[3]:
        return True
    else:
        return False
