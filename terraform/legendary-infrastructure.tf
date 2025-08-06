# File: terraform/legendary-infrastructure.tf
# N3EXTPATH HR Platform - Complete AWS Infrastructure
# Built: 2025-08-05 17:58:53 UTC by RICKROLL187
# WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.20"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.10"
    }
  }
  
  backend "s3" {
    bucket = "n3extpath-terraform-state-legendary"
    key    = "legendary-hr-platform/terraform.tfstate"
    region = "us-west-2"
    
    dynamodb_table = "n3extpath-terraform-locks-legendary"
    encrypt        = true
    
    # Legendary state management
    tags = {
      Environment    = "production"
      Project       = "n3extpath-hr"
      BuiltBy       = "rickroll187"
      LegendaryStatus = "maximum"
      SwissPrecision = "enabled"
      CodeBroEnergy  = "infinite"
    }
  }
}

# Variables
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "n3extpath-legendary-cluster"
}

variable "legendary_founder" {
  description = "Legendary founder username"
  type        = string
  default     = "rickroll187"
  sensitive   = true
}

# Local values
locals {
  common_tags = {
    Environment     = var.environment
    Project        = "n3extpath-hr"
    BuiltBy        = "rickroll187"
    LegendaryStatus = "maximum"
    SwissPrecision  = "enabled"
    CodeBroEnergy   = "infinite"
    ManagedBy      = "terraform"
    CreatedAt      = "2025-08-05T17:58:53Z"
  }
  
  # Availability zones for legendary high availability
  availability_zones = ["${var.region}a", "${var.region}b", "${var.region}c"]
}

# Data sources
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# VPC for legendary networking
resource "aws_vpc" "legendary_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-vpc"
    Type = "legendary-networking"
  })
}

# Internet Gateway for legendary connectivity
resource "aws_internet_gateway" "legendary_igw" {
  vpc_id = aws_vpc.legendary_vpc.id
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-igw"
    Type = "legendary-gateway"
  })
}

# Public Subnets for legendary load balancers
resource "aws_subnet" "legendary_public_subnets" {
  count = length(local.availability_zones)
  
  vpc_id                  = aws_vpc.legendary_vpc.id
  cidr_block              = "10.0.${count.index + 1}.0/24"
  availability_zone       = local.availability_zones[count.index]
  map_public_ip_on_launch = true
  
  tags = merge(local.common_tags, {
    Name                              = "n3extpath-legendary-public-${count.index + 1}"
    Type                              = "legendary-public-subnet"
    "kubernetes.io/role/elb"          = "1"
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
  })
}

# Private Subnets for legendary application workloads
resource "aws_subnet" "legendary_private_subnets" {
  count = length(local.availability_zones)
  
  vpc_id            = aws_vpc.legendary_vpc.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = local.availability_zones[count.index]
  
  tags = merge(local.common_tags, {
    Name                              = "n3extpath-legendary-private-${count.index + 1}"
    Type                              = "legendary-private-subnet"
    "kubernetes.io/role/internal-elb" = "1"
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
  })
}

# Database Subnets for legendary data storage
resource "aws_subnet" "legendary_database_subnets" {
  count = length(local.availability_zones)
  
  vpc_id            = aws_vpc.legendary_vpc.id
  cidr_block        = "10.0.${count.index + 20}.0/24"
  availability_zone = local.availability_zones[count.index]
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-database-${count.index + 1}"
    Type = "legendary-database-subnet"
  })
}

# NAT Gateways for legendary outbound connectivity
resource "aws_eip" "legendary_nat_eips" {
  count = length(local.availability_zones)
  
  domain = "vpc"
  
  depends_on = [aws_internet_gateway.legendary_igw]
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-nat-eip-${count.index + 1}"
    Type = "legendary-elastic-ip"
  })
}

resource "aws_nat_gateway" "legendary_nat_gateways" {
  count = length(local.availability_zones)
  
  allocation_id = aws_eip.legendary_nat_eips[count.index].id
  subnet_id     = aws_subnet.legendary_public_subnets[count.index].id
  
  depends_on = [aws_internet_gateway.legendary_igw]
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-nat-${count.index + 1}"
    Type = "legendary-nat-gateway"
  })
}

# Route Tables for legendary routing
resource "aws_route_table" "legendary_public_rt" {
  vpc_id = aws_vpc.legendary_vpc.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.legendary_igw.id
  }
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-public-rt"
    Type = "legendary-route-table"
  })
}

