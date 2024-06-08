from urllib.parse import quote
# Define the path to your ontology file here
ONTOLOGY_FILE = 'data/my_ontology.owl'
from owlready2 import *
from rdflib import *
from datetime import date

onto_path.append(ONTOLOGY_FILE)
onto = get_ontology("data/my_ontology.owl").load()

level_mapping = {
    'LowLevel': 'LowLevel',
    'MediumLevel': 'MediumLevel',
    'AdvancedLevel': 'AdvancedLevel'
}

def query_class_instances(class_uri):
    # Construct the SPARQL query
    q = f"""
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX licenta_onto: <http://www.semanticweb.org/suciu/ontologies/2023/4/licenta_onto#>
        SELECT ?name ?description
        WHERE {{
            ?individual rdf:type licenta_onto:{class_uri} ;
                        licenta_onto:hasName ?name ;
                        licenta_onto:hasDescription ?description .
        }}
    """

    rdf_graph = onto.world.as_rdflib_graph()
    results = rdf_graph.query(q)

    return  parse_response(results)

def query_class_instances_by_part(class_uri, domain_name):
    domain_name_encoded = quote(domain_name)
    class_uri_encoded = quote(class_uri)

    domain_uri = f"""http://www.semanticweb.org/suciu/ontologies/2023/4/licenta_onto#{domain_name.replace(' ', '_')}"""

    query = f"""
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX licenta_onto: <http://www.semanticweb.org/suciu/ontologies/2023/4/licenta_onto#>
        SELECT ?name ?description
        WHERE {{
            ?individual rdf:type licenta_onto:{class_uri} ;
                        licenta_onto:hasName ?name ;
                        licenta_onto:hasDescription ?description ;
                        licenta_onto:isPartOf <{domain_uri} .
        }}
    """
    rdf_graph = onto.world.as_rdflib_graph()
    results = rdf_graph.query(query)

    return parse_response(results)

def parse_response(results):
    parsed_data = {}
    id = 0
    for row in results:
        try:
            topic = str(row["name"])
            description = str(row["description"])
            parsed_data[id] = {"name": topic, "description": description}
            id += 1
        except Exception as e:
            print(f"Error parsing row: {e}")
    return parsed_data


def get_instance_by_name(cls, names):
    instances = []
    if isinstance(names, str):  # Check if input is a string
        for instance in cls.instances():
            if instance.name == names:
                instances.append(instance)
    else:  # Assume it's a list
        for name in names:
            for instance in cls.instances():
                if instance.name == name.replace(" ", "_"):
                    instances.append(instance)
    return instances


def query_assigned_courses_for_student(student_username):

    student_uri = f"""http://www.semanticweb.org/suciu/ontologies/2023/4/licenta_onto#{student_username.replace(' ', '_')}"""
    q = f"""
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX licenta_onto: <http://www.semanticweb.org/suciu/ontologies/2023/4/licenta_onto#>
        SELECT ?courseName
        WHERE {{
            <{student_uri}> licenta_onto:assignedCourse ?course .
            ?course licenta_onto:hasName ?courseName .
        }}
    """

    # Execute the SPARQL query
    rdf_graph = onto.world.as_rdflib_graph()
    results = rdf_graph.query(q)

    # Return the list of assigned courses for the student
    parsed_data = []
    for row in results:
        try:
            topic = str(row["courseName"])
            parsed_data.append(topic)
        except Exception as e:
            print(f"Error parsing row: {e}")
    return parsed_data


