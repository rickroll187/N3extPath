# File: terraform/main.tf
# N3EXTPATH HR Platform - Legendary Terraform Infrastructure
# Built: 2025-08-05 16:33:22 UTC by RICKROLL187
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
      version = "~> 2.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.0"
    }
  }
  
  backend "s3" {
    bucket = "n3extpath-terraform-state"
    key    = "legendary/terraform.tfstate"
    region = "us-west-2"
    
    dynamodb_table = "n3extpath-terraform-locks"
    encrypt        = true
    
    # Built by RICKROLL187 with Swiss precision!
  }
}

# Local values for legendary configuration
locals {
  project_name = "n3extpath-hr-platform"
  environment  = "production"
  region      = "us-west-2"
  
  # Legendary metadata
  legendary_tags = {
    Project       = "N3EXTPATH HR Platform"
    Environment   = "production"
    BuiltBy       = "RICKROLL187"
    LegendaryMode = "enabled"
    SwissPrecision = "true"
    CodeBroEnergy = "maximum"
    CreatedAt     = "2025-08-05T16:33:22Z"
  }
  
  # Availability zones for legendary high availability
  availability_zones = ["us-west-2a", "us-west-2b", "us-west-2c"]
}

# AWS Provider configuration
provider "aws" {
  region = local.region
  
  default_tags {
    tags = local.legendary_tags
  }
}

# VPC for legendary networking
resource "aws_vpc" "legendary_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = merge(local.legendary_tags, {
    Name = "${local.project_name}-vpc"
    Type = "LegendaryVPC"
  })
}

# Internet Gateway for legendary connectivity
resource "aws_internet_gateway" "legendary_igw" {
  vpc_id = aws_vpc.legendary_vpc.id
  
  tags = merge(local.legendary_tags, {
    Name = "${local.project_name}-igw"
  })
}

# Public subnets for legendary load balancers
resource "aws_subnet" "legendary_public_subnets" {
  count = length(local.availability_zones)
  
  vpc_id                  = aws_vpc.legendary_vpc.id
  cidr_block              = "10.0.${count.index + 1}.0/24"
  availability_zone       = local.availability_zones[count.index]
  map_public_ip_on_launch = true
  
  tags = merge(local.legendary_tags, {
    Name = "${local.project_name}-public-subnet-${count.index + 1}"
    Type = "Public"
    kubernetes.io/role/elb = "1"
  })
}

# Private subnets for legendary workloads
resource "aws_subnet" "legendary_private_subnets" {
  count = length(local.availability_zones)
  
  vpc_id            = aws_vpc.legendary_vpc.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = local.availability_zones[count.index]
  
  tags = merge(local.legendary_tags, {
    Name = "${local.project_name}-private-subnet-${count.index + 1}"
    Type = "Private"
    kubernetes.io/role/internal-elb = "1"
  })
}

# NAT Gateways for legendary outbound connectivity
resource "aws_eip" "legendary_nat_eips" {
  count = length(local.availability_zones)
  
  domain = "vpc"
  
  tags = merge(local.legendary_tags, {
    Name = "${local.project_name}-nat-eip-${count.index + 1}"
  })
}

resource "aws_nat_gateway" "legendary_nat_gateways" {
  count = length(local.availability_zones)
  
  allocation_id = aws_eip.legendary_nat_eips[count.index].id
  subnet_id     = aws_subnet.legendary_public_subnets[count.index].id
  
  tags = merge(local.legendary_tags, {
    Name = "${local.project_name}-nat-gateway-${count.index + 1}"
  })
  
  depends_on = [aws_internet_gateway.legendary_igw]
}

# Route tables for legendary routing
resource "aws_route_table" "legendary_public_rt" {
  vpc_id = aws_vpc.legendary_vpc.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.legendary_igw.id
  }
  
  tags = merge(local.legendary_tags, {
    Name = "${local.project_name}-public-rt"
    Type = "Public"
  })
}

resource "aws_route_table" "legendary_private_rts" {
  count = length(local.availability_zones)
  
  vpc_id = aws_vpc.legendary_vpc.id
  
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.legendary_nat_gateways[count.index].id
  }
  
  tags = merge(local.legendary_tags, {
    Name = "${local.project_name}-private-rt-${count.index + 1}"
    Type = "Private"
  })
}

