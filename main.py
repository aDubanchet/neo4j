from py2neo import Graph, Node, Relationship

# ----------------------------
# Thanks to :
# https://github.com/elena/py2neo-quickstart
# https://thibaut-deveraux.medium.com/how-to-install-neo4j-with-docker-compose-36e3ba939af0
# https://py2neo.org/2021.1/
# ----------------------------

# Connexion à la base de données Neo4j
graph = Graph("neo4j://localhost:7687",auth=("neo4j","password"))


# ----------------------------
# Création des noeuds 
# ----------------------------
def creer_entreprise(nom):
    entreprise = Node("Entreprise", nom=nom)

    tx = graph.begin()
    tx.create(entreprise)
    return entreprise

def creer_utilisateur(nom, prenom, description, competences):
    utilisateur = Node("Utilisateur", nom=nom, prenom=prenom, description=description, competences=competences)
    
    tx = graph.begin()
    tx.create(utilisateur)
    return utilisateur

# ----------------------------
# Relations entre les noeuds
# ----------------------------
def travailler_pour(utilisateur, entreprise, role, periode):
    # creation d'une relation entre les noeuds
    relation = Relationship(utilisateur, "A_TRAVAILLE_POUR", entreprise, role=role, periode=periode)
    
    tx = graph.begin()
    tx.create(relation)

# ----------------------------
# Fonctions de recherche
# ----------------------------

def rechercher_entreprises_par_nom(nom):
    query = "MATCH (entreprise:Entreprise) WHERE entreprise.nom CONTAINS $nom RETURN entreprise"
    result = graph.run(query, nom=nom)
    return result


def rechercher_utilisateurs_par_nom(nom):
    query = "MATCH (utilisateur:Utilisateur) WHERE utilisateur.nom CONTAINS $nom RETURN utilisateur"
    result = graph.run(query, nom=nom)
    return result

# ----------------------------
# Suggestions
# ----------------------------

def suggestions_relation_travail(utilisateur, entreprise):
    # suggestions de relations basée sur le travail en commun dans une entreprise donnée
    query = "MATCH (utilisateur)-[relation:A_TRAVAILLE_POUR]->(entreprise) WHERE entreprise.nom = $entreprise_nom AND NOT utilisateur = $utilisateur RETURN utilisateur"
    result = graph.run(query, entreprise_nom=entreprise, utilisateur=utilisateur)
    return result

def suggestions_relation_connaissances(utilisateur):
    # suggestions de relations basée sur les connaissances d'un utilisateur donné
    query = "MATCH (utilisateur)-[:A_TRAVAILLE_POUR]->(entreprise)<-[:A_TRAVAILLE_POUR]-(autre_utilisateur) WHERE NOT utilisateur = autre_utilisateur AND NOT (utilisateur)-[:CONNNAISSANCE]->(autre_utilisateur) RETURN autre_utilisateur"
    result = graph.run(query)
    return result



# Test

# Création d'une entreprise
entreprise = creer_entreprise("Relais de l'abbaye")


# Création d'un utilisateur
utilisateur = creer_utilisateur("Alexis", "Dbn", "Développeur Python", ["Python", "SQL", "Web"])


# Création d'une relation "A travaillé pour"
print("utilisateur :",utilisateur)
print("entreprise : ",entreprise)
travailler_pour(utilisateur, entreprise, "Salarié", "2020-2022")

# Recherche d'entreprise
resultat_entreprises = rechercher_entreprises_par_nom("Relais de l'abbaye")
print("-------------------")
print("Recherche entreprise :")
for entreprise in resultat_entreprises:
    print(entreprise["entreprise"]["nom"])

# Recherche d'utilisateur
print("-------------------")
print("Recherche utilisateurs :")
resultat_utilisateurs = rechercher_utilisateurs_par_nom("Dbn")
print(resultat_utilisateurs)
