resource "aws_iam_role" "Micro_EKS_Role" {
  name = "my-eks-role"
  # The assume_role_policy sepecifies which entities can assume this role 
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "eks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "Micro_EKS_Role_Attachment" {
  role       = aws_iam_role.Micro_EKS_Role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}



resource "aws_iam_role" "Micro_EKS_NodeGroup_Role" {
  name = "micro_eks_nodegroup_role"
  assume_role_policy = jsonencode({
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
    Version = "2012-10-17"
  })
}


resource "aws_iam_role_policy_attachment" "Micro_Node_Group_Attachments" {
  for_each   = toset(var.nodegroup_policies)
  role       = aws_iam_role.Micro_EKS_NodeGroup_Role.name
  policy_arn = each.value
}

# Role for the AWS Load Balancer Service Account
resource "aws_iam_role" "awslb-controller-role" {
  name = "AmazonEKSLoadBalancerControllerRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Federated = var.oidc_arn
      },
      Action = "sts:AssumeRoleWithWebIdentity",
      Condition = {
        StringEquals = {
          "${replace(var.oidc_arn, "arn:aws:iam::014498645803:oidc-provider/", "")}:sub" : "system:serviceaccount:kube-system:awslb"
        }
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "awslb-controller-role-attachment" {
  role       = aws_iam_role.awslb-controller-role.name
  policy_arn = "arn:aws:iam::014498645803:policy/AWSLoadBalancerControllerIAMPolicy"

}

# Role for external DNS Service Account
resource "aws_iam_role" "ExternalDNSServiceAccountRole" {
  name = "ExternalDNSServiceAccountRole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = var.oidc_arn
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "${replace(var.oidc_arn, "arn:aws:iam::014498645803:oidc-provider/", "")}:sub" : "system:serviceaccount:production:external-dns"
          }
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "extnds-policy-attachment" {
  role       = aws_iam_role.ExternalDNSServiceAccountRole.name
  policy_arn = aws_iam_policy.AllowExternalDNSUpdates.arn
}

