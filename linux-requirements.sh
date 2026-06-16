echo
echo "Oi, aqui fala o professor Alexandre pelo Linux"
echo "Nao se sinta sozinho(a), eu estou no computador com voce"
echo
echo
echo "vou CRIAR o ambiente virtual na pasta de nivel anterior"
python3 -m venv ../venv &&
echo "PRONTO!"
echo
echo
echo "agora vou ATIVAR o ambiente virtual"
source ../venv/bin/activate &&
echo "PRONTO!"
echo
echo
echo "finalmente, eu vou INSTALAR a biblioteca pdf2image"
echo
pip3 install pdf2image &&
echo
echo "PRONTO!"
echo
echo "agora vc pode codar :) boa sorte"
echo
echo
echo
echo "lembre-se de dar o git config --list para conferir se vc esta realmente no seu repositorio"
echo "e conferir o user.email e user.name"
echo
echo
echo