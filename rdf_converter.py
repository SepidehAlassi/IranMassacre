from rdflib import Graph, Literal, URIRef

from rdflib.namespace import RDF, RDFS, XSD, SDO

from rdflib.namespace import Namespace


pvvo_onto = Namespace("http://www.pvvo.com/ontology/")
pvvo_graph = Graph()
pvvo_graph.bind("pvvo", pvvo_onto)
pvvo_graph.bind("rdf", RDF)
pvvo_graph.bind("rdfs", RDFS)
pvvo_graph.bind("schema", SDO)
pvvo_graph.bind("xsd", XSD)
WiKi = Namespace("http://en.wikipedia.org/wiki/")
pvvo_graph.bind("wiki", WiKi)

OntologyIRI = URIRef(pvvo_onto)

#************ Classes *************#
# Person Class
Person = pvvo_onto.Person
pvvo_graph.add((Person, RDF.type, RDF.Class))
pvvo_graph.add((Person, RDFS.label, Literal("Person")))
pvvo_graph.add((Person, RDFS.comment, Literal("A person")))
pvvo_graph.add((Person, RDFS.subClassOf, SDO.Person))

# Location Class
Location = pvvo_onto.Location
pvvo_graph.add((Location, RDF.type, RDF.Class))
pvvo_graph.add((Location, RDFS.label, Literal("Location")))
pvvo_graph.add((Location, RDFS.comment, Literal("A Location")))
pvvo_graph.add((Location, RDFS.subClassOf, SDO.Place))

# University Class
University = pvvo_onto.University
pvvo_graph.add((University, RDF.type, RDF.Class))
pvvo_graph.add((University, RDFS.label, Literal("University")))
pvvo_graph.add((University, RDFS.comment, Literal("A University")))
pvvo_graph.add((University, RDFS.subClassOf, SDO.CollegeOrUniversity))

#************ Properties *************#
#*** Person Properties ****

# Person ID
personId = pvvo_onto.personID
pvvo_graph.add((personId, RDF.type, RDF.Property))
pvvo_graph.add((personId, RDFS.label, Literal("Person ID")))
pvvo_graph.add((personId, RDFS.comment, Literal("The person's ID")))
pvvo_graph.add((personId, RDFS.range, XSD.string))
pvvo_graph.add((personId, RDFS.domain, Person))

# Gender
gender = pvvo_onto.isFemale
pvvo_graph.add((gender, RDF.type, RDF.Property))
pvvo_graph.add((gender, RDFS.label, Literal("gender")))
pvvo_graph.add((gender, RDFS.comment, Literal("The person is female or male")))
pvvo_graph.add((gender, RDFS.range, XSD.boolean))
pvvo_graph.add((gender, RDFS.domain, Person))

# Neighbourhood
neighbourhood = pvvo_onto.neighbourhood
pvvo_graph.add((neighbourhood, RDF.type, RDF.Property))
pvvo_graph.add((neighbourhood, RDFS.label, Literal("Neighbourhood")))
pvvo_graph.add((neighbourhood, RDFS.comment, Literal("Death Neighbourhood")))
pvvo_graph.add((neighbourhood, RDFS.range, XSD.string))
pvvo_graph.add((neighbourhood, RDFS.domain, Person))

# Age
age = pvvo_onto.age
pvvo_graph.add((age, RDF.type, RDF.Property))
pvvo_graph.add((age, RDFS.label, Literal("Age")))
pvvo_graph.add((age, RDFS.comment, Literal("Age of the person")))
pvvo_graph.add((age, RDFS.range, XSD.integer))
pvvo_graph.add((age, RDFS.domain, Person))

# Birthplace
birthPlace = pvvo_onto.birthPlace
pvvo_graph.add((birthPlace, RDF.type, RDF.Property))
pvvo_graph.add((birthPlace, RDFS.label, Literal("Birth Place")))
pvvo_graph.add((birthPlace, RDFS.comment, Literal("Birthplace of the person")))
pvvo_graph.add((birthPlace, RDFS.range, Location))
pvvo_graph.add((birthPlace, RDFS.domain, Person))

