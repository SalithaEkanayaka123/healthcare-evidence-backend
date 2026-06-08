class SummaryService:
    """
    Service responsible for generating simple extractive summaries
    for healthcare evidence records.
    """

    SUMMARY_WORD_LIMIT = 35

    def generate_summary(self, title: str, content: str) -> str:
        words = content.split()
        short_content = " ".join(words[: self.SUMMARY_WORD_LIMIT])
        ellipsis = "..." if len(words) > self.SUMMARY_WORD_LIMIT else ""

        return (
            f"Summary for '{title}': {short_content}{ellipsis} "
            "This evidence may support healthcare decision-making, "
            "but it should be reviewed by a domain expert."
        )