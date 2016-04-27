


from flask import Flask, render_template, send_file
import json
import analyzer


app = Flask('stalky')
persons = ['Lars Nedberg','Eyvind Gjertsen','Eirik Klevstad','Trond Hnsi','Jonathan Hansen','Eirik Fosser','Jon-Anders Kabbe','Astri Marie Ravnaas','Ann-Helen Brembo','Marianne Melhoos']


@app.route("/")
def hello():
    return render_template('main.html')

@app.route('/index')
def index():
    #Who do you want to show on the page
    people = analyzer.localtest(persons)
    timelist = []
    for time in people['ref']:


        timelist.append(str(time))

    del people['ref']
   # print people
    return render_template('index.html',people = people,timelist = timelist)

@app.route('/index/<int:backtrack_hours>')
def lasthours(backtrack_hours = None):

    #Who do you want to show on the page
    people = analyzer.last_x_hours(persons,backtrack_hours)
    timelist = []
    for time in people['ref']:


        timelist.append(str(time))

    del people['ref']
   # print people
    return render_template('index.html',people = people,timelist = timelist)



if __name__ == "__main__":
    app.run(debug=True)



