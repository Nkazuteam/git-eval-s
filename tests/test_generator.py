from mdtoc.generator import generate_toc, slugify
from mdtoc.parser import Heading


class TestSlugify:
    def test_basic(self):
        assert slugify("Hello World") == "hello-world"

    def test_strips_punctuation(self):
        assert slugify("Hello, World!") == "hello-world"

    def test_preserves_hyphens(self):
        assert slugify("well-known") == "well-known"

    def test_collapses_whitespace(self):
        assert slugify("a   b") == "a-b"


class TestGenerateToc:
    def test_single_heading(self):
        headings = [Heading(1, "Title")]
        assert generate_toc(headings) == "- [Title](#title)"

    def test_nested_headings(self):
        headings = [Heading(1, "Title"), Heading(2, "Section")]
        lines = generate_toc(headings).splitlines()
        assert lines[0] == "- [Title](#title)"
        assert lines[1] == "  - [Section](#section)"

    def test_empty_list(self):
        assert generate_toc([]) == ""

    def test_max_depth_limits_output(self):
        headings = [
            Heading(1, "A"),
            Heading(2, "B"),
            Heading(3, "C"),
            Heading(4, "D"),
        ]
        toc = generate_toc(headings, max_depth=2)
        assert "A" in toc
        assert "B" in toc
        assert "C" not in toc
        assert "D" not in toc

    def test_starts_from_h2(self):
        headings = [Heading(2, "First"), Heading(3, "Second")]
        lines = generate_toc(headings).splitlines()
        assert lines[0] == "- [First](#first)"
        assert lines[1] == "  - [Second](#second)"

    def test_explicit_min_level(self):
        headings = [Heading(2, "A"), Heading(3, "B")]
        toc = generate_toc(headings, min_level=1)
        assert toc.startswith("  - [A]")
