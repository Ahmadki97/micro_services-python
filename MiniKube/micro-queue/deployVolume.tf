resource "kubernetes_persistent_volume" "rabbitmq-pv"{
    metadata {
        name = "rabbitmq-pv"
    }
    spec { 
        storage_class_name = "rabbitmq-local-storage"
        capacity = {
            storage = "1Gi"
        }
        access_modes = ["ReadWriteOnce"]
        persistent_volume_source {
            host_path {
                path = "/storage/data1"
            }
        }
    }
}
resource "kubernetes_persistent_volume_claim" "rabbitmq-pvc" {
    depends_on = [kubernetes_persistent_volume.rabbitmq-pv]
    metadata {
        name = "rabbitmq-pvc"
        namespace = "production"
    }
    spec {
        storage_class_name = "rabbitmq-local-storage"
        access_modes = ["ReadWriteOnce"]
        resources {
            requests = {
                storage = "1Gi"
            }
        }
        volume_mode = "Filesystem"
    }
}