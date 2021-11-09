#!/usr/bin/env bash

# Install prerequisite packages
sudo yum update -y
sudo yum install -y java-1.8.0-openjdk java-1.8.0-openjdk-devel-1.8.0.* curl wget git docker awscli unzip
sudo yum install -y gcc-7.3.* gcc-gfortran-7.3.* gcc-c++-7.3.* pcre-devel zlib-devel
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
sudo systemctl start docker
sudo usermod -a -G docker ec2-user

# Install Nextflow
cd /usr/bin/
sudo curl -s https://get.nextflow.io | sudo bash
sudo wget -qO- https://github.com/nextflow-io/nextflow/releases/download/v20.08.1-edge/nextflow-20.08.1-edge-all | sudo bash
sudo bash nextflow self-update
sudo chown -R ec2-user:ec2-user /usr/bin/nextflow 
sudo cp -prf nextflow /root/
sudo cd /root/
sudo cp -prf /.nextflow/ /root/

cd /usr/local/bin/
# Install H2 database(1.4.199)
sudo wget https://h2database.com/h2-2019-03-13.zip
sudo unzip h2-2019-03-13.zip

# Install Nextflow tower
sudo git clone https://github.com/seqeralabs/nf-tower.git
cd nf-tower/
# Checkout to current susleep 1mpported commit
sudo git checkout ea289521a915bcd2cd64cb2a1de66a08e2892938
# Copy custom files to tower folder
sudo mv "/tmp/nextflow/docker-compose.yml" "/usr/local/bin/nf-tower/"
sudo mv "/tmp/nextflow/application.yml" "/usr/local/bin/nf-tower/tower-backend/src/main/resources/"
sudo make build
sudo docker-compose up -d

# Wait for 1m for docker container to come up
sleep 1m

# Create new user in the H2 database
cd ..
sudo mv "/tmp/nextflow/create-user.sql" "/usr/local/bin/"
sudo mv "/tmp/nextflow/update-user.sql" "/usr/local/bin/"
AUTH_TOKEN=$(uuidgen)
ACCESS_TOKEN=$(uuidgen)
# Replace the generated tokens in the sql file
sudo sed -i "s/<<AUTH_TOKEN>>/${AUTH_TOKEN}/g" /usr/local/bin/create-user.sql
sudo sed -i "s/<<ACCESS_TOKEN>>/${ACCESS_TOKEN}/g" /usr/local/bin/create-user.sql
sudo java -cp /usr/local/bin/h2/bin/h2-*.jar org.h2.tools.RunScript -url "jdbc:h2:file:/usr/local/bin/nf-tower/.db/h2/tower" -driver "org.h2.Driver" -user "sa" -password "testpass" -script /usr/local/bin/create-user.sql -showResults

# Add the access token to nextflow config file
sudo bash -c "cat << EOF > /root/.nextflow/config                                                                                                                                                                                                                                                                                                                                                            
tower {
  accessToken = '${ACCESS_TOKEN}'
  endpoint = 'http://localhost:8000/api'
  enabled = true
}
EOF
"

#Generate self signed certificate
commonname=$(uname -n)
password=dummypassword
mkdir -p "/tmp/nextflow/ssl"
chmod 700 /tmp/nextflow/ssl
cd /tmp/nextflow/ssl
openssl genrsa -des3 -passout pass:$password -out cert.key 2048
#Remove passphrase from the key. Comment the line out to keep the passphrase
openssl rsa -in cert.key -passin pass:$password -out cert.key
openssl req -new -key cert.key -out cert.csr -passin pass:$password \
    -subj "/C=NA/ST=NA/L=NA/O=NA/OU=SWB/CN=$commonname/emailAddress=example.com"
openssl x509 -req -days 365 -in cert.csr -signkey cert.key -out cert.pem
cd /usr/local/bin/

# Install and configure nginx
sudo amazon-linux-extras enable nginx1
sudo yum install -y nginx-1.20.0
sudo openssl dhparam -out "/etc/nginx/dhparam.pem" 2048
sudo mv "/tmp/nextflow/ssl/cert.pem" "/etc/nginx/"
sudo mv "/tmp/nextflow/ssl/cert.key" "/etc/nginx/"
sudo mv "/tmp/nextflow/nginx.conf" "/etc/nginx/"
sudo chown -R ec2-user:ec2-user "/etc/nginx"
sudo chmod -R 600 "/etc/nginx"
#Install Nginx Fancy index module
sudo wget https://nginx.org/download/nginx-1.20.0.tar.gz
sudo gunzip -c nginx-1.20.0.tar.gz | sudo tar -xvf -
sudo git clone https://github.com/aperezdc/ngx-fancyindex.git ngx-fancyindex
cd nginx-1.20.0/
sudo ./configure --with-compat --add-dynamic-module=../ngx-fancyindex --with-http_addition_module --prefix=/usr/share/nginx
sudo make install
cd ..
#Copy Custom HTML and CSS file for fancy index
sudo mv "/tmp/nextflow/Nginx-Theme.zip" "/usr/local/bin/"
sudo unzip Nginx-Theme.zip && sudo mv Nginx-Theme /home/ec2-user/.nginxy
sudo systemctl enable nginx
sudo systemctl restart nginx

# Install script that sets the authentication token at boot
sudo mv "/tmp/nextflow/set-token" "/usr/local/bin/"
sudo chown root: "/usr/local/bin/set-token"
sudo chmod 775 "/usr/local/bin/set-token"
sudo crontab -l 2>/dev/null > "/tmp/crontab"
echo '@reboot /usr/local/bin/set-token 2>&1 >> /var/log/set-token.log' >> "/tmp/crontab"
sudo crontab "/tmp/crontab"

#Create Nextflow output directory
sudo mkdir -p /home/ec2-user/nextflow/outputs

# Wipe out all traces of provisioning files
sudo rm -rf "/tmp/nextflow"