resource "kubernetes_deployment" "micro-queue"{
    depends_on = [kubernetes_persistent_volume.rabbitmq-pv]
    metadata {
        name = "micro-queue"
        namespace = "production"
        labels = {
            app = "micro-queue"
        }
    }
    spec {
        replicas = 1
        selector {
            match_labels = {
                app = "micro-queue"
            }
        }
        template {
            metadata {
                labels = {
                    app = "micro-queue"
                }
            }
            spec {
                container {
                    name = "micro-queue"
                    image = "rabbitmq:management"
                    env {
                        name = "RABBITMQ_DEFAULT_USER"
                        value = "admin"
                    }
                    env {
                        name = "RABBITMQ_DEFAULT_PASS"
                        value = "adminpass"
                    }
                    resources {
                        limits = {
                            memory = "128Mi"
                            cpu = "500m"
                        }
                        requests = {
                            memory = "128Mi"
                            cpu = "500m"
                        }
                    }
                    port {
                        name = "micro-queue"
                        container_port = 5672
                        host_port = 5672
                        protocol = "TCP"
                    }
                    port {
                        name = "queue-mgmt"
                        container_port = 15672
                        host_port = 15672
                        protocol = "TCP"
                    }
                    volume_mount {
                        name = "rabbitmq-local-storage"
                        mount_path = "/var/lib/rabbitmq"
                    }
                }
                volume {
                    name = "rabbitmq-local-storage"
                    persistent_volume_claim {
                        claim_name = "rabbitmq-pvc"
                    }
                }
            }
        }
    }
}