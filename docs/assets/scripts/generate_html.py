import os

def indent(text, indentation):
    return ' ' * indentation * 2 + text + "\n"

for filename in os.listdir("../markdown/"):
    filename = filename.replace(".md", "")

    with open(f"../markdown/{filename}.md", "r") as input:
        markdown = input.readlines()

    content = []
    indentation = 4
    heading2 = False
    in_author_list = False
    in_affiliation_list = False
    for line in markdown:
        if line[:3] == "###":
            content.append(indent(f'<h3 class="project-heading-s">{line[3:].strip()}</h3>', indentation))
        elif line[:2] == "##":
            if heading2:
                indentation -= 1
                content.append(indent("</div>", indentation))
            else:
                heading2 = True
            content.append(indent('<div class="project-grid-row">', indentation))
            indentation += 1
            content.append(indent(f'<h2 class="project-heading-m">{line[2:].strip()}</h2>', indentation))
        elif line[0] == "#":
            content.append(indent('<div class="project-grid-row">', indentation))
            content.append(indent(f'<h1 class="project-heading-l">{line[1:].strip()}</h1>', indentation + 1))
            content.append(indent('</div>', indentation))
            title = line[1:].strip()
        elif line[:2] == "*C":
            content.append(indent('<div class="project-grid-row">', indentation))
            content.append(indent(f'<p class="project-conference-name project-body">{line[2:-3].strip()}</p>', indentation + 1))
            content.append(indent('</div>', indentation))
        elif line[:2] == "*A":
            if not in_author_list:
                content.append(indent('<div class="project-grid-row">', indentation))
                indentation += 1
                if line[2] == "u":
                    content.append(indent('<ul class="project-authors-list">', indentation))
                    is_ordered = False
                else:
                    content.append(indent('<ol class="project-authors-list">', indentation))
                    is_ordered = True
                indentation += 1

            author_name = line[line.find("[")+1:line.find("]")]
            if "(" in line:
                author_link = line[line.find("(")+1:line.find(")")]
            else:
                author_link = None
            if "{" in line:
                affiliations = line[line.find("{")+1:line.find("}")].split(",")
            else:
                affiliations = []
            content_line = "<li>"
            if author_link:
                content_line += f'<a href="{author_link}">'
            content_line += author_name
            if author_link:
                content_line += "</a>"
            for affiliation in affiliations:
                content_line += f'<a href="#{affiliation}" class="project-reference" aria-describedby="{affiliation}">{affiliation[11:]}</a>'
                if affiliation != affiliations[-1]:
                    content_line += '<span class="project-reference">,</span>'
            content_line += "</li>"
            content.append(indent(content_line, indentation))
            in_author_list = True
        elif line[:11] == "affiliation":
            if not in_affiliation_list:
                content.append(indent('<div class="project-grid-row">', indentation))
                indentation += 1
                content.append(indent('<ol class="project-affiliations-list">', indentation))
                indentation += 1
            content.append(indent(f'<li id="{line[:line.find(".")]}">{line[line.find(".")+1:].strip()}</li>', indentation))
            in_affiliation_list = True
        elif line[0] == "!":
            content.append(indent('<div class="project-grid-row">', indentation))
            if "[" in line:
                alt_text = f' alt="{line[line.find("[")+1:line.find("]")]}"'
            else:
                alt_text = ""
            content.append(indent(f'<img src="{line[line.find("(")+1:line.find(")")]}"{alt_text}>', indentation + 1))
            content.append(indent('</div>', indentation))
        elif line.strip() == "":
            if in_author_list:
                indentation -= 1
                if is_ordered:
                    content.append(indent("</ol>", indentation))
                else:
                    content.append(indent("</ul>", indentation))
                indentation -= 1
                content.append(indent("</div>", indentation))
            if in_affiliation_list:
                indentation -= 1
                content.append(indent("</ol>", indentation))
                indentation -= 1
                content.append(indent("</div>", indentation))
            in_author_list = False
            in_affiliation_list = False
        else:
            while "](" in line:
                start_url = line.find("](") + 2
                end_url = line.find(")", line.find("]("))
                link_url = line[start_url: end_url]

                start_link_text = line.find("](") - line[:line.find("](")][::-1].find("[")
                end_link_text = line.find("](")
                link_text = line[start_link_text: end_link_text]

                line = f'{line[:start_link_text - 1]}<a href="{link_url}">{link_text}</a>{line[end_url + 1:]}'

            content.append(indent(f'<p>{line.strip()}</p>', indentation))

    start = [indent('<!DOCTYPE html>', 0),
              indent('<html lang="en">', 0),
              indent('<head>', 1),
              indent(f'<title>{title}</title>', 2),
              indent('<link rel="stylesheet" type="text/css" href="docs/assets/css/styles.css">', 2),
              indent('</head>', 1),
              indent('<body class="project-font">', 1),
              indent('<main>', 2),
              indent('<div class="project-width-container">', 3)]

    end = [indent('</div>', 4),
           indent('</div>', 3),
           indent('</main>', 2),
           indent('</body>', 1),
           indent('</html>', 0)]

    with open(f"../../../{filename}.html", "w") as output_file:
        output_file.writelines(start)
        output_file.writelines(content)
        output_file.writelines(end)