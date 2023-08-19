# Guia para Criar um Comando Personalizado para um Script Python

Neste guia, vamos mostrar como criar um comando personalizado no terminal para executar o seu script Python "pdf-booklet.py" de qualquer diretório.

## Passo 1: Crie um Diretório para seus Scripts (Opcional)

Se você ainda não tem um diretório para armazenar seus scripts personalizados, crie um. Neste exemplo, usaremos "meus-scripts".

```bash
mkdir ~/meus-scripts
```
## Passo 2: Mova o Script Python
Mova o arquivo "pdf-booklet.py" para o diretório "meus-scripts":

```bash
mv pdf-booklet.py ~/meus-scripts/
```

## Passo 3: Crie um Arquivo de Script de Shell (Wrapper)
Crie um arquivo de script de shell que funcionará como um wrapper para chamar o seu script Python. Vamos chamá-lo de "pdf-booklet" (sem a extensão ".py"). Use um editor de texto para criar o arquivo:

```bash
nano ~/meus-scripts/pdf-booklet
```

Dentro do arquivo, adicione o seguinte conteúdo:

```bash
#!/bin/bash
python3 ~/meus-scripts/pdf-booklet.py "$@"
```

Salve o arquivo e saia do editor.

## Passo 4: Dê Permissão de Execução ao Arquivo de Script
Dê permissão de execução ao seu arquivo de script para que ele possa ser executado:

```bash
chmod +x ~/meus-scripts/pdf-booklet
```

## Passo 5: Adicione o Diretório "meus-scripts" ao PATH
Para permitir que o sistema encontre seu comando "pdf-booklet" de qualquer diretório, adicione o diretório "meus-scripts" ao seu PATH. Edite o arquivo ~/.bashrc ou ~/.bash_profile com um editor de texto:

```bash
nano ~/.bashrc
```

No final do arquivo, adicione a seguinte linha (substitua "/caminho/para" pelo caminho real para sua pasta de scripts):

```bash
export PATH="$PATH:/caminho/para/meus-scripts"
```

Salve o arquivo e saia do editor.

## Passo 6: Atualize o Ambiente do Terminal
Para aplicar as alterações, atualize o ambiente do terminal:

```bash
source ~/.bashrc
```

Agora, você deve ser capaz de executar o seu comando "pdf-booklet" a partir de qualquer diretório no terminal, conforme mostrado abaixo:

```bash
pdf-booklet arquivo.pdf
```

Certifique-se de substituir "/caminho/para" pelo caminho real para a pasta "meus-scripts" em que você armazenou seu script "pdf-booklet.py". Com esses passos, você criou um comando personalizado que pode ser chamado de qualquer lugar no terminal.
