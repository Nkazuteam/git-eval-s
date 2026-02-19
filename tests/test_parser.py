from mdtoc.parser import Heading, parse_headings


class TestParseHeadings:
    def test_single_heading(self):
        assert parse_headings("# Hello") == [Heading(1, "Hello")]

    def test_multiple_levels(self):
        md = "# Title\n## Section\n### Sub"
        result = parse_headings(md)
        assert result == [
            Heading(1, "Title"),
            Heading(2, "Section"),
            Heading(3, "Sub"),
        ]

    def test_ignores_non_headings(self):
        md = "Normal text\n# Heading\nMore text"
        assert len(parse_headings(md)) == 1

    def test_empty_content(self):
        assert parse_headings("") == []

    def test_heading_with_special_chars(self):
        result = parse_headings("# Hello World! (2024)")
        assert result[0].text == "Hello World! (2024)"

    def test_requires_space_after_hashes(self):
        assert parse_headings("##no space") == []

    def test_max_level_six(self):
        result = parse_headings("###### Level 6")
        assert result == [Heading(6, "Level 6")]

    def test_seven_hashes_ignored(self):
        assert parse_headings("####### Not a heading") == []

    def test_skips_fenced_code_blocks(self):
        md = "# Real\n```\n# Fake\n```\n## Also Real"
        result = parse_headings(md)
        assert result == [Heading(1, "Real"), Heading(2, "Also Real")]

    def test_multiple_code_blocks(self):
        md = "```\n# A\n```\n# B\n```\n# C\n```"
        result = parse_headings(md)
        assert result == [Heading(1, "B")]
