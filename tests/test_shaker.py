import pytest
import os
import shutil
from treeshake import Shaker


def test_add_stylesheet_exists():
    shaker = Shaker()
    file = './tests/_data/css/stylesheet.css'
    shaker.add_stylesheet(file)
    added_sheets = shaker.get_private_attributes().get('stylesheets', set())
    assert len(added_sheets) == 1
    assert next(iter(added_sheets)) == file
    shaker.add_stylesheet('./tests/_data/css/second.css')
    added_sheets = shaker.get_private_attributes().get('stylesheets', set())
    assert len(added_sheets) == 2


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
    added_files = shaker.get_private_attributes().get('html_files', [])
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


def test_discover_add_stylesheets():
    shaker = Shaker()
    shaker.discover_add_stylesheets('./tests/_data/css/', True)
    added_sheets = shaker.get_private_attributes().get('stylesheets', set())
    assert len(added_sheets) == 2
    gen = iter(added_sheets)
    first_sheet = next(gen)
    assert first_sheet == './tests/_data/css/second.css' or first_sheet == './tests/_data/css/stylesheet.css'
    second_sheet = next(gen)
    assert second_sheet == './tests/_data/css/second.css' or second_sheet == './tests/_data/css/stylesheet.css'
    assert first_sheet != second_sheet


def test_discover_add_html_files():
    shaker = Shaker()
    shaker.discover_add_html('./tests/_data/html/', True)
    added_files = shaker.get_private_attributes().get('html_files', set())
    assert len(added_files) == 2
    gen = iter(added_files)
    first_file = next(gen)
    assert first_file == './tests/_data/html/index.html' or first_file == './tests/_data/html/job.html'
    second_file = next(gen)
    assert second_file == './tests/_data/html/index.html' or second_file == './tests/_data/html/job.html'
    assert first_file != second_file


def test_optimize_stylesheet():
    output_folder = './tests/_data/output/'
    shutil.rmtree(output_folder)
    os.mkdir(output_folder)
    assert os.path.exists(output_folder)
    assert len(os.listdir(output_folder)) == 0

    shaker = Shaker()
    shaker.discover_add_stylesheets('./tests/_data/css/', True)
    shaker.discover_add_html('./tests/_data/html/', True)
    private_attributes = shaker.get_private_attributes()
    assert len(private_attributes.get('stylesheets', set())) == 2
    assert len(private_attributes.get('html_files', [])) == 2

    shaker.optimize(output_folder)
    assert len(os.listdir(output_folder)) == 1

    with open(output_folder + 'stylesheet.css', 'r') as f:
        assert f.readline().strip() == 'h1 {'
        assert f.readline().strip() == 'font-family: Comic Sans MS, serif'
        assert f.readline().strip() == '}'
        cur = f.tell()  # save current position
        f.seek(0, os.SEEK_END)
        end = f.tell()  # find the size of file
        f.seek(cur, os.SEEK_SET)
        assert cur == end
