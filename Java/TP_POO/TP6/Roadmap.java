import java.io.*;
import java.util.*;

public class RoadMap implements Serializable, Cloneable {
    private Map<String, City> cities = new HashMap<>();

    public void addCity(String name) {
        cities.putIfAbsent(name, new City(name));
    }

    public void addRoad(String from, String to, double weight) {
        City start = cities.get(from);
        City end = cities.get(to);
        if (start != null && end != null) {
            start.addEdge(end, weight);
            end.addEdge(start, weight); // Graphe non-orienté
        }
    }

    // QUESTION 13 : Recherche de chemin (DFS simple)
    public List<String> findPath(String start, String end) {
        cities.values().forEach(c -> c.setVisited(false));
        List<String> path = new ArrayList<>();
        if (dfs(cities.get(start), end, path)) return path;
        return null;
    }

    private boolean dfs(City current, String target, List<String> path) {
        if (current == null) return false;
        current.setVisited(true);
        path.add(current.getName());

        if (current.getName().equals(target)) return true;

        for (Edge edge : current.getEdges()) {
            if (!edge.getDestination().isVisited()) {
                if (dfs(edge.getDestination(), target, path)) return true;
            }
        }
        path.remove(path.size() - 1);
        return false;
    }

    // QUESTION 10 : Copie Profonde via Sérialisation (méthode élégante pour les graphes)
    @Override
    public RoadMap clone() {
        try {
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            ObjectOutputStream oos = new ObjectOutputStream(baos);
            oos.writeObject(this);
            
            ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());
            ObjectInputStream ois = new ObjectInputStream(bais);
            return (RoadMap) ois.readObject();
        } catch (Exception e) {
            return null;
        }
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof RoadMap)) return false;
        RoadMap roadMap = (RoadMap) o;
        return Objects.equals(cities, roadMap.cities);
    }

    // Sérialisation vers fichier
    public void saveToFile(String filename) throws IOException {
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(filename))) {
            oos.writeObject(this);
        }
    }

    public static RoadMap loadFromFile(String filename) throws IOException, ClassNotFoundException {
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(filename))) {
            return (RoadMap) ois.readObject();
        }
    }
}