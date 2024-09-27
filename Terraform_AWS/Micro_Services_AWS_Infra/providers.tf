provider "aws" {
  region     = "us-east-1" # Choose your desired AWS region
  access_key = "AKIAQGYBPY4VTPVHOPHV"
  secret_key = "PWBGC7vpFX1HBB9ObvdxOJOloOf+/neR6G1dVR+M"
}

provider "kubernetes" {
  host                   = module.EKS.eks-cluster-endpoint
  cluster_ca_certificate = base64decode(module.EKS.eks-cluster-ca)
  token                  = module.EKS.eks-cluster-token

}

provider "helm" {
  kubernetes {
    host                   = module.EKS.eks-cluster-endpoint
    cluster_ca_certificate = base64decode(module.EKS.eks-cluster-ca)
    token                  = module.EKS.eks-cluster-token
  }
}