# Route table associations
resource "aws_route_table_association" "legendary_public_rta" {
  count = length(aws_subnet.legendary_public_subnets)
  
  subnet_id      = aws_subnet.legendary_public_subnets[count.index].id
  route_table_id = aws_route_table.legendary_public_rt.id
}

resource "aws_route_table_association" "legendary_private_rta" {
  count = length(aws_subnet.legendary_private_subnets)
  
  subnet_id      = aws_subnet.legendary_private_subnets[count.index].id
  route_table_id = aws_route_table.legendary_private_rts[count.index].id
}

# Security groups for legendary security
resource "aws_security_group" "legendary_eks_cluster_sg" {
  name        = "${local.project_name}-eks-cluster-sg"
  description = "Security group for legendary EKS cluster"
  vpc_id      = aws_vpc.legendary_vpc.id
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "All outbound traffic"
  }
  
  tags = merge(local.legendary_tags, {
    Name = "${local.project_name}-eks-cluster-sg"
    Type = "LegendaryClusterSecurity"
  })
}

resource "aws_security_group" "legendary_eks_nodes_sg" {
  name        = "${local.project_name}-eks-nodes-sg"
  description = "Security group for legendary EKS worker nodes"
  vpc_id      = aws_vpc.legendary_vpc.id
  
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.legendary_vpc.cidr_block]
    description = "All traffic within VPC"
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "All outbound traffic"
  }
  
  tags = merge(local.legendary_tags, {
    Name = "${local.project_name}-eks-nodes-sg"
    Type = "LegendaryNodeSecurity"
  })
}

# IAM role for legendary EKS cluster
resource "aws_iam_role" "legendary_eks_cluster_role" {
  name = "${local.project_name}-eks-cluster-role"
  
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
  
  tags = local.legendary_tags
}

resource "aws_iam_role_policy_attachment" "legendary_eks_cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.legendary_eks_cluster_role.name
}

# IAM role for legendary EKS node group
resource "aws_iam_role" "legendary_eks_node_role" {
  name = "${local.project_name}-eks-node-role"
  
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
  
  tags = local.legendary_tags
}

resource "aws_iam_role_policy_attachment" "legendary_eks_worker_node_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.legendary_eks_node_role.name
}

resource "aws_iam_role_policy_attachment" "legendary_eks_cni_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.legendary_eks_node_role.name
}

resource "aws_iam_role_policy_attachment" "legendary_ec2_container_registry_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.legendary_eks_node_role.name
}

# EKS Cluster for legendary container orchestration
resource "aws_eks_cluster" "legendary_eks_cluster" {
  name     = "${local.project_name}-cluster"
  role_arn = aws_iam_role.legendary_eks_cluster_role.arn
  version  = "1.28"
  
  vpc_config {
    subnet_ids              = concat(aws_subnet.legendary_public_subnets[*].id, aws_subnet.legendary_private_subnets[*].id)
    security_group_ids      = [aws_security_group.legendary_eks_cluster_sg.id]
    endpoint_private_access = true
    endpoint_public_access  = true
    public_access_cidrs     = ["0.0.0.0/0"]
  }
  
  enabled_cluster_log_types = ["api", "audit", "authenticator", "controllerManager", "scheduler"]
  
  encryption_config {
    provider {
      key_arn = aws_kms_key.legendary_eks_encryption_key.arn
    }
    resources = ["secrets"]
  }
  
  tags = merge(local.legendary_tags, {
    Name = "${local.project_name}-cluster"
    Type = "LegendaryEKSCluster"
  })
  
  depends_on = [
    aws_iam_role_policy_attachment.legendary_eks_cluster_policy,
    aws_cloudwatch_log_group.legendary_eks_log_group
  ]
}

