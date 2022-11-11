# S3 Bucket
resource "aws_s3_bucket" "staging_bucket" {
  bucket = "${var.bucket_name}"

  tags = {
    Name    = "${var.project}-${var.group_name}"
    project = var.project
  }
}

# IAM Role to let Snowflake access to the S3 bucket
resource "aws_iam_role" "snowflake_role" {
  name = "${var.snowflake_access_role}"

  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "${var.aws_account_id}"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": "0000"
                }
            }
        }
    ]
}
EOF

  tags = {
    Name    = "${var.project}-${var.group_name}"
    project = var.project
  }
}


# IAM Policy to attach to the S3 Role
resource "aws_iam_policy" "snowflake_s3_access_policy" {
  name        = "okr4-snowflake-s3-access-policy"
  description = "Allows the ${aws_iam_role.snowflake_role.name} role access to S3"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket",
                "s3:GetBucketLocation",
                "s3:GetObjectVersion"
            ],
            "Resource": "*"
        }
    ]
}
EOF
  tags = {
    Name    = "${var.project}-${var.group_name}"
    project = var.project
  }
}

resource "aws_iam_role_policy_attachment" "attach-s3-policy-to-snowflake-role" {
  role       = aws_iam_role.snowflake_role.name
  policy_arn = aws_iam_policy.snowflake_s3_access_policy.arn
}

# Security group for the ASTRONOMER SERVER
resource "aws_security_group" "astronomer_security_group" {
  name        = "${var.project}-astronomer-sg"
  description = "Security group for ASTRONOMER EC2 instance"

  tags = {
    Name    = "${var.project}-astronomer-sg"
    project = var.project
  }

ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "for all outgoing traffics"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}



# AWS key pair for ASTRONOMER instance
resource "tls_private_key" "astronomer_private_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "aws_key_pair_astronomer" {
  key_name   = "${var.project}-astronomer"
  public_key = tls_private_key.astronomer_private_key.public_key_openssh

  provisioner "local-exec" {
    command = "echo '${tls_private_key.astronomer_private_key.private_key_pem}' > ./keys/astronomer-${var.project}.pem"
  }
}

# Astronomer EC2 Instance
resource "aws_instance" "astronomer_instance" {

  ami                    = "ami-052efd3df9dad4825"
  instance_type          = "t2.large"
  vpc_security_group_ids = [aws_security_group.astronomer_security_group.id]
  key_name               = aws_key_pair.aws_key_pair_astronomer.key_name
  user_data              = <<-EOF
    #!/bin/bash
    cd /home/ubuntu

    sudo apt update
    sudo snap install docker

    curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose

    sudo curl -sSL install.astronomer.io | sudo bash -s
    sudo mkdir okr4-astronomer
    cd okr4-astronomer/
    sudo astro dev init
    sudo astro dev start

  EOF

  tags = {
    Name    = "${var.project}-astronomer-instance"
    project = var.project
  }
}

# Security group for the AIRBYTE SERVER
resource "aws_security_group" "airbyte_security_group" {
  name        = "${var.project}-airbyte-sg"
  description = "Security group for AIRBYTE EC2 instance"

  tags = {
    Name    = "${var.project}-airbyte-sg"
    project = var.project
  }

ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "for all outgoing traffics"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


# AWS key pair for airbyte instance
resource "tls_private_key" "airbyte_private_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "aws_key_pair_airbyte" {
  key_name   = "${var.project}-airbyte"
  public_key = tls_private_key.airbyte_private_key.public_key_openssh

  provisioner "local-exec" {
    command = "echo '${tls_private_key.airbyte_private_key.private_key_pem}' > ./keys/airbyte-${var.project}.pem"
  }
}

# airbyte EC2 Instance
resource "aws_instance" "airbyte_instance" {

  ami                    = "ami-052efd3df9dad4825"
  instance_type          = "t2.large"
  vpc_security_group_ids = [aws_security_group.airbyte_security_group.id]
  key_name               = aws_key_pair.aws_key_pair_airbyte.key_name
  user_data              = <<-EOF
    #!/bin/bash
    cd /home/ubuntu

    sudo apt update
    sudo snap install docker

    curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose

    git clone https://github.com/airbytehq/airbyte.git
    cd airbyte
    sudo docker-compose up
  EOF

  tags = {
    Name    = "${var.project}-airbyte-instance"
    project = var.project
  }
}