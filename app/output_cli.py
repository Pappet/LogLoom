def display_counts(key, data):
    counts_strings = [f"{sub_key}: {count}" for sub_key, count in data.items()]
    return f"{key.capitalize()} Counts:\n" + "\n".join(counts_strings)


def display_range(key, data):
    start, end = data
    return f"{key.capitalize()} Range:\nFrom: {start}\nTo:   {end}"


def display_time_difference(data):
    return f"Time Difference: {data} minutes"


def display_log_length(data):
    return f"Log Length: {data} lines"


def display_parsed_length(data):
    return f"Parsed Length: {data} lines"


def display_insights(insights, log_data_length, parsed_data_length):
    """Display the insights in a formatted manner."""

    separator = "=" * 50
    insights_header = "Log File Insights".center(50)
    insights_footer = "\nEnjoy diving deeper into your logs with LogLoom!"

    display_functions = {
        "counts": display_counts,
        "range": display_range,
        "time_difference": display_time_difference,
        "log_length": display_log_length,
        "parsed_length": display_parsed_length
    }

    # Integrating the log length into the insights dictionary for uniformity
    insights["log"] = {"log_length": log_data_length}
    insights["parsed"] = {"parsed_length": parsed_data_length}

    insight_messages = []
    for key, data in insights.items():
        for sub_key, sub_data in data.items():
            func = display_functions.get(sub_key)
            if func:
                if sub_key in ["time_difference", "log_length", "parsed_length"]:
                    insight_messages.append(func(sub_data))
                else:
                    insight_messages.append(func(key, sub_data))

    # Construct the final message
    message_parts = [
        separator,
        insights_header,
        separator,
        "\n".join(insight_messages),
        insights_footer,
        separator
    ]

    print("\n".join(message_parts))
