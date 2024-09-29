resource "aws_iam_user" "micro" {
  name = "micro"
  tags = {
    info = "User to Run the microservices app"
  }
}



