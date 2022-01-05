def pages_divider(page, page_range, perpage=5):
    page = int(page)
    if len(page_range) < perpage:
        return page_range
    if perpage / 2 - int(perpage / 2) == 0.5:
        start = page - int(perpage / 2)
        end = page + int(perpage / 2)
        if start < 1:
            start = 1
            end = perpage
        if end > page_range[-1]:
            end = page_range[-1]
            start = end - perpage
        return range(start, end + 1)
    else:
        start = page - int(perpage / 2) + 1
        end = page + int(perpage / 2)
        if start < 1:
            start = 1
            end = perpage
        if end > page_range[-1]:
            end = page_range[-1]
            start = end - perpage + 1
        return range(start, end + 1)