resource "aws_route_table" "legendary_private_rt" {
  count = length(local.availability_zones)
  
  vpc_id = aws_vpc.legendary_vpc.id
  
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.legendary_nat_gateways[count.index].id
  }
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-private-rt-${count.index + 1}"
    Type = "legendary-route-table"
  })
}

# Route Table Associations
resource "aws_route_table_association" "legendary_public_rta" {
  count = length(aws_subnet.legendary_public_subnets)
  
  subnet_id      = aws_subnet.legendary_public_subnets[count.index].id
  route_table_id = aws_route_table.legendary_public_rt.id
}

resource "aws_route_table_association" "legendary_private_rta" {
  count = length(aws_subnet.legendary_private_subnets)
  
  subnet_id      = aws_subnet.legendary_private_subnets[count.index].id
  route_table_id = aws_route_table.legendary_private_rt[count.index].id
}

# Security Groups for legendary protection
resource "aws_security_group" "legendary_eks_cluster_sg" {
  name_prefix = "n3extpath-legendary-eks-cluster-"
  vpc_id      = aws_vpc.legendary_vpc.id
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-eks-cluster-sg"
    Type = "legendary-security-group"
  })
}

resource "aws_security_group" "legendary_eks_node_sg" {
  name_prefix = "n3extpath-legendary-eks-node-"
  vpc_id      = aws_vpc.legendary_vpc.id
  
  ingress {
    from_port = 0
    to_port   = 65535
    protocol  = "tcp"
    self      = true
  }
  
  ingress {
    from_port       = 1025
    to_port         = 65535
    protocol        = "tcp"
    security_groups = [aws_security_group.legendary_eks_cluster_sg.id]
  }
  
  ingress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.legendary_eks_cluster_sg.id]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-eks-node-sg"
    Type = "legendary-security-group"
  })
}

# RDS Security Group
resource "aws_security_group" "legendary_rds_sg" {
  name_prefix = "n3extpath-legendary-rds-"
  vpc_id      = aws_vpc.legendary_vpc.id
  
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.legendary_eks_node_sg.id]
  }
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-rds-sg"
    Type = "legendary-security-group"
  })
}

# ElastiCache Security Group
resource "aws_security_group" "legendary_elasticache_sg" {
  name_prefix = "n3extpath-legendary-elasticache-"
  vpc_id      = aws_vpc.legendary_vpc.id
  
  ingress {
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [aws_security_group.legendary_eks_node_sg.id]
  }
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-elasticache-sg"
    Type = "legendary-security-group"
  })
}

# IAM Role for EKS Cluster
resource "aws_iam_role" "legendary_eks_cluster_role" {
  name = "n3extpath-legendary-eks-cluster-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
      }
    ]
  })
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-eks-cluster-role"
    Type = "legendary-iam-role"
  })
}

resource "aws_iam_role_policy_attachment" "legendary_eks_cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.legendary_eks_cluster_role.name
}

# IAM Role for EKS Node Group
resource "aws_iam_role" "legendary_eks_node_role" {
  name = "n3extpath-legendary-eks-node-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-eks-node-role"
    Type = "legendary-iam-role"
  })
}

resource "aws_iam_role_policy_attachment" "legendary_eks_worker_node_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.legendary_eks_node_role.name
}

resource "aws_iam_role_policy_attachment" "legendary_eks_cni_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.legendary_eks_node_role.name
}

resource "aws_iam_role_policy_attachment" "legendary_eks_container_registry_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.legendary_eks_node_role.name
}

# EKS Cluster - The Legendary Heart
resource "aws_eks_cluster" "legendary_cluster" {
  name     = var.cluster_name
  role_arn = aws_iam_role.legendary_eks_cluster_role.arn
  version  = "1.27"
  
  vpc_config {
    subnet_ids              = concat(aws_subnet.legendary_public_subnets[*].id, aws_subnet.legendary_private_subnets[*].id)
    endpoint_private_access = true
    endpoint_public_access  = true
    public_access_cidrs     = ["0.0.0.0/0"]
    security_group_ids      = [aws_security_group.legendary_eks_cluster_sg.id]
  }
  
  encryption_config {
    provider {
      key_arn = aws_kms_key.legendary_kms_key.arn
    }
    resources = ["secrets"]
  }
  
  enabled_cluster_log_types = ["api", "audit", "authenticator", "controllerManager", "scheduler"]
  
  depends_on = [
    aws_iam_role_policy_attachment.legendary_eks_cluster_policy,
    aws_cloudwatch_log_group.legendary_eks_logs
  ]
  
  tags = merge(local.common_tags, {
    Name = var.cluster_name
    Type = "legendary-eks-cluster"
  })
}

