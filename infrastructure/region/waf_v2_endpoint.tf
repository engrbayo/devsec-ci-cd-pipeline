module "wafv2" {
  source = "../../modules/wafv2"

  web_acl_name              = "reinevent-takeaway-wafv2"
  scope                     = "REGIONAL"
  association_resource_arns = []
  allow_default_action      = true
  create_alb_association    = false
  application               = "load-balancer"
  environment               = "DEV"
  functionality             = "WAFv2"
  enabled                   = true
  name_prefix               = "reinvent"
  description               = "WAFv2 to protect internet facing endpoints"

  visibility_config = {
    metric_name                = "reinvent-takeaway"
    cloudwatch_metrics_enabled = true
    sampled_requests_enabled   = true
  }

  rules = [
    {
      name     = "reinevent-takeaway"
      priority = "1"

      action = "block"

      visibility_config = {
        cloudwatch_metrics_enabled = true
        metric_name                = "reinvent-takeaway"
        sampled_requests_enabled   = true
      }

      byte_match_statement = {
        field_to_match = {
          uri_path = "{}"
        }
        positional_constraint = "STARTS_WITH"
        search_string         = "/portal"
        priority              = 0
        type                  = "NONE"
      }
    }
  ]
}
