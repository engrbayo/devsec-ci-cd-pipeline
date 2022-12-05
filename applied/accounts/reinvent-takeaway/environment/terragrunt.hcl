terraform {
  source = "../../../..//modules/tf-code"
}


include {
  path = find_in_parent_folders()
}