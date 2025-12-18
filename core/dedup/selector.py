def choose_candidates(groups, keep="first"):
    """
    Decide which images should be removed.

    keep:
        - "first": keep first image
        - "last": keep last image

    Returns:
        ["b.jpg", "c.jpg", ...]
    """
    remove = []

    for g in groups:
        if len(g) <= 1:
            continue
        if keep == "first":
            remove.extend(g[1:])
        else:
            remove.extend(g[:-1])

    return remove