from py2neo import Graph, Node, Relationship

# ----------------------------
# Thanks to :
# https://github.com/elena/py2neo-quickstart
# https://thibaut-deveraux.medium.com/how-to-install-neo4j-with-docker-compose-36e3ba939af0
# https://py2neo.org/2021.1/
# ----------------------------

# Connexion à la base de données Neo4j
graph = Graph("bolt://localhost:7687",auth=("neo4j","neo4j"))

# Fonction pour créer une entreprise
def creer_entreprise(nom):
    entreprise = Node("Entreprise", nom=nom)
    graph.create(entreprise)

# Fonction pour créer un utilisateur
def creer_utilisateur(nom, prenom, description, competences):
    utilisateur = Node("Utilisateur", nom=nom, prenom=prenom, description=description, competences=competences)
    graph.create(utilisateur)

# Fonction pour créer une relation "A travaillé pour"
def travailler_pour(utilisateur, entreprise, role, periode):
    relation = Relationship(utilisateur, "A_TRAVAILLE_POUR", entreprise, role=role, periode=periode)
    graph.create(relation)

# Fonction de recherche d'entreprises par nom
def rechercher_entreprises_par_nom(nom):
    query = "MATCH (entreprise:Entreprise) WHERE entreprise.nom CONTAINS $nom RETURN entreprise"
    result = graph.run(query, nom=nom)
    return result

# Fonction de recherche d'utilisateurs par nom
def rechercher_utilisateurs_par_nom(nom):
    query = "MATCH (utilisateur:Utilisateur) WHERE utilisateur.nom CONTAINS $nom RETURN utilisateur"
    result = graph.run(query, nom=nom)
    return result

# Fonction de suggestions de relations basée sur le travail en commun dans une entreprise donnée
def suggestions_relation_travail(utilisateur, entreprise):
    query = "MATCH (utilisateur)-[relation:A_TRAVAILLE_POUR]->(entreprise) WHERE entreprise.nom = $entreprise_nom AND NOT utilisateur = $utilisateur RETURN utilisateur"
    result = graph.run(query, entreprise_nom=entreprise, utilisateur=utilisateur)
    return result

# Fonction de suggestions de relations basée sur les connaissances d'un utilisateur donné
def suggestions_relation_connaissances(utilisateur):
    query = "MATCH (utilisateur)-[:A_TRAVAILLE_POUR]->(entreprise)<-[:A_TRAVAILLE_POUR]-(autre_utilisateur) WHERE NOT utilisateur = autre_utilisateur AND NOT (utilisateur)-[:CONNNAISSANCE]->(autre_utilisateur) RETURN autre_utilisateur"
    result = graph.run(query)
    return result

# Exemples d'utilisation des fonctions

# Création d'une entreprise
creer_entreprise("Acme Corporation")

# Création d'un utilisateur
creer_utilisateur("Alexis", "Dbn", "Développeur Python", ["Python", "SQL", "Web"])

# Création d'une relation "A travaillé pour"
utilisateur = graph.nodes.match("Utilisateur", nom="Doe").first()
entreprise = graph.nodes.match("Entreprise", nom="Acme Corporation").first()
travailler_pour(utilisateur, entreprise, "Salarié", "2020-2022")

# Recherche d'entreprises par nom
resultat_entreprises = rechercher_entreprises_par_nom("Acme")
for entreprise in resultat_entreprises:
    print(entreprise["entreprise"]["nom"])

# Recherche d'utilisateurs par nom
resultat_utilisateurs = rechercher_utilisateurs_par_nom("Dbn")
print(resultat_utilisateurs)
