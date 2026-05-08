import ollama
import subprocess
from smart_home import SmartHome
import os

def control_home(action, room):
    smart_home = SmartHome()
    if action == 'light_on':
        smart_home.light_on(room)
        return f'La lumière dans {room} est allumée.'
    elif action == 'light_off':
        smart_home.light_off(room)
        return f'La lumière dans {room} est éteinte.'
    elif action == 'get_temperature':
        temperature = smart_home.get_temperature(room)
        return f'Temperature dans {room}: {temperature}°C'
    else:
        return 'Action non reconnue.'

os.environ['NO_PROXY'] = 'localhost,127.0.0.1,::1'

client = ollama.Client(host = 'http://127.0.0.1:11434')


# ==============================================================================
# --- CONFIGURATION ---
MODEL = "gemma3:4b"

# Codes couleurs pour le terminal (Pédagogie visuelle)
class Colors:
    SYSTEM = '\033[95m'    # Messages système
    BLUE = '\033[94m'      # Pensées de l'IA
    GREEN = '\033[92m'     # Observations (Retour du système)
    YELLOW = '\033[93m'    # Actions décidées
    RED = '\033[91m'       # Erreurs
    ENDC = '\033[0m'
    BOLD = '\033[1m'


# ==============================================================================
# --- Initialisation du terminal pour le support des couleurs sous Windows

subprocess.run('', shell=True)


# ==============================================================================
# Étape 2 : Conception du Prompt Système
# ==============================================================================

def get_tools_list():
    """Retourne la liste des outils disponibles pour l'agent."""
    return """
- get_light_state(room_name) : Retourne l'état de la lumière dans une pièce.
- light_on(room_name) : Allume la lumière (salon, cuisine, chambre).
- light_off(room_name) : Éteint la lumière.
- get_temperature(room_name) : Donne la température actuelle.
"""

def get_system_prompt(tools_list):
    """Crée le prompt système pour l'agent domotique intelligent."""
    return f"""Tu es un assistant domotique intelligent contrôlant une maison connectée.

Tes responsabilités:
- Comprendre les demandes de l'utilisateur en français
- Utiliser les outils disponibles pour contrôler la maison
- Fournir un retour clair sur les actions effectuées

Outils disponibles:
{tools_list}
Format d'action: Utilise le format [TOOL](argument) pour appeler une fonction.
Exemple: [light_on](cuisine) pour allumer la cuisine.

Respecte ces règles:
1. Demande toujours confirmation avant une action majeure
2. Gère les erreurs avec clarté
3. Aide l'utilisateur à formuler ses demandes correctement
4. Explique ce que tu fais étape par étape
"""

# ==============================================================================
# Étape 5 : Prompt Dynamique
# ==============================================================================

def get_dynamic_system_prompt(actions):
    """Génère le prompt système en listant dynamiquement les outils disponibles."""
    tools_list = ""
    for tool_name, tool_func in actions.items():
        doc = tool_func.__doc__ if tool_func.__doc__ else "Pas de description disponible"
        tools_list += f"- {tool_name}: {doc.strip()}\n"
    return get_system_prompt(tools_list)


# ==============================================================================
# Étape 3 : La Boucle d'Exécution
# ==============================================================================

def get_available_tools(home):
    """Retourne un dictionnaire des outils disponibles pour l'agent."""
    return {
        "light_on": home.light_on,
        "light_off": home.light_off,
        "get_temperature": home.get_temperature
    }


def get_available_tools_auto(home):
    """Retourne un dictionnaire des outils disponibles pour l'agent en les récupérant dynamiquement."""
    tools = {}
    for method_name in dir(home):
        # Récupérer uniquement les méthodes publiques (ne commençant pas par _)
        if not method_name.startswith('_'):
            method = getattr(home, method_name)
            # Vérifier que c'est une méthode callable (pas un attribut)
            if callable(method):
                tools[method_name] = method
    return tools