def retrieve_course_from_ontology(courseName):

    graph = Graph()
    graph.parse(data=onto.world.as_rdflib_graph().serialize(format='turtle'), format='turtle')

    course_uri = f"""http://www.semanticweb.org/suciu/ontologies/2023/4/licenta_onto#{courseName.replace(' ', '_')}"""

    q = f"""
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX licenta_onto: <http://www.semanticweb.org/suciu/ontologies/2023/4/licenta_onto#>
        SELECT ?courseName ?courseDescription ?courseLevel
        WHERE {{
                <{course_uri}>  licenta_onto:hasName ?courseName ;
                                licenta_onto:hasDescription ?courseDescription ;
                                licenta_onto:hasStudyLevel ?level .
                
                ?level rdf:type licenta_onto:Level ;
                        licenta_onto:hasName ?courseLevel .

        }}
    """
    try:
        # Convert ontology to RDFLib graph
        # rdf_graph = onto.world.as_rdflib_graph()
        # print("RDFLib graph created successfully.")

        # Execute the query
        results = graph.query(q)
        print("Query executed successfully.")
        
        # Process the results
        for course in results:
            print(course)
            response = {
                "name": course.courseName,
                "description":  course.courseDescription,
                "level": course.courseLevel
            }
            return response

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def compute_learning_data(course_names):
    course_names_str = " ,".join([f'"{name}"' for name in course_names])
    query = f"""
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX licenta_onto: <http://www.semanticweb.org/suciu/ontologies/2023/4/licenta_onto#>
        SELECT ?domainName ?domainDescription ?courseName ?courseDescription
        WHERE {{
                ?course rdf:type licenta_onto:Course ;
                        licenta_onto:hasName ?courseName ;
                        licenta_onto:hasDescription ?courseDescription ;
                        licenta_onto:isPartOf ?domain .
                
                ?domain rdf:type licenta_onto:Domain ;
                        licenta_onto:hasDescription ?domainDescription ;
                        licenta_onto:hasName ?domainName .
        }}
    """
    
    rdf_graph = onto.world.as_rdflib_graph()
    results = rdf_graph.query(query)
    formatted_results = defaultdict(lambda: {'domain_description': '', 'courses': []})
    for row in results:
        try:
            course_name = str(row['courseName'])
            if course_name not in course_names:
                continue
            domain_name = str(row['domainName'])
            domain_description = str(row['domainDescription'])
            course_name = str(row['courseName'])
            course_description = str(row['courseDescription']) if row["courseDescription"] else ""
            course = {
                'name': course_name,
                'description': course_description
            }
            formatted_results[domain_name]['domain_description'] = domain_description
            formatted_results[domain_name]['courses'].append(course)
        except Exception as e:
            print(f"Error parsing row: {e}")
    return formatted_results

def compute_course_details(course_name):
    graph = Graph()
    graph.parse(data=onto.world.as_rdflib_graph().serialize(format='turtle'), format='turtle')
    
    course_uri = f"""http://www.semanticweb.org/suciu/ontologies/2023/4/licenta_onto#{course_name.replace(' ', '_')}"""
    q = f"""
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX licenta_onto: <http://www.semanticweb.org/suciu/ontologies/2023/4/licenta_onto#>
        SELECT ?domainName ?courseName ?courseDescription
        WHERE {{
                <{course_uri}> licenta_onto:hasName ?courseName ;
                                licenta_onto:hasDescription ?courseDescription ;
                                licenta_onto:isPartOf ?domain .
                
                ?domain rdf:type licenta_onto:Domain ;
                        licenta_onto:hasName ?domainName .
        }}
    """

    try:
        # Convert ontology to RDFLib graph
        # rdf_graph = onto.world.as_rdflib_graph()
        # print("RDFLib graph created successfully.")

        # Execute the query
        results = graph.query(q)
        print("Query executed successfully.")
        
        # Process the results
        for course in results:
            print(course)
            response = {
                "courseName": course.courseName,
                "courseDomain":  course.domainName,
                "courseDescription": course.courseDescription
            }
            return response

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_computer_science_domains(course_names):
    Course = onto.Course
    Domain =onto.Domain
    response = []
    domain_counts = {}

    query = f"""
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX licenta_onto: <http://www.semanticweb.org/suciu/ontologies/2023/4/licenta_onto#>
        SELECT ?domainName ?courseName
        WHERE {{
                ?course rdf:type licenta_onto:Course ;
                        licenta_onto:hasName ?courseName ;
                        licenta_onto:isPartOf ?domain .
                
                ?domain rdf:type licenta_onto:Domain ;
                        licenta_onto:hasName ?domainName .
        }}
    """
    
    rdf_graph = onto.world.as_rdflib_graph()
    results = rdf_graph.query(query)
    for row in results:
        try:
            course_name = str(row['courseName'])
            if course_name not in course_names:
                continue
            domain_name = str(row['domainName'])
            if domain_name not in domain_counts:
                domain_counts[domain_name] = 0
            domain_counts[domain_name] += 1
        except Exception as e:
            print(f"Error parsing row: {e}")

    for domain, student_count in domain_counts.items():
        domain_item = {
            "domain": domain,
            "studentsEnrolled": student_count
        }
        response.append(domain_item)
    return response


