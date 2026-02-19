from mdtoc.cli import main


class TestMain:
    def test_basic_file(self, tmp_path):
        md = tmp_path / "test.md"
        md.write_text("# Title\n## Section\n", encoding="utf-8")
        assert main([str(md)]) == 0

    def test_missing_file(self):
        assert main(["nonexistent.md"]) == 1

    def test_no_headings(self, tmp_path):
        md = tmp_path / "empty.md"
        md.write_text("No headings here\n", encoding="utf-8")
        assert main([str(md)]) == 0

    def test_max_depth_option(self, tmp_path):
        md = tmp_path / "test.md"
        md.write_text("# A\n## B\n### C\n", encoding="utf-8")
        assert main([str(md), "--max-depth", "1"]) == 0

    def test_output_content(self, tmp_path, capsys):
        md = tmp_path / "test.md"
        md.write_text("# Hello\n## World\n", encoding="utf-8")
        main([str(md)])
        out = capsys.readouterr().out
        assert "Hello" in out
        assert "World" in out
