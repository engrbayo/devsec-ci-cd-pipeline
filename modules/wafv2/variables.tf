variable "enabled" {
  description = "Indicates if module is enabled. Set to false to prevent the module from creating resources"
  type        = bool
  default     = true
}

variable "web_acl_name" {
  description = "The name of the Web ACL to be created"
  type        = string
  default     = null
}

variable "allow_default_action" {
  description = "Set to `true` for WAF to allow requests by default. Set to `false` for WAF to block requests by default"
  type        = bool
  default     = true
}

variable "scope" {
  description = "Specifies whether this is for an AWS Cloudfront distribution or for a regional application"
  type        = string
}

variable "rules" {
  description = "list of WAF rules"
  type        = any
  default     = []
}

variable "name_prefix" {
  description = "Friendly metric name prefix"
  type        = string
}

variable "visibility_config" {
  description = "Visibility config for WAFv2 web acl. https://www.terraform.io/docs/providers/aws/r/wafv2_web_acl.html#visibility-configuration"
  type        = map(string)
  default     = {}
}

variable "association_resource_arns" {
  description = "A list of ARNs of the resources (Application Load Balance , Amazon API Gateway) that should be associated with the web ACL"
  type        = list(string)
  default     = []
}

variable "create_alb_association" {
  description = "Whether to create alb association with WAF web ACL"
  type        = bool
  default     = true
}

variable "tags" {
  description = "A map of tags (key-value pairs) passed to resources"
  type        = map(string)
  default     = {}
}

variable "description" {
  type        = string
  description = "A friendly description of the WebACL"
}

variable "create_logging" {
  type        = bool
  description = "Whether to create logging configuration in order start logging from a WAFv2 Web ACL to Amazon Kinesis Data Firehose."
  default     = false
}

variable "log_destination_arn" {
  type        = list(string)
  description = "The Amazon Kinesis Data Firehose Amazon Resource Name (ARNs) that you want to associate with the web ACL. Currently, only 1 ARN is supported."
  default     = []
}

variable "logging_filter" {
  type = object({
    default_behavior = string
    filter = list(object({
      behavior = string
      condition = list(object({
        action_condition     = optional(map(string))
        label_name_condition = optional(map(string))
      }))
      requirement = string
    }))
  })
  description = "Filtering that specifies which web requests are kept in the logs and which are dropped."
  default     = null
}

variable "redacted_fields" {
  type = object({
    single_header = optional(map(string))
    method        = optional(string)
    query_string  = optional(string)
    uri_path      = optional(string)
  })

  description = "The parts of the request that you want to keep out of the logs."
  default     = null
}

variable "application" {
  type = string
}

variable "environment" {
  type = string
}

variable "functionality" {
  type = string
}