def run_agent(actions, system_prompt):
    print(f"{Colors.SYSTEM}--- Démarrage de l'Agent Domotique (Modèle: {MODEL}) ---{Colors.ENDC}")
    print("Commandes possibles : 'Allume la cuisine', 'Quelle température fait-il ?', 'exit'")

    print(f"\n{Colors.GREEN}-> Fonctions disponibles pour l'agent :")
    for action in actions.keys():
        print(f"  - {Colors.YELLOW}{action}{Colors.GREEN}")
    print(f"{Colors.ENDC}")

    # Historique de conversation (Mémoire à court terme)
    history = [{'role': 'system', 'content': system_prompt}]

    while True:
        try:
            user_input = input(f"{Colors.YELLOW}User: {Colors.ENDC}")
            if user_input.lower() in ['exit', 'quit']:
                print(f"{Colors.SYSTEM}--- Arrêt de l'Agent Domotique ---{Colors.ENDC}")
                break

            # Ajouter l'entrée utilisateur à l'historique
            history.append({'role': 'user', 'content': user_input})

            # Boucle de résolution (Max 5 étapes pour éviter les boucles infinies)
            step = 0
            max_steps = 5
            while step < max_steps:
                # -------------------------------------------------------------------
                # 1 : Appel au modèle Ollama avec l'historique complet
                print(f"{Colors.SYSTEM}... Réflexion en cours ...{Colors.ENDC}")
                response = client.chat(model=MODEL, messages=history)
                ai_msg = response['message']['content'].strip()
 
                print(f"{Colors.SYSTEM}-> L'assistant pense :\n\t'{Colors.BLUE}{ai_msg}{Colors.SYSTEM}'{Colors.ENDC}\n")

                # Ajout de la réponse de l'IA à l'historique pour qu'elle s'en souvienne
                history.append({'role': 'assistant', 'content': ai_msg})

                # -------------------------------------------------------------------
                # 2 : Parsing de la réponse pour détecter une action
                action = None
                action_input = None
                # Chercher le format [TOOL](argument) dans la réponse
                import re
                match = re.search(r'\[(\w+)\]\((.*?)\)', ai_msg)
                if match:
                    action = match.group(1)
                    action_input = match.group(2)

                # -------------------------------------------------------------------
                # 3 : Exécution de l'action si détectée
                if action and action in actions:
                    print(f"{Colors.YELLOW}-> ACTION DÉTECTÉE : {action}('{action_input}'){Colors.ENDC}")

                    # Appeler la fonction Python correspondante et obtenir l'observation
                    try:
                        observation = actions[action](action_input)
                    except Exception as e:
                        observation = f"Erreur lors de l'exécution: {str(e)}"

                    # ---------------------------------------------------------------
                    # 4 : Ajout de l'observation à l'historique
                    print(f"{Colors.GREEN}-> OBSERVATION : {observation}{Colors.ENDC}")
                    # Ajouter l'observation à l'historique pour que l'IA s'en souvienne
                    history.append({'role': 'user', 'content': f'Observation: {observation}'})

                    step += 1
                else:
                    print(f"{Colors.GREEN}-> Aucune action détectée. L'agent a terminé sa réflexion.{Colors.ENDC}")
                    break

                if step == max_steps:
                    print(f"{Colors.RED}-> Limite de raisonnement atteinte (Boucle infinie ?){Colors.ENDC}")

        except KeyboardInterrupt:
            print(f"\n{Colors.SYSTEM}--- Arrêt forcé ---{Colors.ENDC}")
            break
        except Exception as e:
            print(f"{Colors.RED}--- Erreur Critique : {e}{Colors.ENDC}")
            print("Vérifiez qu'Ollama est bien lancé (ollama serve).")
            break


# ==============================================================================
# --- Fonction principale ---

if __name__ == "__main__":
    # Instanciation de la maison
    home = SmartHome()

    # Exemple d'utilisation des méthodes de SmartHome
    print(f"{Colors.SYSTEM}=> Test des fonctions de la maison connectée :{Colors.ENDC}")
    print(home.light_on("salon"))
    print(home.get_light_state("salon"))
    print(home.light_off("salon"))
    print(home.get_light_state("salon"))
    print(home.get_temperature("salon"))
    print()

    # Démarrage de l'agent simple
    print(f"{Colors.SYSTEM}=> Démarrage de l'agent domotique avec outils fixes...{Colors.ENDC}")
    actions = get_available_tools(home)
    system_prompt = get_system_prompt(get_tools_list())
    run_agent(actions, system_prompt)

    # Démarrage de l'agent avec outils dynamiques
    print(f"{Colors.SYSTEM}=> Démarrage de l'agent domotique avec outils dynamiques...{Colors.ENDC}")
    actions_dynamic = get_available_tools_auto(home)
    run_agent(actions_dynamic, get_dynamic_system_prompt(actions_dynamic))
