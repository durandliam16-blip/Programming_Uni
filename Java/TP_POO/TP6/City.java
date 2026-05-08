import java.io.Serializable;
import java.util.*;

public class City implements Serializable, Cloneable {
    private String name;
    private List<Edge> edges;
    private transient boolean visited; // transient car l'état de visite n'est pas structurel

    public City(String name) {
        this.name = name;
        this.edges = new ArrayList<>();
        this.visited = false;
    }

    public void addEdge(City destination, double weight) {
        edges.add(new Edge(destination, weight));
    }

    // Getters et Setters
    public String getName() { return name; }
    public List<Edge> getEdges() { return edges; }
    public boolean isVisited() { return visited; }
    public void setVisited(boolean visited) { this.visited = visited; }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder(name + " connectée à : ");
        for (Edge e : edges) {
            sb.append(String.format("[%s (%.2f)] ", e.getDestination().getName(), e.getWeight()));
        }
        return sb.toString();
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        City city = (City) o;
        return Objects.equals(name, city.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name);
    }

    // Clonage superficiel par défaut
    @Override
    protected Object clone() throws CloneNotSupportedException {
        return super.clone();
    }
}