# CloudWatch Log Group for EKS
resource "aws_cloudwatch_log_group" "legendary_eks_logs" {
  name              = "/aws/eks/${var.cluster_name}/cluster"
  retention_in_days = 7
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-eks-logs"
    Type = "legendary-log-group"
  })
}

# KMS Key for encryption
resource "aws_kms_key" "legendary_kms_key" {
  description             = "N3EXTPATH Legendary KMS Key for EKS Encryption"
  deletion_window_in_days = 7
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-kms-key"
    Type = "legendary-encryption"
  })
}

resource "aws_kms_alias" "legendary_kms_alias" {
  name          = "alias/n3extpath-legendary-key"
  target_key_id = aws_kms_key.legendary_kms_key.key_id
}

# EKS Node Groups - Legendary Compute Power
resource "aws_eks_node_group" "legendary_node_group_general" {
  cluster_name    = aws_eks_cluster.legendary_cluster.name
  node_group_name = "legendary-general-nodes"
  node_role_arn   = aws_iam_role.legendary_eks_node_role.arn
  subnet_ids      = aws_subnet.legendary_private_subnets[*].id
  
  capacity_type  = "ON_DEMAND"
  instance_types = ["t3.large", "t3.xlarge"]
  
  scaling_config {
    desired_size = 3
    max_size     = 10
    min_size     = 3
  }
  
  update_config {
    max_unavailable_percentage = 25
  }
  
  ami_type       = "AL2_x86_64"
  disk_size      = 50
  
  remote_access {
    ec2_ssh_key = aws_key_pair.legendary_key_pair.key_name
    source_security_group_ids = [aws_security_group.legendary_eks_node_sg.id]
  }
  
  labels = {
    role = "general"
    environment = var.environment
    legendary-status = "maximum"
    built-by = "rickroll187"
  }
  
  depends_on = [
    aws_iam_role_policy_attachment.legendary_eks_worker_node_policy,
    aws_iam_role_policy_attachment.legendary_eks_cni_policy,
    aws_iam_role_policy_attachment.legendary_eks_container_registry_policy
  ]
  
  tags = merge(local.common_tags, {
    Name = "legendary-general-node-group"
    Type = "legendary-node-group"
  })
}

# High-Performance Node Group for RICKROLL187's workloads
resource "aws_eks_node_group" "legendary_node_group_performance" {
  cluster_name    = aws_eks_cluster.legendary_cluster.name
  node_group_name = "legendary-performance-nodes"
  node_role_arn   = aws_iam_role.legendary_eks_node_role.arn
  subnet_ids      = aws_subnet.legendary_private_subnets[*].id
  
  capacity_type  = "ON_DEMAND"
  instance_types = ["c5.2xlarge", "c5.4xlarge"]
  
  scaling_config {
    desired_size = 2
    max_size     = 5
    min_size     = 2
  }
  
  update_config {
    max_unavailable_percentage = 25
  }
  
  ami_type       = "AL2_x86_64"
  disk_size      = 100
  
  remote_access {
    ec2_ssh_key = aws_key_pair.legendary_key_pair.key_name
    source_security_group_ids = [aws_security_group.legendary_eks_node_sg.id]
  }
  
  labels = {
    role = "performance"
    environment = var.environment
    legendary-status = "maximum"
    built-by = "rickroll187"
    swiss-precision = "enabled"
  }
  
  taints = [
    {
      key    = "legendary-performance"
      value  = "true"
      effect = "NO_SCHEDULE"
    }
  ]
  
  depends_on = [
    aws_iam_role_policy_attachment.legendary_eks_worker_node_policy,
    aws_iam_role_policy_attachment.legendary_eks_cni_policy,
    aws_iam_role_policy_attachment.legendary_eks_container_registry_policy
  ]
  
  tags = merge(local.common_tags, {
    Name = "legendary-performance-node-group"
    Type = "legendary-high-performance-nodes"
  })
}

