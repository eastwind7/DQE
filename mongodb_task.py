import csv
import argparse
import pymongo as pm


def parse_arguments():
    parser = argparse.ArgumentParser(description='Parses path to csv files to fill the database and get username and '
                                                 'pasword to database ')
    parser.add_argument('-projects', type=str, help='path to csv with projects')
    parser.add_argument('-tasks', type=str, help='path to csv with tasks')
    parser.add_argument('-user', type=str, help='username to mongo')
    parser.add_argument('-pwd', type=str, help='password to mongo')
    return parser.parse_args()


def _connect_mongo(host, port, db, username='', password=''):

    """ Create connection to database  """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s?authSource=admin' % (username, password, host, port, db)
        conn = pm.MongoClient(mongo_uri)
    else:
        conn = pm.MongoClient(host, port)
    return conn[db]


def fill_collection_with_csv(file_name, collection):
    """
            Reads data from csv file and fills the collection in DB with it.

           :param file_name: name of csv file with data.
           :param collection: collection in DB which we want to fill with data.
       """
    with open(file_name) as f:
        d = csv.DictReader(f)
        collection.insert_many(d)


def find_canceled_task_proj(task_collection):
    """
           Search for tasks with status = 'Canceled' and extracts from its object name of the project it belongs to .

           :param task_collection: the collection of tasks

    """
    canceled_tasks = task_collection.find({'status': 'Canceled'})
    projects = set()
    for t in canceled_tasks:
        projects.add(t["Project"])
    return list(projects)


def find_proj_details(project_collection, project_names):
    """
           Search for the rest information of the projects by names

           :param project_collection: collection of projects .
           :param project_names: names of projects which we looking for.

       """
    return project_collection.find({"Name": {"$in": list(project_names)}})


args = parse_arguments()
db = _connect_mongo('127.0.0.1', 27017, 'mydb1', 'helloworld', 'helloworld')
projects_collection = db["project"]
tasks_collection = db["tasks"]

fill_collection_with_csv(args.projects, projects_collection)
fill_collection_with_csv(args.tasks, tasks_collection)

canceled_task_proj = find_canceled_task_proj(tasks_collection)
# we don't need to call this function but in other case we never use our projects collection)
projects_details = find_proj_details(projects_collection, canceled_task_proj)

for project in projects_details:
    print(project["Name"])
