terraform {
  source = "../../../..//infrastructure/region/waf"
}


include {
  path = find_in_parent_folders()
}