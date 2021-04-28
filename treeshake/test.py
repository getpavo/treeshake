from treeshake.shaker import Shaker

treeshaker = Shaker()
treeshaker.discover_add_stylesheets('./src/', True)
treeshaker.discover_add_html('./html/')
treeshaker.optimize('./out')
