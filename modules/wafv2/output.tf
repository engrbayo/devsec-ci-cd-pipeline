output "web_acl_name" {
  description = "The name of the WAFv2 WebACL."
  value       = aws_wafv2_web_acl.waf_web_acl.*.name
}

output "web_acl_arn" {
  description = "The ARN of the WAFv2 WebACL."
  value       = aws_wafv2_web_acl.waf_web_acl.*.arn
}

output "web_acl_id" {
  description = "The ID of the WAFv2 WebACL."
  value       = aws_wafv2_web_acl.waf_web_acl.*.id
}
