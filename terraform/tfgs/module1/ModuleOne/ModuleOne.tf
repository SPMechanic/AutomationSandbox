##################################################################################
# VARIABLES
##################################################################################

variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "private_key_path" {}

variable "key_name" {
  default = "architect"
}

##################################################################################
# PROVIDERS
##################################################################################

provider "aws" {
  access_key = "${var.aws_access_key}"
  secret_key = "${var.aws_secret_key}"
  region     = "ap-southeast-1"
}

##################################################################################
# RESOURCES
##################################################################################
# default-image (Amazon Linux AMI 2018.03.0 (HVM), SSD Volume Type - ami-de90a5a2)
# community-image (amzn-ami-hvm-2018.03.0.20180508-x86_64-gp2 - ami-de90a5a2)
resource "aws_instance" "nginx" {
  ami           = "ami-de90a5a2"
  instance_type = "t2.micro"
  key_name      = "${var.key_name}"

  connection {
    user        = "ec2-user"
    private_key = "${file(var.private_key_path)}"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo yum install nginx -y",
      "sudo service nginx start",
    ]
  }
}

##################################################################################
# OUTPUT
##################################################################################

output "aws_instance_public_dns" {
  value = "${aws_instance.nginx.public_dns}"
}
