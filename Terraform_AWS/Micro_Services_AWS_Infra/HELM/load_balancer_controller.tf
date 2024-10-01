resource "helm_release" "aws-lb-controller" {
  name       = "load-lb-controller"
  namespace  = "kube-system"
  repository = "https://aws.github.io/eks-charts"
  chart      = "aws-load-balancer-controller"
  version    = "1.5.0" # You can specify the version you need here
  set {
    name  = "clusterName"
    value = "micro-eks"
  }
  set {
    name  = "serviceAccount.create"
    value = "false"
  }
  set {
    name  = "serviceAccount.name"
    value = var.lb_srvaccount
  }
  set {
    name  = "region"
    value = "us-east-1"
  }
  set {
    name  = "vpcId"
    value = var.vpc_id
  }
}
