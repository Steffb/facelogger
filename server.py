


from flask import Flask, render_template, send_file
import json
import analyzer


app = Flask('stalky')
persons = ['Lars Nedberg','Eyvind Gjertsen','Eirik Klevstad','Trond Hnsi','Jonathan Hansen','Eirik Fosser','Jon-Anders Kabbe','Astri Marie Ravnaas','Ann-Helen Brembo','Marianne Melhoos']

def get_early(people):
    list = []
    earliest= 999
    # Determine what the earlies entry was
    for person in people.keys():
        counter =0
        for element in people[person]:

            if (element and counter<earliest):
                earliest =counter
                print counter
                print person
            counter+=1
    print earliest
    # Determine who is was
    for person,value in people.iteritems():

        if(value[earliest]):

            list.append(person)
    return list

def most_active(people):
    # Only returns the last person in the list with max on registerd
    active_person =''
    value =0
    earliest= 999
    # Determine what the earlies entry was
    for person in people.keys():
        counter =0
        for element in people[person]:
            counter+=element
        if(counter>=value):
            value = counter
            active_person = person
    return active_person

    # Determine who is was
    for person in people.keys():
        if(person.value[earliest]):
            list.append(person)
    return person


@app.route("/")
def hello():
    return render_template('main.html')

@app.route('/index')
def index():
    #Who do you want to show on the page
    people,sorted_names = analyzer.last_x_hours(persons,13)
    timelist = []
    for time in people['ref']:
        timelist.append(str(time))

    del people['ref']

    earlybird = get_early(people)
    activist = most_active(people)
   # print people
    return render_template('index.html',people = people,timelist = timelist,activist = activist,earlybird = earlybird, sorted_names = sorted_names)


@app.route('/index/<int:backtrack_hours>')
def lasthours(backtrack_hours = None):
    #Show only for the last hours hours given in the url

    #Who do you want to show on the page
    people,sorted_names = analyzer.last_x_hours(persons,backtrack_hours)
    timelist = []
    for time in people['ref']:


        timelist.append(str(time))

    del people['ref']
    earlybird = get_early(people)
    activist = most_active(people)
   # print people
    return render_template('index.html',people = people,timelist = timelist,activist = activist,earlybird = earlybird, sorted_names = sorted_names)



if __name__ == "__main__":
    app.run(debug=True)



