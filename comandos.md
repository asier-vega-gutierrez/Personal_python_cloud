cd Personal_python_cloud/src/db_comparer/local/
/home/asier/miniconda3/envs/cloud/bin/python /home/asier/project/Personal_python_cloud/src/db_comparer/local/src/main.py

cd Personal_python_cloud/src/sync_client/
/home/asier/miniconda3/envs/cloud/bin/python /home/asier/project/Personal_python_cloud/src/sync_client/src/main.py

cd Personal_python_cloud/IaC/Terraform/
terraform apply -auto-approve
terraform apply -auto-approve -target=module.container_generator -var config_container_name=asier-container