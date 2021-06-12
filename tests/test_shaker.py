import pytest
from treeshake import Shaker


def test_add_stylesheet_exists():
    shaker = Shaker()
    file = './tests/_data/css/stylesheet.css'
    shaker.add_stylesheet(file)
    added_sheets = shaker.get_private_attributes().get('stylesheets', set())
    assert len(added_sheets) == 1
    assert next(iter(added_sheets)) == file


def test_add_stylesheet_not_exists():
    shaker = Shaker()
    with pytest.raises(FileNotFoundError):
        shaker.add_stylesheet('./tests/_data/css/missing.css')
        assert len(shaker.get_private_attributes().get('stylesheets', [])) == 0


def test_add_stylesheet_not_stylesheet():
    shaker = Shaker()
    with pytest.raises(ValueError):
        shaker.add_stylesheet('./tests/_data/css/no_css.html')
        assert len(shaker.get_private_attributes().get('stylesheets', [])) == 0


def test_add_html_file_exists():
    shaker = Shaker()
    file = './tests/_data/html/index.html'
    shaker.add_html_file(file)
    added_files = shaker.get_private_attributes().get('html_files', [])
    assert len(added_files) == 1
    assert next(iter(added_files)) == file
    shaker.add_html_file('./tests/_data/html/job.html')
    assert len(added_files) == 2


def test_add_html_file_not_exists():
    shaker = Shaker()
    with pytest.raises(FileNotFoundError):
        shaker.add_html_file('./tests/_data/html/missing.html')
        assert len(shaker.get_private_attributes().get('html_files', [])) == 0


def test_add_html_file_not_html():
    shaker = Shaker()
    with pytest.raises(ValueError):
        shaker.add_html_file('./tests/_data/html/no_html.xml')
        assert len(shaker.get_private_attributes().get('html_files', [])) == 0
