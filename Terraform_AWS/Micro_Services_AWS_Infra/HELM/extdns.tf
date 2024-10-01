resource "helm_release" "external_dns" {
  name             = "external-dns"
  chart            = "external-dns"
  namespace        = "kube-system" # You can change this to your desired namespace
  create_namespace = true
  repository       = "https://kubernetes-sigs.github.io/external-dns/"
  values = [
    <<EOF
      aws:
        region: "us-east-1"
        zoneType: "public"
        sources:
        - service
        - ingress
    EOF
  ]
  set {
    name  = "serviceAccount.create"
    value = "false"
  }
  set {
    name  = "serviceAccount.name"
    value = var.extdns_srvaccount
  }
}