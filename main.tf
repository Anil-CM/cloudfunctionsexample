provider "ibm"{}

resource "ibm_function_package" "package" {
  name = var.packageName
  namespace = var.namespace
}

resource "ibm_function_action" "action" {
  name = "${ibm_function_package.package.name}/${var.actionName}"
  namespace = var.namespace  

  exec {
    image = "anilcm/test:v1.0"
    kind = "blackbox"
    code = file("test_schematics_operations.py")
  }
  user_defined_annotations = <<EOF
        [
    {
        "key": "web-export",
        "value": true},
    {
        "key":"raw-http",
        "value":false
    },
    {
        "key":"final",
        "value":true
    },
    {
        "key":"exec",
        "value":"blackbox"
    }
]
EOF
 user_defined_parameters = <<EOF
        [
    {
        "key": "apikey",
        "value":"${var.api_key}"
    },
    {
        "key":"workspace_id",
        "value":"${var.workspace_id}"
    },
    {
        "key": "count",
        "value": 3
    }
]
EOF
}