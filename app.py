from flask import Flask , render_template,request
from summerize import summerizeApp

app = Flask(__name__)


def summarize_text(text):
    return "This is a summarized version of the text: "

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/summerize",methods=["GET","POST"])
def summerize():
    if request.method == "POST":
        rawText = request.form['rawText']
        # print(rawText)
        sum_text,len_sum,org_text,len_org_text,person,places,org,date = summerizeApp(rawText)
        # if summarized_text is None:
        # # Handle the case when summarize_text returns None
        #     summarized_text = 'Error: Unable to summarize the text.'
        # print(summarized_text)
    return render_template('summerize.html',sum_text=sum_text,org_text=org_text,len_org_text=len_org_text,len_sum=len_sum,person=person,places=places,org=org,date=date)

if __name__ == "__main__":
    app.run(debug=True)

