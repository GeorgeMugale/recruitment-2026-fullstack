def find_province_by_constituency(
    data: dict[str, list[str]],
    constituency_name: str
) -> str | None:
    """
    Given scraped data and a constituency name,
    return the province it belongs to.

    Case-insensitive.

    Returns:
        province name if found, otherwise None
    """
    # lower case to make query case-insensitive
    search_term = constituency_name.lower()

    # loop through each dictionary item (Key=Province, Value=List of Constituencies)
    for province, constituencies in data.items():
        # loop through the list of constituencies for this specific province
        for constituency in constituencies:
            # case-insensitive compare
            if constituency.lower() == search_term:
                return province

    return None
