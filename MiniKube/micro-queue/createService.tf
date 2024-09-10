resource "kubernetes_service" "micro_queue" {
  metadata {
    name      = "micro-queue"
    namespace = "production"
  }

  spec {
    type = "ClusterIP" 
    selector = {
      app = "micro-queue"
    }

    port {
      name        = "micro-queue"
      port        = 5672
      target_port = 5672
      protocol    = "TCP"
    }

    port {
      name        = "queue-mgmt"
      port        = 15672
      target_port = 15672
      protocol    = "TCP"
    }
  }
}
