from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import json
import os
import base64
from io import BytesIO
import statistics

def emptyPlot():
    with open("./templates/index3.html", "r") as read_file:
        soup = BeautifulSoup(read_file, 'html.parser')
        for i in soup.find_all('img', class_='summary-plot-img'):
            i['src'] = ""

        for j in soup.find_all('div', class_='doc-list'):
            j.clear()

            for fileName in os.listdir("DATA"):
                item_tag = soup.new_tag("li", class_="nav-item")
                link_tag = soup.new_tag("a", href=f"/individual-plots?file={fileName}", class_="nav-link active")
                link_tag.string = fileName

                item_tag.append(link_tag)
                j.append(link_tag)
                j.append(soup.new_tag("br"))




    with open("./templates/index3.html", "w") as write_file:
        write_file.write(soup.prettify())

def renderIndividualPlots(fileName):
    x = json.load(open(f"DATA/{fileName}", 'r'))
    yA = x["rep times"]
    xA = [i for i in range(len(yA))]
    mean = sum(yA)/len(yA)

    fig = plt.figure()
    plt.bar(xA, yA, color='maroon')
    plt.xlabel('Rep')
    plt.ylabel('Time Interval')
    subtitle = "Max: " + str(max(yA))
    subtitle += "/ Min: " + str(min(yA))
    subtitle += "/ Mean: " + str(sum(yA)/len(yA))
    subtitle += "\nStdDev: " + str(mean)
    fig.suptitle(subtitle)

    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    plt.clf()
    plt.close()
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    with open("./templates/index3.html", "r") as read_file:
        soup = BeautifulSoup(read_file, 'html.parser')
        for i in soup.find_all('img', class_='summary-plot-img'):
            i['src'] = "data:image/png;base64,{}".format(encoded)

    with open("./templates/index3.html", "w") as write_file:
        write_file.write(soup.prettify())