# EKS Node Group for legendary worker nodes
resource "aws_eks_node_group" "legendary_node_group" {
  cluster_name    = aws_eks_cluster.legendary_eks_cluster.name
  node_group_name = "legendary-nodes"
  node_role_arn   = aws_iam_role.legendary_eks_node_role.arn
  subnet_ids      = aws_subnet.legendary_private_subnets[*].id
  
  instance_types = ["t3.large"]
  capacity_type  = "ON_DEMAND"
  
  scaling_config {
    desired_size = 3
    max_size     = 10
    min_size     = 2
  }
  
  update_config {
    max_unavailable = 1
  }
  
  ami_type       = "AL2_x86_64"
  disk_size      = 50
  
  tags = merge(local.legendary_tags, {
    Name = "${local.project_name}-node-group"
    Type = "LegendaryNodeGroup"
  })
  
  depends_on = [
    aws_iam_role_policy_attachment.legendary_eks_worker_node_policy,
    aws_iam_role_policy_attachment.legendary_eks_cni_policy,
    aws_iam_role_policy_attachment.legendary_ec2_container_registry_policy,
  ]
}

# KMS key for legendary encryption
resource "aws_kms_key" "legendary_eks_encryption_key" {
  description             = "KMS key for legendary EKS cluster encryption"
  deletion_window_in_days = 7
  
  tags = merge(local.legendary_tags, {
    Name = "${local.project_name}-eks-encryption-key"
  })
}

resource "aws_kms_alias" "legendary_eks_encryption_key_alias" {
  name          = "alias/${local.project_name}-eks-encryption"
  target_key_id = aws_kms_key.legendary_eks_encryption_key.key_id
}

# CloudWatch log group for legendary logging
resource "aws_cloudwatch_log_group" "legendary_eks_log_group" {
  name              = "/aws/eks/${local.project_name}-cluster/cluster"
  retention_in_days = 30
  
  tags = merge(local.legendary_tags, {
    Name = "${local.project_name}-eks-logs"
  })
}

# RDS Aurora for legendary database (optional)
resource "aws_rds_cluster" "legendary_aurora_cluster" {
  count = var.use_aurora ? 1 : 0
  
  cluster_identifier      = "${local.project_name}-aurora"
  engine                 = "aurora-postgresql"
  engine_version         = "14.9"
  database_name          = "n3extpath_hr"
  master_username        = "n3extpath_user"
  master_password        = var.db_password
  backup_retention_period = 7
  preferred_backup_window = "03:00-04:00"
  preferred_maintenance_window = "sun:04:00-sun:05:00"
  
  vpc_security_group_ids = [aws_security_group.legendary_rds_sg[0].id]
  db_subnet_group_name   = aws_db_subnet_group.legendary_db_subnet_group[0].name
  
  storage_encrypted = true
  kms_key_id       = aws_kms_key.legendary_rds_encryption_key[0].arn
  
  deletion_protection = true
  skip_final_snapshot = false
  final_snapshot_identifier = "${local.project_name}-aurora-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}"
  
  tags = merge(local.legendary_tags, {
    Name = "${local.project_name}-aurora-cluster"
    Type = "LegendaryDatabase"
  })
}

# Outputs for legendary reference
output "legendary_cluster_endpoint" {
  description = "Endpoint for legendary EKS cluster"
  value       = aws_eks_cluster.legendary_eks_cluster.endpoint
}

output "legendary_cluster_security_group_id" {
  description = "Security group ID attached to the legendary EKS cluster"
  value       = aws_eks_cluster.legendary_eks_cluster.vpc_config[0].cluster_security_group_id
}

output "legendary_cluster_iam_role_arn" {
  description = "IAM role ARN of the legendary EKS cluster"
  value       = aws_eks_cluster.legendary_eks_cluster.role_arn
}

output "legendary_cluster_certificate_authority_data" {
  description = "Base64 encoded certificate data required to communicate with the legendary cluster"
  value       = aws_eks_cluster.legendary_eks_cluster.certificate_authority[0].data
}

output "legendary_vpc_id" {
  description = "ID of the legendary VPC"
  value       = aws_vpc.legendary_vpc.id
}

output "legendary_message" {
  description = "Legendary message from RICKROLL187"
  value       = "🎸 LEGENDARY INFRASTRUCTURE DEPLOYED! WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸"
}
