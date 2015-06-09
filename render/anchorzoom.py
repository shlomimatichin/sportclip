def anchorZoom(clip, anchor, factor):
    assert anchor in ['C', 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    size = clip.size
    newSize = (size[0] / factor, size[1] / factor)
    x1 = (size[0] - newSize[0]) / 2
    y1 = (size[1] - newSize[1]) / 2
    if 'N' in anchor:
        y1 = 0
    if 'S' in anchor:
        y1 = size[1] - newSize[1]
    if 'E' in anchor:
        x1 = size[0] - newSize[0]
    if 'W' in anchor:
        x1 = 0
    cropped = clip.crop(x1=x1, y1=y1, width=newSize[0], height=newSize[1])
    return cropped.resize(size)
