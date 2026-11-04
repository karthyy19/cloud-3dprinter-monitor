# The board's device certificate (created with the AWS CLI, see the cli_steps output).
# Not a secret: the private key never leaves the board. Without this, every apply detaches it.
certificate_arn = "arn:aws:iot:eu-west-1:045774533738:cert/b7eae4c13348d4ac06ef68b2517c1799a693079eb80d4a17243b3ab1a37632c9"
