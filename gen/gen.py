from pathlib import Path

pageTemplate = '''<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Showcase</title>
        <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css" rel="stylesheet">
        <link href="/showcase/css/styles.css" rel="stylesheet">
    </head>
    <body>
        <div id="wrap">
            <div class="navbar navbar-inverse" role="navigation">
                <div class="container">
                    <div class="navbar-header">
                        <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                            <span class="sr-only">Toggle navigation</span>
                            <span class="icon-bar"></span>
                            <span class="icon-bar"></span>
                            <span class="icon-bar"></span>
                        </button>
                        <a class="navbar-brand" href="/showcase/">Showcase</a>
                    </div>
                    <div class="navbar-collapse collapse">
                        <ul class="nav navbar-nav">
                            {{NAV}}
                        </ul>
                    </div>
                </div>
            </div>

            <div class="container" id="main">
                {{CONTENT}}
            </div>
        </div>

        <div id="footer">
            <hr>
            <div class="container">
                <small>All rights reserved.</small>
            </div>
        </div>

        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.3/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
    </body>
</html>
'''

homeContent = '''<h1 class="page-header">Photography Showcase <small>Micah Ng</small></h1>
<p>Here is a collection of my best photos, plus a few from my family. Select a year above to begin.</p>
'''

def listJpg(folder):
    imgs = list(Path(folder).rglob("*.[jJ][pP][gG]"))
    return sorted([str(img)[len(folder) + 1:] for img in imgs])

def listYears():
    folders = list(Path("../img").iterdir())
    return sorted([folder.name for folder in folders if folder.name.isdigit()])

def genNav(curYear):
    nav = ""
    for year in listYears():
        if year == curYear:
            nav += f'<li class="active"><a>{year}</a></li>'
        else:
            nav += f'<li><a href="/showcase/{year}">{year}</a></li>'
    return nav

with open("../index.html", "w") as f:
    f.write(pageTemplate.replace("{{NAV}}", genNav("")).replace("{{CONTENT}}", homeContent))

for year in listYears():
    jpgs = listJpg(f'../img/{year}')
    content = ""
    count = 0
    for jpg in jpgs:
        jpg = year + "/" + jpg
        if count % 2 == 0:
            if len(content) > 0:
                content += "</div>"
            content += '<div class="row">';
        content += f'<div class="col-md-6"><a href="/showcase/img/{jpg}" class="thumbnail">'
        filename = Path(jpg).name
        content += f'<img src="/showcase/img/thumb/{jpg}" alt="{filename}"></a></div>'
        count += 1
    content += "</div>"

    with open(f'../{year}.html', "w") as f:
        f.write(pageTemplate.replace("{{NAV}}", genNav(year)).replace("{{CONTENT}}", content))
