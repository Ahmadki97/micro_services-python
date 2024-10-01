resource "helm_release" "Grafana" {
    name = "grafana"
    chart = "grafana"
    namespace = kubernetes_namespace.grafana.metadata[0].name
    create_namespace = true 
    repository = "https://grafana.github.io/helm-charts"
    depends_on = [kubernetes_namespace.grafana]
    # set {
    #     name = "serviceAccount.create"
    #     value = false
    # }
    # set {
    #     name = "serviceAccount.name"
    #     value = ""
    # }
}