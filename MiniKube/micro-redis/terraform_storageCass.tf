provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_storage_class" "redis_local_storage" {
  metadata {
    name = "redis-local-storage"
  }

  provisioner = "kubernetes.io/no-provisioner"
  volume_binding_mode = "WaitForFirstConsumer"
  allow_volume_expansion = true
  reclaim_policy = "Delete"
}
