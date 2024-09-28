# Policy for the micro_user
resource "aws_iam_user_policy_attachment" "micro_User_Policy" {
  user       = aws_iam_user.micro.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

resource "aws_iam_policy" "AllowExternalDNSUpdates" {
  name        = "AllowExternalDNSUpdates"
  description = "A policy to allow external dns updates using our eks cluster services and ingresses."

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "route53:ChangeResourceRecordSets"
        ]
        Resource = [
          "arn:aws:route53:::hostedzone/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "route53:ListHostedZones",
          "route53:ListResourceRecordSets",
          "route53:ListTagsForResource"
        ]
        Resource = [
          "*"
        ]
      }
    ]
  })
}


