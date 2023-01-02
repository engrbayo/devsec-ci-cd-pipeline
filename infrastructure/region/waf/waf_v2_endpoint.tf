module "wafv2" {
  source = "../../modules/wafv2"

  web_acl_name              = "reinvent-takeaway-wafv2"
  scope                     = "REGIONAL"
  association_resource_arns = ["arn:aws:elasticloadbalancing:us-east-1:721933253214:loadbalancer/app/oludare-nginx-test/239525d3d0e914d6"]
  allow_default_action      = true
  create_alb_association    = true
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
      name     = "reinevent-takeaway-block"
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
