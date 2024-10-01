# resource "aws_elasticache_cluster" "Micro_Elastic_Cache_Cluster" {
#   cluster_id                 = "micro-elastic-cache-cluster"
#   engine                     = "redis"
#   node_type                  = "cache.t2.micro"
#   num_cache_nodes            = 1
#   subnet_group_name          = aws_elasticache_subnet_group.Cache_Subnet_Group.name
#   parameter_group_name       = "default.redis3.2"
#   engine_version             = "3.2.10"
#   port                       = 6379
#   transit_encryption_enabled = false
# }

resource "aws_elasticache_cluster" "example" {
  cluster_id           = "cluster-example"
  engine               = "redis"
  node_type            = "cache.m4.large"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis3.2"
  engine_version       = "3.2.10"
  port                 = 6379
}