# Key Pair for EC2 Access
resource "aws_key_pair" "legendary_key_pair" {
  key_name   = "n3extpath-legendary-key"
  public_key = file("~/.ssh/n3extpath_legendary.pub") # You'll need to generate this
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-key-pair"
    Type = "legendary-key-pair"
  })
}

# RDS Subnet Group
resource "aws_db_subnet_group" "legendary_db_subnet_group" {
  name       = "n3extpath-legendary-db-subnet-group"
  subnet_ids = aws_subnet.legendary_database_subnets[*].id
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-db-subnet-group"
    Type = "legendary-db-subnet-group"
  })
}

# RDS PostgreSQL Instance - Legendary Database
resource "aws_db_instance" "legendary_postgres" {
  identifier     = "n3extpath-legendary-postgres"
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.r6g.xlarge"
  
  allocated_storage     = 100
  max_allocated_storage = 1000
  storage_type          = "gp3"
  storage_encrypted     = true
  kms_key_id           = aws_kms_key.legendary_kms_key.arn
  
  db_name  = "n3extpath_hr"
  username = "n3extpath_admin"
  password = random_password.legendary_db_password.result
  
  vpc_security_group_ids = [aws_security_group.legendary_rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.legendary_db_subnet_group.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "Mon:04:00-Mon:05:00"
  
  skip_final_snapshot = false
  final_snapshot_identifier = "n3extpath-legendary-postgres-final-snapshot"
  
  performance_insights_enabled = true
  monitoring_interval          = 60
  monitoring_role_arn         = aws_iam_role.legendary_rds_monitoring_role.arn
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-postgres"
    Type = "legendary-database"
  })
}

# Random password for database
resource "random_password" "legendary_db_password" {
  length  = 32
  special = true
}

# RDS Monitoring Role
resource "aws_iam_role" "legendary_rds_monitoring_role" {
  name = "n3extpath-legendary-rds-monitoring-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "monitoring.rds.amazonaws.com"
        }
      }
    ]
  })
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-rds-monitoring-role"
    Type = "legendary-iam-role"
  })
}

resource "aws_iam_role_policy_attachment" "legendary_rds_monitoring_policy" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
  role       = aws_iam_role.legendary_rds_monitoring_role.name
}

# ElastiCache Subnet Group
resource "aws_elasticache_subnet_group" "legendary_cache_subnet_group" {
  name       = "n3extpath-legendary-cache-subnet-group"
  subnet_ids = aws_subnet.legendary_private_subnets[*].id
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-cache-subnet-group"
    Type = "legendary-cache-subnet-group"
  })
}

# ElastiCache Redis Cluster - Legendary Caching
resource "aws_elasticache_replication_group" "legendary_redis" {
  replication_group_id       = "n3extpath-legendary-redis"
  description                = "N3EXTPATH Legendary Redis Cluster"
  
  port                      = 6379
  parameter_group_name      = "default.redis7"
  node_type                 = "cache.r6g.large"
  num_cache_clusters        = 3
  
  engine_version            = "7.0"
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  auth_token                = random_password.legendary_redis_password.result
  
  subnet_group_name         = aws_elasticache_subnet_group.legendary_cache_subnet_group.name
  security_group_ids        = [aws_security_group.legendary_elasticache_sg.id]
  
  maintenance_window        = "sun:03:00-sun:04:00"
  snapshot_retention_limit  = 5
  snapshot_window          = "02:00-03:00"
  
  automatic_failover_enabled = true
  multi_az_enabled          = true
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-redis"
    Type = "legendary-cache"
  })
}

# Random password for Redis
resource "random_password" "legendary_redis_password" {
  length  = 32
  special = false # Redis auth tokens can't have special characters
}

# S3 Bucket for legendary file storage
resource "aws_s3_bucket" "legendary_storage" {
  bucket = "n3extpath-legendary-storage-${random_id.bucket_suffix.hex}"
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-storage"
    Type = "legendary-storage"
  })
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket_versioning" "legendary_storage_versioning" {
  bucket = aws_s3_bucket.legendary_storage.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_encryption" "legendary_storage_encryption" {
  bucket = aws_s3_bucket.legendary_storage.id
  
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        kms_master_key_id = aws_kms_key.legendary_kms_key.arn
        sse_algorithm     = "aws:kms"
      }
    }
  }
}

