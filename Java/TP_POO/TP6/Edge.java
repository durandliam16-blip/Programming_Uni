import java.io.Serializable;

public class Edge implements Serializable {
    private City destination;
    private double weight;

    public Edge(City destination, double weight) {
        this.destination = destination;
        this.weight = weight;
    }

    public City getDestination() { return destination; }
    public double getWeight() { return weight; }
}