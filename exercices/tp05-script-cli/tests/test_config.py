# TODO : tester charger_config, en écrivant de petits fichiers dans tmp_path :
# - un fichier absent lève ConfigurationError ;
# - un fichier auquel il manque une clé (par exemple sans section sorties) lève ConfigurationError ;
# - un fichier qui n'est pas du YAML valide (par exemple "donnees: [ventes") lève ConfigurationError.
