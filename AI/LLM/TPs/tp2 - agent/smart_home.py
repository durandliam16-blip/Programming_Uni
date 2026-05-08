# ==============================================================================
# Étape 1 : Conception de la Maison Domotique
# ==============================================================================

"""Le systeme physique que l'IA va controler."""
class SmartHome:
    def __init__(self):
        # État initial de la maison
        self.rooms = ["salon", "cuisine", "chambre"]
        self.state = {}
        for room in self.rooms:
            self.state[room] = False  # False = Éteint
        self.state["temperature"] = 19.5

    def get_light_state(self, room):
        """Retourne l'état de la lumière dans une pièce."""
        if room not in self.rooms:
            return f"Erreur: {room} n'existe pas. Pièces disponibles: {', '.join(self.rooms)}"
        state = self.state.get(room, False)
        return f"La lumière dans {room} est {'allumée' if state else 'éteinte'}."

    def light_on(self, room):
        """Allume la lumière dans une pièce."""
        if room not in self.rooms:
            return f"Erreur: {room} n'existe pas. Pièces disponibles: {', '.join(self.rooms)}"
        self.state[room] = True
        return f"La lumière dans {room} est allumée."

    def light_off(self, room):
        """Éteint la lumière dans une pièce."""
        if room not in self.rooms:
            return f"Erreur: {room} n'existe pas. Pièces disponibles: {', '.join(self.rooms)}"
        self.state[room] = False
        return f"La lumière dans {room} est éteinte."

    def get_temperature(self, room):
        """Retourne la température de la pièce spécifiée."""
        if room not in self.rooms and room != "general":
            return f"Erreur: {room} n'existe pas. Pièces disponibles: {', '.join(self.rooms)}"
        temp = self.state.get("temperature", 19.5)
        return f"La température actuelle est {temp}°C."


# ==============================================================================
# --- Codes couleurs pour les tests ---
# ==============================================================================

class Colors:
    SYSTEM = '\033[95m'    # Magenta
    BLUE = '\033[94m'      # Bleu
    GREEN = '\033[92m'     # Vert
    YELLOW = '\033[93m'    # Jaune
    RED = '\033[91m'       # Rouge
    ENDC = '\033[0m'
    BOLD = '\033[1m'


# ==============================================================================
# --- Tests ---
# ==============================================================================

if __name__ == "__main__":
    import subprocess
    
    # Initialiser les couleurs sous Windows
    subprocess.run('', shell=True)
    
    home = SmartHome()
    
    print(f"\n{Colors.BOLD}{Colors.SYSTEM}╔═══════════════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.SYSTEM}  ║     TEST DE LA MAISON DOMOTIQUE (SmartHome)                  ║{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.SYSTEM}  ╚═══════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")
    
    # ==== TEST 1 : Vérifier l'état initial ====
    print(f"{Colors.YELLOW}[TEST 1] État initial de la maison:{Colors.ENDC}")
    print(f"  {Colors.GREEN}Pièces: {home.rooms}{Colors.ENDC}")
    print(f"  {Colors.GREEN}État des lumières: {home.state}{Colors.ENDC}")
    print(f"  {Colors.GREEN}Température initiale: {home.state['temperature']}°C{Colors.ENDC}\n")
    
    # ==== TEST 2 : Allumer et éteindre les lumières ====
    print(f"{Colors.YELLOW}[TEST 2] Contrôle des lumières:{Colors.ENDC}")
    for room in home.rooms:
        print(f"  {Colors.BLUE}→ Allumer {room}:{Colors.ENDC}")
        print(f"    {Colors.GREEN}{home.light_on(room)}{Colors.ENDC}")
        print(f"  {Colors.BLUE}→ État:{Colors.ENDC}")
        print(f"    {Colors.GREEN}{home.get_light_state(room)}{Colors.ENDC}")
        print(f"  {Colors.BLUE}→ Éteindre {room}:{Colors.ENDC}")
        print(f"    {Colors.GREEN}{home.light_off(room)}{Colors.ENDC}\n")
    
    # ==== TEST 3 : Vérifier la température ====
    print(f"{Colors.YELLOW}[TEST 3] Température:{Colors.ENDC}")
    print(f"  {Colors.GREEN}{home.get_temperature('salon')}{Colors.ENDC}\n")
    
    # ==== TEST 4 : Gestion des erreurs (pièce invalide) ====
    print(f"{Colors.YELLOW}[TEST 4] Gestion des erreurs (pièce invalide):{Colors.ENDC}")
    print(f"  {Colors.RED}{home.light_on('garage')}{Colors.ENDC}")
    print(f"  {Colors.RED}{home.get_light_state('grenier')}{Colors.ENDC}\n")
    
    # ==== TEST 5 : État final ====
    print(f"{Colors.YELLOW}[TEST 5] État final de la maison:{Colors.ENDC}")
    print(f"  {Colors.GREEN}État des lumières: {home.state}{Colors.ENDC}")
    print(f"  {Colors.GREEN}Toutes les lumières sont éteintes: {all(not home.state[room] for room in home.rooms)}{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}{Colors.SYSTEM}╔═══════════════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.SYSTEM}║                    TESTS TERMINÉS                             ║{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.SYSTEM}╚═══════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")