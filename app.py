import numpy as np
import pickle
from flask import Flask, request, render_template
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import pprint

app = Flask(__name__)
model = pickle.load(open("model.pkl", 'rb'))


@app.route('/')
def index():
    return render_template(
        'index.html',
        data=[{'gender': 'Gender'}, {'gender': 'female'}, {'gender': 'male'}],
        data1=[{'noc': 'Number of Children'}, {'noc': 0}, {'noc': 1}, {'noc': 2}, {'noc': 3}, {'noc': 4}, {'noc': 5}],
        data2=[{'smoke': 'Smoking Status'}, {'smoke': 'yes'}, {'smoke': 'no'}],
        data3=[{'region': "Region"}, {'region': "northeast"}, {'region': "northwest"},
               {'region': 'southeast'}, {'region': "southwest"}])


@app.route("/predict", methods=['GET', 'POST'])
def predict():

    # Fill in with your personal access token and org URL
    #personal_access_token = 'wzgh5o4f7osyirvxdy3l2rwoq6es2feqwjcz6qkfwfhqhp2ghsha'
    personal_access_token = 'iaychvpf23q4olefxi46ujmk3oz77mcpnsza5g57wl5tbc6w64ja'
    organization_url = 'https://dev.azure.com/AdilPathan'

    # Create a connection to the org
    credentials = BasicAuthentication('', personal_access_token)
    connection = Connection(base_url=organization_url, creds=credentials)

    # Get a client (the "core" client provides access to projects, teams, etc)
    core_client = connection.clients.get_core_client()
    #pprint.pprint(core_client)

    # Get the first page of projects
    # Get the first page of projects
    get_projects_response = core_client.get_projects()
    #print(get_projects_response)
    index = 0
    while get_projects_response is not None:
        for project in get_projects_response.value:
            pprint.pprint("[" + str(index) + "] " + project.name)
            index += 1
        if get_projects_response.continuation_token is not None and get_projects_response.continuation_token != "":
            # Get the next page of projects
            get_projects_response = core_client.get_projects(continuation_token=get_projects_response.continuation_token)
        else:
            # All projects have been retrieved
            get_projects_response = None

if __name__ == '__main__':
    app.run(debug=True)