# Death Place
deathPlace = pvvo_onto.deathPlace
pvvo_graph.add((deathPlace, RDF.type, RDF.Property))
pvvo_graph.add((deathPlace, RDFS.label, Literal("Death Place")))
pvvo_graph.add((deathPlace, RDFS.comment, Literal("Death place of the person")))
pvvo_graph.add((deathPlace, RDFS.range, Location))
pvvo_graph.add((deathPlace, RDFS.domain, Person))

# Burial Place
burialPlace = pvvo_onto.burialPlace
pvvo_graph.add((burialPlace, RDF.type, RDF.Property))
pvvo_graph.add((burialPlace, RDFS.label, Literal("Burial Place")))
pvvo_graph.add((burialPlace, RDFS.comment, Literal("Burial place of the person")))
pvvo_graph.add((burialPlace, RDFS.range, Location))
pvvo_graph.add((burialPlace, RDFS.domain, Person))

# Burial Date
burialDate = pvvo_onto.burialDate
pvvo_graph.add((burialDate, RDF.type, RDF.Property))
pvvo_graph.add((burialDate, RDFS.label, Literal("Burial Date")))
pvvo_graph.add((burialDate, RDFS.comment, Literal("Burial date of the person")))
pvvo_graph.add((burialDate, RDFS.range, XSD.date))
pvvo_graph.add((burialDate, RDFS.domain, Person))

# Arrest Date
arrestDate = pvvo_onto.arrestDate
pvvo_graph.add((arrestDate, RDF.type, RDF.Property))
pvvo_graph.add((arrestDate, RDFS.label, Literal("Arrest Date")))
pvvo_graph.add((arrestDate, RDFS.comment, Literal("Arrest date of the person")))
pvvo_graph.add((arrestDate, RDFS.range, XSD.date))
pvvo_graph.add((arrestDate, RDFS.domain, Person))

# Arrest Place
arrestPlace = pvvo_onto.arrestPlace
pvvo_graph.add((arrestPlace, RDF.type, RDF.Property))
pvvo_graph.add((arrestPlace, RDFS.label, Literal("Arrest Place")))
pvvo_graph.add((arrestPlace, RDFS.comment, Literal("Arrest Place of the person")))
pvvo_graph.add((arrestPlace, RDFS.range, Location))
pvvo_graph.add((arrestPlace, RDFS.domain, Person))

# relatedTo
relatedTo = pvvo_onto.relatedTo
pvvo_graph.add((relatedTo, RDF.type, RDF.Property))
pvvo_graph.add((relatedTo, RDFS.label, Literal("Personal Relationship")))
pvvo_graph.add((relatedTo, RDFS.comment, Literal("person related to another person")))
pvvo_graph.add((relatedTo, RDFS.range, Person))
pvvo_graph.add((relatedTo, RDFS.domain, Person))

# deathType
deathType = pvvo_onto.deathType
pvvo_graph.add((deathType, RDF.type, RDF.Property))
pvvo_graph.add((deathType, RDFS.label, Literal("Type of Death")))
pvvo_graph.add((deathType, RDFS.comment, Literal("A person's death type")))
pvvo_graph.add((deathType, RDFS.range, XSD.string))
pvvo_graph.add((deathType, RDFS.domain, Person))

# disability
disability = pvvo_onto.disability
pvvo_graph.add((disability, RDF.type, RDF.Property))
pvvo_graph.add((disability, RDFS.label, Literal("Disability")))
pvvo_graph.add((disability, RDFS.comment, Literal("A person's disability")))
pvvo_graph.add((disability, RDFS.range, XSD.string))
pvvo_graph.add((disability, RDFS.domain, Person))

# profession
profession = pvvo_onto.profession
pvvo_graph.add((profession, RDF.type, RDF.Property))
pvvo_graph.add((profession, RDFS.label, Literal("Profession")))
pvvo_graph.add((profession, RDFS.comment, Literal("A person's profession")))
pvvo_graph.add((profession, RDFS.domain, Person))
pvvo_graph.add((profession, RDFS.subPropertyOf, SDO.hasOccupation))

# wasStudent
wasStudent = pvvo_onto.wasStudent
pvvo_graph.add((wasStudent, RDF.type, RDF.Property))
pvvo_graph.add((wasStudent, RDFS.label, Literal("wasStudent")))
pvvo_graph.add((wasStudent, RDFS.comment, Literal("A person was a student or not")))
pvvo_graph.add((wasStudent, RDFS.domain, Person))
pvvo_graph.add((wasStudent, RDFS.range, XSD.boolean))

