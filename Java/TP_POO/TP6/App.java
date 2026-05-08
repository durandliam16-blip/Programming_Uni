public class App {
    public static void main(String[] args) {
        RoadMap myMap = new RoadMap();

        // Ajout des villes
        String[] names = {"Rouen", "Paris", "Le Mans", "Rennes", "Brest", "Angers", "Tours", "Nantes", "Poitiers"};
        for (String n : names) myMap.addCity(n);

        // Ajout des routes (selon les valeurs du PDF)
        myMap.addRoad("Rouen", "Paris", 1.2);    // [cite: 10]
        myMap.addRoad("Rouen", "Rennes", 2.8);   // [cite: 11]
        myMap.addRoad("Rouen", "Le Mans", 1.9);  // [cite: 12]
        myMap.addRoad("Paris", "Le Mans", 1.8);  // [cite: 13]
        myMap.addRoad("Brest", "Rennes", 2.4);   // [cite: 14]
        myMap.addRoad("Rennes", "Le Mans", 0.9); // [cite: 15]
        myMap.addRoad("Rennes", "Nantes", 1.05); // [cite: 19]
        myMap.addRoad("Le Mans", "Angers", 0.95);// [cite: 17]
        myMap.addRoad("Le Mans", "Tours", 1.1);  // [cite: 18]
        myMap.addRoad("Angers", "Tours", 1.2);   // [cite: 21]
        myMap.addRoad("Angers", "Nantes", 0.95); // [cite: 20]
        myMap.addRoad("Nantes", "Poitiers", 2.1);// [cite: 24]
        myMap.addRoad("Tours", "Poitiers", 0.8); // [cite: 23]

        try {
            // Test Copie [cite: 48]
            RoadMap copyMap = myMap.clone();
            System.out.println("Égalité par == : " + (myMap == copyMap)); 
            System.out.println("Égalité par equals : " + myMap.equals(copyMap));

            // Test Sérialisation [cite: 62, 63]
            myMap.saveToFile("map_data.ser");
            RoadMap restoredMap = RoadMap.loadFromFile("map_data.ser");
            
            System.out.println("Chemin original (Brest -> Poitiers) : " + myMap.findPath("Brest", "Poitiers"));
            System.out.println("Chemin restauré (Brest -> Poitiers) : " + restoredMap.findPath("Brest", "Poitiers"));

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}