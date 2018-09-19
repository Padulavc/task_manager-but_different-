#Projeto de Bloco

Projeto de bloco do período de python/redes de 2018 sob inspeção do professor Cassius Figueiredo

##Configuração

#####Instalação do ambiente virtual
caso não tenha o virutalenv instalado, pode adquiri-lo com ```$pip install virtualenv```.
Após a instalação, execute dentro da pasta principal do projeto:
``` 
$virtualenv venv
```
Para ativá-lo, execute:
```
$source venv/bin/activate
```
Agora, com o ambiente virtual antivado, installe as bibliotecas com:
```
$pip install -r requirements.txt
```


##Execução
Para a execução do projeto, você poderá optar por opções:
* Makefile
* Run.sh

#####Opção  _Makefile_

execute apenas ```$make```

#####Opção _run.sh_
 Talavez o arquivo peça permissão de execução.
 Neste caso, execute
 ```
 $chmod +X run.sh | ./run.sh
 ```
 
 se seu arquivo já tiver permissão de execução, execute apenas 
```$./run.hs```

####Adendo

o código do space invaders percence à  [Lee Robinson]( https://github.com/leerob/Space_Invaders)