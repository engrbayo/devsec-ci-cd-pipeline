terraform {
  source = "../../../..//infrastructure/region"
}


include {
  path = find_in_parent_folders()
}