with onto:
    class VarkEntity(Thing): pass
    class LevelEntity(Thing): pass
    class NamedEntity(Thing):
        pass
    class DescribedEntity(Thing):
        pass
    class Student(VarkEntity, LevelEntity):
        pass
    class Course(NamedEntity, DescribedEntity, LevelEntity):
        pass
    class Domain(NamedEntity, DescribedEntity):
        pass
    class Vark(NamedEntity):
        pass
    class Level(NamedEntity):
        pass
    class Interest(NamedEntity, DescribedEntity):
        pass
    class Goal(NamedEntity, DescribedEntity):
        pass
    class Material(NamedEntity, DescribedEntity, VarkEntity):
        pass
    class Project(NamedEntity, DescribedEntity, VarkEntity):
        pass
    class Evaluation(Thing):
        pass

    class hasVarkModel(ObjectProperty):
        domain = [VarkEntity]
        range = [Vark]

    class hasStudyLevel(ObjectProperty):
        domain = [LevelEntity]
        range = [Level]
    
    class hasInterest(ObjectProperty):
        domain = [Student]
        range = [Interest]

    class hasGoal(ObjectProperty):
        domain = [Student]
        range = [Goal]

    class assignedCourse(ObjectProperty):
        domain = [Student]
        range = [Course]

    class relatedTo(ObjectProperty):
        domain = [Goal]
        range = [Domain]

    class relevantFor(ObjectProperty):
        domain = [Interest]
        range = [Domain]

    class isPartOf(ObjectProperty):
        domain = [Course]
        range = [Domain]

    class hasMaterial(ObjectProperty):
        domain = [Course]
        range = [Material]

    class atEndOf(ObjectProperty):
        domain = [Evaluation]
        range = [Course]

    class afterStudy(ObjectProperty):
        domain = [Project]
        range = [Material]

    class hasEmail(DataProperty):
        domain = [Student]
        range = [str]

    class date_of_birth(DataProperty):
        domain = [Student]
        range = [date]

    class first_name(DataProperty):
        domain = [Student]
        range = [str]

    class last_name(DataProperty):
        domain = [Student]
        range = [str]

    class hasName(DataProperty):
        domain = [NamedEntity]
        range = [str]

    class hasDescription(DataProperty):
        domain = [DescribedEntity]
        range = [str]

    class hasLink(DataProperty):
        domain = [Material]
        range = [str]

onto.save(file=ONTOLOGY_FILE)

    # AllDisjoint([Student, Course, Domain, Vark, Level, Interest, Goal, Material, Project, Evaluation])

def add_student(student_data):
    vark_model =  get_instance_by_name(onto.Vark, student_data["vark_model"]) or onto.Vark(student_data["vark_model"])
    study_level = get_instance_by_name(onto.Level, student_data["level"]) or onto.Level(student_data["level"])
    interests = get_instance_by_name(onto.Interest, student_data["interests"]) or onto.Interest(student_data["interests"])
    goals = get_instance_by_name(onto.Goal, student_data["goals"]) or onto.Goal(student_data["goals"])
    student = Student(student_data["username"].replace(" ", "_"))
    student.hasEmail = [student_data["email"]]
    student.date_of_birth = [student_data["date_of_birth"]]
    student.first_name = [student_data["first_name"]]
    student.last_name = [student_data["last_name"]]
    student.hasVarkModel = vark_model
    student.hasStudyLevel = study_level
    student.hasInterest = interests
    student.hasGoal = goals
    onto.save(file=ONTOLOGY_FILE)


with onto:
    rule_curriculum_generation = Imp()
    rule_curriculum_generation.set_as_rule(
        """
        hasVarkModel(?student, ?vark) ^ 
        hasStudyLevel(?student, ?level) ^ 
        hasInterest(?student, ?interest) ^ 
        hasGoal(?student, ?goal) ^
        relatedTo(?goal, ?domain) ^ 
        relevantFor(?interest, ?domain) ^
        isPartOf(?course, ?domain) ^ 
        hasStudyLevel(?course, ?level) ^ 
        -> assignedCourse(?student, ?course)
        """
    )

    rule_project_generation = Imp()
    rule_project_generation.set_as_rule(
        """
        hasVarkModel(?student, ?vark) ^ 
        hasStudyLevel(?student, ?level) ^ 
        hasMaterial (?material, ?course) ^
        
        afterStudy(?project, ?material) ^ 
        hasStudyLevel(?project, ?level) ^

        """
    )
onto.save(file=ONTOLOGY_FILE)



