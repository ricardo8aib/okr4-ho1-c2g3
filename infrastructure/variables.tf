variable "profile" {
  type        = string
  description = "AWS profile to run Terraform"
}

variable "region" {
  type        = string
  description = "Region to use for provisioning"
}

variable "project" {
  type        = string
  description = "Project tag for the resources"
}

variable "group_name" {
  type        = string
  description = "The name of the group"
}

variable "bucket_name" {
  type        = string
  description = "Name of the bucket"
}