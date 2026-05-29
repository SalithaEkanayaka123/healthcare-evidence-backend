# Service class responsible for generating summaries of healthcare evidence records.
class SummaryService:

    # Generates a plain-text summary from an evidence title and content.
    # Takes the first 35 words of the content as a brief extract,
    # appends '...' if the content is longer, and adds a standard healthcare disclaimer.
    # Returns the summary as a formatted string to be stored in the evidence record.
    def generate_summary(self, title: str, content: str) -> str:
        # Split content into individual words for truncation
        words = content.split()

        # Take the first 35 words as a simple summary preview
        short_content = " ".join(words[:35])

        return (
            f"Summary for '{title}' : {short_content}"
            # Append ellipsis if the content was truncated beyond 35 words
            f"{'...' if len(words) > 35 else ''}"
            # Standard disclaimer appended to every generated summary
            "This evidence may support heealthcare desicion-making, "
            "but it should be reviewed by a domian expert."
        )