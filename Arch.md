https://wiki.archlinux.org/title/Install_Arch_Linux_on_WSL

# Añadir usuario (añadir primero contraseña al root)
useradd -m -G wheel -s /bin/bash <user>
passwd <user>

# Cambia usuario por defecto
wsl --manage archlinux --set-default-user username

# Cambiar entre usuarios
su <user>

# Antes de intalar nada hay que hacer esto para intalar pqeutes basicos de pacman para conexiones
pacman -Syu

# Listar los paquetes intallados
pacman -Q

# Añadir un usuario a sudo (se deve dar sudo al grupo wheel primero)
sudo pacman -S sudo
sudo usermod -aG wheel <user>
sudo pascman -S nano
EDITOR=nano visudo  
Se descomenta la linea "%wheel ALL=(ALL:ALL) ALL"
CTRL+O ENTER CTRL+X

# Intalacion de miniconda
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
source ~/miniconda3/bin/activate




# Paquetes (https://aur.archlinux.org/packages)
sudo pacman -S --needed man-db
sudo pacman -S --needed base-devel
sudo pacman -S --needed git
sudo pacman -S --needed wget


# Paquetes de python
pip install watchdog
pip install PyYAML