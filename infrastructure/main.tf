# S3 Bucket
resource "aws_s3_bucket" "staging_bucket" {
  bucket = "${var.bucket_name}"
  acl    = "public-read"

  tags = {
    Name    = "${var.project}-${var.group_name}"
    project = var.project
  }
}

# IAM Role to let Snowflake access to the S3 bucket
resource "aws_iam_role" "snowflake_role" {
  name = "${var.snowflake_access_role}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:GetObjectVersion",
          "s3:DeleteObject",
          "s3:DeleteObjectVersion"
        ],
        Resource: "arn:aws:s3:::${var.bucket_name}/staging/*"
      },
      {
        Effect: "Allow",
        Action: [
            "s3:ListBucket",
            "s3:GetBucketLocation"
        ],
        Resource: "arn:aws:s3:::${var.bucket_name}",
        Condition: {
            StringLike: {
                "s3:prefix": [
                    "staging/*"
                ]
            }
        }
    }    
    ]
  })

  tags = {
    Name    = "${var.project}-${var.group_name}"
    project = var.project
  }
}
