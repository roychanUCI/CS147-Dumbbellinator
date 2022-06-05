from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import json
import os
import base64
from io import BytesIO
import statistics


def renderSummaryPlot():
     
    #with open("./templates/index2.html", "r") as html_doc:
    #    soup = BeautifulSoup(html_doc, 'html.parser')
    #    soup.find(id="to-replace").string.replace_with('test')

    #with open("./templates/index2.html", "w") as html_doc_write:
    #    html_doc_write.write(soup.prettify())
   
    means = []
    sorted_file_names = []
    for filename in os.listdir("DATA"):
        sorted_file_names.append(filename)

    sorted_file_names.sort()

    for filename in sorted_file_names:
        f = os.path.join("DATA", filename)
        x = json.load(open(f, 'r'))
        yA = x["rep times"]
        xA = [i for i in range(len(yA))]
        mean = sum(yA)/len(yA)
        means.append(mean)
    
    fig = plt.figure()
    plt.plot(means, linestyle='solid')
    plt.xticks(range(len(means)))
    plt.xlabel('Set')
    plt.ylabel('Mean')
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    plt.clf()
    plt.close()
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    with open("./templates/index2.html", "r") as read_file:
        soup = BeautifulSoup(read_file, 'html.parser')
        for i in soup.find_all('img', class_='summary-plot-img'):
            i['src'] = "data:image/png;base64,{}".format(encoded)

    with open("./templates/index2.html", "w") as write_file:
        write_file.write(soup.prettify())

