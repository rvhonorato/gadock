#!/bin/bash
export GDOCK_PATH=$1

cd "$GDOCK_PATH" || exit
mkdir "$GDOCK_PATH"/src
cd "$GDOCK_PATH"/src || exit

# dcomplex
wget http://servers.sparks-lab.org/downloads/dcomplex2.tar.gz
tar zxfv dcomplex2.tar.gz
rm dcomplex2.tar.gz
cd "$GDOCK_PATH"/src/dcomplex_single_file || exit
sed -i "s|5400|54000|g" dcomplex.c
sed -i "s|charge_inp.dat|$GDOCK_PATH/src/dcomplex_single_file/charge_inp.dat|g" dcomplex.c
sed -i "s|\"fort.21_alla\"|\"$GDOCK_PATH/src/dcomplex_single_file/fort.21_alla\"|g" dcomplex.c
g++ -o dcomplex dcomplex.c
cd "$GDOCK_PATH"/src || exit

# fcc
git clone https://github.com/haddocking/fcc.git
cd fcc || exit
git checkout python3
cd src || exit
make
cd "$GDOCK_PATH"/src || exit

# pdb-tools
git clone https://github.com/haddocking/pdb-tools
cd "$GDOCK_PATH"/src || exit

# haddock-tools
git clone https://github.com/haddocking/haddock-tools
g++ -O2 -o contact-chainID contact-chainID.cpp
cd "$GDOCK_PATH"/src || exit

# profit
wget http://www.bioinf.org.uk/software/profit/235216/profit.tar.gz
tar zxvf profit.tar.gz
rm profit.tar.gz
cd ProFit_V3.3/src || exit
make
cd "$GDOCK_PATH"/src || exit

# edit paths
cd "$GDOCK_PATH" || exit
sed -i s"|/Users/rodrigo/repos/gdock|$GDOCK_PATH|g" etc/gdock.ini