resource "aws_s3_bucket_public_access_block" "legendary_storage_pab" {
  bucket = aws_s3_bucket.legendary_storage.id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# CloudFront Distribution for legendary global delivery
resource "aws_cloudfront_distribution" "legendary_cdn" {
  origin {
    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
    
    domain_name = "n3extpath.com" # This would be your ALB DNS name
    origin_id   = "n3extpath-legendary-origin"
    
    custom_header {
      name  = "X-Legendary-Status"
      value = "maximum"
    }
    
    custom_header {
      name  = "X-Built-By"
      value = "rickroll187"
    }
  }
  
  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"
  
  aliases = ["n3extpath.com", "www.n3extpath.com"]
  
  default_cache_behavior {
    allowed_methods        = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "n3extpath-legendary-origin"
    compress               = true
    viewer_protocol_policy = "redirect-to-https"
    
    forwarded_values {
      query_string = true
      headers      = ["Host", "Authorization", "X-Legendary-*"]
      
      cookies {
        forward = "all"
      }
    }
    
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }
  
  # Cache behavior for API
  ordered_cache_behavior {
    path_pattern           = "/api/*"
    allowed_methods        = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods         = ["GET", "HEAD", "OPTIONS"]
    target_origin_id       = "n3extpath-legendary-origin"
    compress               = true
    viewer_protocol_policy = "https-only"
    
    forwarded_values {
      query_string = true
      headers      = ["*"]
      
      cookies {
        forward = "all"
      }
    }
    
    min_ttl     = 0
    default_ttl = 0
    max_ttl     = 0
  }
  
  price_class = "PriceClass_All"
  
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
  
  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.legendary_cert.arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-cdn"
    Type = "legendary-cdn"
  })
}

# ACM Certificate for HTTPS
resource "aws_acm_certificate" "legendary_cert" {
  domain_name               = "n3extpath.com"
  subject_alternative_names = ["*.n3extpath.com"]
  validation_method         = "DNS"
  
  lifecycle {
    create_before_destroy = true
  }
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-cert"
    Type = "legendary-certificate"
  })
}

# Route53 Hosted Zone
resource "aws_route53_zone" "legendary_zone" {
  name = "n3extpath.com"
  
  tags = merge(local.common_tags, {
    Name = "n3extpath-legendary-zone"
    Type = "legendary-dns"
  })
}

# Route53 Records
resource "aws_route53_record" "legendary_a_record" {
  zone_id = aws_route53_zone.legendary_zone.zone_id
  name    = "n3extpath.com"
  type    = "A"
  
  alias {
    name                   = aws_cloudfront_distribution.legendary_cdn.domain_name
    zone_id                = aws_cloudfront_distribution.legendary_cdn.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "legendary_www_record" {
  zone_id = aws_route53_zone.legendary_zone.zone_id
  name    = "www.n3extpath.com"
  type    = "A"
  
  alias {
    name                   = aws_cloudfront_distribution.legendary_cdn.domain_name
    zone_id                = aws_cloudfront_distribution.legendary_cdn.hosted_zone_id
    evaluate_target_health = false
  }
}

# Outputs for legendary reference
output "legendary_cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = aws_eks_cluster.legendary_cluster.endpoint
  sensitive   = true
}

output "legendary_cluster_security_group_id" {
  description = "Security group ids attached to the cluster control plane"
  value       = aws_eks_cluster.legendary_cluster.vpc_config[0].cluster_security_group_id
}

output "legendary_postgres_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.legendary_postgres.endpoint
  sensitive   = true
}

output "legendary_redis_endpoint" {
  description = "ElastiCache Redis endpoint"
  value       = aws_elasticache_replication_group.legendary_redis.primary_endpoint_address
  sensitive   = true
}

output "legendary_s3_bucket" {
  description = "S3 bucket name"
  value       = aws_s3_bucket.legendary_storage.bucket
}

output "legendary_cloudfront_distribution_id" {
  description = "CloudFront Distribution ID"
  value       = aws_cloudfront_distribution.legendary_cdn.id
}

output "legendary_route53_zone_id" {
  description = "Route53 hosted zone ID"
  value       = aws_route53_zone.legendary_zone.zone_id
}

output "legendary_status_message" {
  description = "🎸 Legendary infrastructure deployment status 🎸"
  value       = "🎸 LEGENDARY INFRASTRUCTURE DEPLOYED WITH SWISS PRECISION BY RICKROLL187! WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸"
}