with onto:
    class VarkEntity(Thing): pass
    class LevelEntity(Thing): pass
    class NamedEntity(Thing):
        pass
    class DescribedEntity(Thing):
        pass
    class Student(VarkEntity, LevelEntity):
        pass
    class Course(NamedEntity, DescribedEntity, LevelEntity):
        pass
    class Domain(NamedEntity, DescribedEntity):
        pass
    class Vark(NamedEntity):
        pass
    class Level(NamedEntity):
        pass
    class Interest(NamedEntity, DescribedEntity):
        pass
    class Goal(NamedEntity, DescribedEntity):
        pass
    class Material(NamedEntity, DescribedEntity, VarkEntity):
        pass
    class Project(NamedEntity, DescribedEntity, VarkEntity):
        pass
    class Evaluation(Thing):
        pass

    class hasVarkModel(ObjectProperty):
        domain = [VarkEntity]
        range = [Vark]

    class hasStudyLevel(ObjectProperty):
        domain = [LevelEntity]
        range = [Level]
    
    class hasInterest(ObjectProperty):
        domain = [Student]
        range = [Interest]

    class hasGoal(ObjectProperty):
        domain = [Student]
        range = [Goal]

    class assignedCourse(ObjectProperty):
        domain = [Student]
        range = [Course]
    
    class assigendProject(ObjectProperty):
        domain = [Student]
        range = [Project]

    class assigendMaterial(ObjectProperty):
        domain = [Student]
        range = [Material]

    class relatedTo(ObjectProperty):
        domain = [Goal]
        range = [Domain]

    class relevantFor(ObjectProperty):
        domain = [Interest]
        range = [Domain]

    class isPartOf(ObjectProperty):
        domain = [Course]
        range = [Domain]

    class hasMaterial(ObjectProperty):
        domain = [Course]
        range = [Material]

    class atEndOf(ObjectProperty):
        domain = [Evaluation]
        range = [Course]

    class afterStudy(ObjectProperty):
        domain = [Project]
        range = [Material]

    class hasEmail(DataProperty):
        domain = [Student]
        range = [str]

    class date_of_birth(DataProperty):
        domain = [Student]
        range = [date]

    class first_name(DataProperty):
        domain = [Student]
        range = [str]

    class last_name(DataProperty):
        domain = [Student]
        range = [str]

    class hasName(DataProperty):
        domain = [NamedEntity]
        range = [str]

    class hasDescription(DataProperty):
        domain = [DescribedEntity]
        range = [str]

    class hasLink(DataProperty):
        domain = [Material]
        range = [str]

onto.save(file=ONTOLOGY_FILE)

    # AllDisjoint([Student, Course, Domain, Vark, Level, Interest, Goal, Material, Project, Evaluation])

def add_student(student_data):
    vark_model =  get_instance_by_name(onto.Vark, student_data["vark_model"]) or onto.Vark(student_data["vark_model"])
    study_level = get_instance_by_name(onto.Level, student_data["level"]) or onto.Level(student_data["level"])
    interests = get_instance_by_name(onto.Interest, student_data["interests"]) or onto.Interest(student_data["interests"])
    goals = get_instance_by_name(onto.Goal, student_data["goals"]) or onto.Goal(student_data["goals"])
    student = Student(student_data["username"].replace(" ", "_"))
    student.hasEmail = [student_data["email"]]
    student.date_of_birth = [student_data["date_of_birth"]]
    student.first_name = [student_data["first_name"]]
    student.last_name = [student_data["last_name"]]
    student.hasVarkModel = vark_model
    student.hasStudyLevel = study_level
    student.hasInterest = interests
    student.hasGoal = goals
    onto.save(file=ONTOLOGY_FILE)


with onto:
    rule_curriculum_generation = Imp()
    rule_curriculum_generation.set_as_rule(
        """
        hasVarkModel(?student, ?vark) ^ 
        hasStudyLevel(?student, ?level) ^ 
        hasInterest(?student, ?interest) ^ 
        hasGoal(?student, ?goal) ^
        relatedTo(?goal, ?domain) ^ 
        relevantFor(?interest, ?domain) ^
        isPartOf(?course, ?domain) ^ 
        hasStudyLevel(?course, ?level) ^ 
        -> assignedCourse(?student, ?course)
        """
    )
onto.save(file=ONTOLOGY_FILE)

def calculate_curricula(student_data):
    onto = get_ontology("data/my_ontology.owl").load()

    with onto:
        sync_reasoner_pellet(infer_property_values=True, debug=1)
        assigned_courses = query_assigned_courses_for_student(student_data)
        return assigned_courses
    return "Could Not calculate curricula"
