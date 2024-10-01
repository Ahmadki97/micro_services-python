resource "helm_release" "Prometheus" {
  name             = "prometheus"
  namespace        = kubernetes_namespace.prometheus.metadata[0].name
  chart            = "prometheus"
  repository = "https://prometheus-community.github.io/helm-charts"
  depends_on = [kubernetes_namespace.prometheus]

  set {
    name  = "alertmanager.persistence.storageClass"
    value = "gp2"
  }

  set {
    name  = "server.persistentVolume.storageClass"
    value = "gp2"
  }

}