# affiliation
affiliation = pvvo_onto.affiliation
pvvo_graph.add((affiliation, RDF.type, RDF.Property))
pvvo_graph.add((affiliation, RDFS.label, Literal("Affiliation")))
pvvo_graph.add((affiliation, RDFS.comment, Literal("A person's affiliation with a university'")))
pvvo_graph.add((affiliation, RDFS.domain, Person))
pvvo_graph.add((affiliation, RDFS.range, University))

# studyField
studyField = pvvo_onto.studyField
pvvo_graph.add((studyField, RDF.type, RDF.Property))
pvvo_graph.add((studyField, RDFS.label, Literal("Field of Study")))
pvvo_graph.add((studyField, RDFS.comment, Literal("A person's field of study at a university'")))
pvvo_graph.add((studyField, RDFS.domain, Person))
pvvo_graph.add((studyField, RDFS.range, XSD.string))


# attendedProtestAt
attendedProtestAt = pvvo_onto.attendedProtestAt
pvvo_graph.add((attendedProtestAt, RDF.type, RDF.Property))
pvvo_graph.add((attendedProtestAt, RDFS.label, Literal("Attended Protest at")))
pvvo_graph.add((attendedProtestAt, RDFS.comment, Literal("Location where a person attended a protest")))
pvvo_graph.add((attendedProtestAt, RDFS.domain, Person))
pvvo_graph.add((attendedProtestAt, RDFS.range, Location))

# disappearanceDate
disappearanceDate = pvvo_onto.disappearanceDate
pvvo_graph.add((disappearanceDate, RDF.type, RDF.Property))
pvvo_graph.add((disappearanceDate, RDFS.label, Literal("Disappearance Date")))
pvvo_graph.add((disappearanceDate, RDFS.comment, Literal("Date when a person disappeared")))
pvvo_graph.add((disappearanceDate, RDFS.domain, Person))
pvvo_graph.add((disappearanceDate, RDFS.range, XSD.date))

# wasAthlete
wasAthlete = pvvo_onto.wasAthlete
pvvo_graph.add((wasAthlete, RDF.type, RDF.Property))
pvvo_graph.add((wasAthlete, RDFS.label, Literal("was athlete")))
pvvo_graph.add((wasAthlete, RDFS.comment, Literal("Person was an athlete or not")))
pvvo_graph.add((wasAthlete, RDFS.domain, Person))
pvvo_graph.add((wasAthlete, RDFS.range, XSD.boolean))

# sportType
sportType = pvvo_onto.sportType
pvvo_graph.add((sportType, RDF.type, RDF.Property))
pvvo_graph.add((sportType, RDFS.label, Literal("Sport Type")))
pvvo_graph.add((sportType, RDFS.comment, Literal("Person's type of sport")))
pvvo_graph.add((sportType, RDFS.domain, Person))
pvvo_graph.add((sportType, RDFS.range, WiKi.Q31629))

# injuryDate
injuryDate = pvvo_onto.injuryDate
pvvo_graph.add((injuryDate, RDF.type, RDF.Property))
pvvo_graph.add((injuryDate, RDFS.label, Literal("Injury Date")))
pvvo_graph.add((injuryDate, RDFS.comment, Literal("Person's date of injury")))
pvvo_graph.add((injuryDate, RDFS.domain, Person))
pvvo_graph.add((injuryDate, RDFS.range, XSD.date))


#*** Location Properties ****
# belongsToProvince
belongsToProvince = pvvo_onto.belongsToProvince
pvvo_graph.add((belongsToProvince, RDF.type, RDF.Property))
pvvo_graph.add((belongsToProvince, RDFS.label, Literal("Belongs to Provice")))
pvvo_graph.add((belongsToProvince, RDFS.comment, Literal("Province a city belongs to")))
pvvo_graph.add((belongsToProvince, RDFS.domain, Location))
pvvo_graph.add((belongsToProvince, RDFS.range, WiKi.Q34876))

# wikiLink
wikiLink = pvvo_onto.wikiLink
pvvo_graph.add((wikiLink, RDF.type, RDF.Property))
pvvo_graph.add((wikiLink, RDFS.label, Literal("Link to Wikidata Resource")))
pvvo_graph.add((wikiLink, RDFS.comment, Literal("Link to Wikidata Resource")))




