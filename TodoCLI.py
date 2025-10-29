#!/usr/bin/env python3
"""
TodoCLI - Application de gestion de tâches en ligne de commande.

Exemple d'utilisation:
    python TodoCLI.py add "Faire les courses" "Acheter lait, pain et œufs"
    python TodoCLI.py list
    python TodoCLI.py done 1
    python TodoCLI.py remove 2
"""

import json
import os
import sys
from pathlib import Path

TASKS_FILE = Path(__file__).parent / "taches.txt"


def load_tasks():
    """Charge les tâches depuis le fichier de persistance."""
    if TASKS_FILE.exists():
        try:
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_tasks(tasks):
    """Sauvegarde les tâches dans le fichier de persistance."""
    try:
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Erreur lors de la sauvegarde: {e}")


def add_task(title, description):
    """Ajoute une nouvelle tâche."""
    tasks = load_tasks()
    
    task_id = max([t['id'] for t in tasks], default=0) + 1
    
    new_task = {
        'id': task_id,
        'title': title,
        'description': description,
        'done': False
    }
    
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"✓ Tâche ajoutée (ID: {task_id})")


def list_tasks():
    """Affiche toutes les tâches enregistrées."""
    tasks = load_tasks()
    
    if not tasks:
        print("Aucune tâche enregistrée.")
        return
    
    print("\n" + "="*70)
    print(f"{'ID':<4} {'Statut':<10} {'Titre':<25} {'Description':<25}")
    print("="*70)
    
    for task in tasks:
        status = "✓ Terminée" if task['done'] else "○ En cours"
        print(f"{task['id']:<4} {status:<10} {task['title']:<25} {task['description']:<25}")
    
    print("="*70 + "\n")


def mark_done(task_id):
    """Marque une tâche comme terminée."""
    tasks = load_tasks()
    
    task_found = False
    for task in tasks:
        if task['id'] == task_id:
            task['done'] = True
            task_found = True
            break
    
    if task_found:
        save_tasks(tasks)
        print(f"✓ Tâche {task_id} marquée comme terminée")
    else:
        print(f"✗ Tâche {task_id} non trouvée")


def remove_task(task_id):
    """Supprime une tâche par son identifiant."""
    tasks = load_tasks()
    
    initial_count = len(tasks)
    tasks = [t for t in tasks if t['id'] != task_id]
    
    if len(tasks) < initial_count:
        save_tasks(tasks)
        print(f"✓ Tâche {task_id} supprimée")
    else:
        print(f"✗ Tâche {task_id} non trouvée")


def main():
    """Fonction principale pour traiter les commandes."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python TodoCLI.py add \"titre\" \"description\"  - Ajouter une tâche")
        print("  python TodoCLI.py list                         - Afficher toutes les tâches")
        print("  python TodoCLI.py done <id>                   - Marquer comme terminée")
        print("  python TodoCLI.py remove <id>                 - Supprimer une tâche")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'add':
        if len(sys.argv) < 4:
            print("✗ Erreur: Utilise 'add \"titre\" \"description\"'")
            return
        title = sys.argv[2]
        description = sys.argv[3]
        add_task(title, description)
    
    elif command == 'list':
        list_tasks()
    
    elif command == 'done':
        if len(sys.argv) < 3:
            print("✗ Erreur: Utilise 'done <id>'")
            return
        try:
            task_id = int(sys.argv[2])
            mark_done(task_id)
        except ValueError:
            print("✗ Erreur: L'ID doit être un nombre")
    
    elif command == 'remove':
        if len(sys.argv) < 3:
            print("✗ Erreur: Utilise 'remove <id>'")
            return
        try:
            task_id = int(sys.argv[2])
            remove_task(task_id)
        except ValueError:
            print("✗ Erreur: L'ID doit être un nombre")
    
    else:
        print(f"✗ Commande inconnue: {command}")


if __name__ == '__main__':
    main()
