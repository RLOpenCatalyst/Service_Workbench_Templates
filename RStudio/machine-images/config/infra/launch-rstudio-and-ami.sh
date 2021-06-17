packer build -var-file=configuration.json packer-ec2-rstudio-workspace.json 
pip install boto3
pip install PyYAML
python create-rstudio.py