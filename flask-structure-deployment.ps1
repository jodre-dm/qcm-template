# Définir la racine du projet
#$rootPath = "C:\chemin\vers\qcm_project"  # Remplacez par votre chemin souhaité

# Obtenir le chemin du dossier où se trouve le script .ps1
$rootPath = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Créer les dossiers
$folders = @(
    "$rootPath",
    "$rootPath\app",
    "$rootPath\app\templates",
    "$rootPath\app\static",
	"$rootPath\data"
)

foreach ($folder in $folders) {
    if (!(Test-Path -Path $folder)) {
        New-Item -ItemType Directory -Path $folder
    }
}

# Créer les fichiers
$files = @{
    "$rootPath\app\__init__.py"       = "# Initialisation de l'application Flask";
    "$rootPath\app\routes.py"         = "# Les routes de l'application";
    "$rootPath\app\templates\base.html"  = "<!-- Template de base -->";
    "$rootPath\app\templates\index.html" = "<!-- Page d'accueil -->";
    "$rootPath\app\templates\quiz.html"  = "<!-- Page pour le QCM -->";
    "$rootPath\app\static\styles.css"    = "/* Fichiers CSS */";
    "$rootPath\data\questions.py"      = "# questions du QCM";
	"$rootPath\run.py"                = "# Point d'entrée de l'application";
    "$rootPath\requirements.txt"      = "# Dépendances du projet";
	
}

foreach ($file in $files.GetEnumerator()) {
    $filePath = $file.Key
    $content = $file.Value

    if (!(Test-Path -Path $filePath)) {
        New-Item -ItemType File -Path $filePath -Force
        Set-Content -Path $filePath -Value $content
    }
}

Write-Host "Arborescence créée avec succès dans : $rootPath"
