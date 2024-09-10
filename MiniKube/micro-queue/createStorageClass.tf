resource "kubernetes_storage_class" "rabbitmq_local_storage" {
  metadata {
    name = "rabbitmq-local-storage"
  }

  storage_provisioner = "kubernetes.io/no-provisioner"
  volume_binding_mode = "WaitForFirstConsumer"
  allow_volume_expansion = true
  reclaim_policy = "Delete"
}