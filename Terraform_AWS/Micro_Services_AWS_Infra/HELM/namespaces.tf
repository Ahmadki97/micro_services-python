# Prometheus Name Space
resource "kubernetes_namespace" "prometheus" {
  metadata {
    name = "prometheus"
  }
}

# Grafana Name Space
resource "kubernetes_namespace" "grafana" {
    metadata {
      name = "grafana"
    }
}
