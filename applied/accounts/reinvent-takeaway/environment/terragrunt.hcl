terraform {
  source = "../../../..//modules/wafv2"
}


include {
  path = find_in_parent_folders()
}