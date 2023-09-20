# PlanworkBackup
Software desenvolvido em Python 3.11, especialmente criado para o backup dos bancos de dados utilizados pelo software ERP Evolution.

Possui interface simples e direta, log completo, manual detalhado e pode ser parametrizado via linha de comando, funcionalidade pensada na automação pelo Agendador de Tarefas do Windows.

Para próximas versões, pretendo adicionar a opção de integrá-lo ao OneDrive e/ou Google Drive para a sincronização do backup em nuvem.

Este software é o resultado do trabalho de alguém que saiu do zero em Python, fez muitos testes, errou muito e conseguiu lançar uma versão que funciona muito bem ao que se propõe. Ainda assim, foi desenvolvido por um iniciante em programação, e por essa razão aceito de bom grado colaborações e sugestões ao projeto.





<h1>Manual de instruções</h1>

<h2>Sobre o Software</h2><br>
O Planwork Backup é um software gratuito e de código aberto regido pela licença GPL versão 3. A integra dessa licença é exibida durante a instalação do software.

<br><h2>Instalação</h2>
IMPORTANTE: A instalação desse software deve ser realizada no mesmo computador onde está sendo executado o Microsoft SQL utilizado pelo Evolution, caso contrário ele não funcionará.<br><br>

Para instalar o software, basta executar seu instalador, cujo nome do arquivo tem o padrão “Planwork-Backup-X.X.X-installer.exe”, onde X.X.X é a versão do software.
Após a execução, a primeira tela exibida é a abaixo:

![image](https://user-images.githubusercontent.com/49456349/229897104-522ad337-da57-46e0-a038-5c58d854f904.png)

Nessa tela deve ser escolhido o método de instalação. “Instalar pra todos os usuários (recomendado)” necessita de permissões de administrador para que o processo de instalação possa seguir com sucesso.
Já a opção “Instalar só pra mim” usará as permissões do usuário logado no ato da instalação, que precisará ter permissões para gravar dados na pasta escolhida para instalar o software.

Escolhendo uma das opções acima, a tela seguinte é a que exibe a licença de uso.

![image](https://user-images.githubusercontent.com/49456349/229909256-f7c26d2d-e19e-41f8-a25f-b4e8c232e2dc.png)

Nessa tela, a única forma de seguir adiante é selecionando “Eu aceito o acordo”, o que habilita o botão “Avançar”.

IMPORTANTE: Não aceite o acordo e não siga com a instalação do software, exceto se estiver de acordo com a licença.

Aceitando o acordo e clicando em “Avançar”, a próxima tela é um aviso sobre as permissões de pasta, assunto a ser abordado mais adiante.
Devido a restrições na ferramenta escolhida para gerar o arquivo de instalação, o texto abaixo precisou ser escrito sem acentuações.

![image](https://user-images.githubusercontent.com/49456349/229909476-d80a9292-a881-4d5e-af0e-594c11921602.png)

 
Clicando em “Avançar”, é exibido o caminho do diretório onde o software será instalado. Você pode aceitar o diretório padrão clicando em “Avançar” ou selecionar um outro diretório a seu critério clicando em “Procurar”, escolhendo o diretório, e então clicando em “Avançar”.

IMPORTANTE: Não use diretórios cujo caminho possua espaços e/ou caracteres especiais tais como C:\Program Files ou C:\Program Files(x86). Isso pode fazer com que a automação via Agendador de Tarefas do Windows não funcione.

![image](https://user-images.githubusercontent.com/49456349/229909758-021e2027-d157-4a6c-924c-dc8dd59967a1.png)

 
Após clicar em “Avançar”, a tela seguinte lhe dará a opção de criar um atalho na Área de Trabalho. Se desejar criar o atalho, marque a opção “Criar um atalho na área de trabalho”, caso contrário, deixe o campo desmarcado. Após escolher, clique em “Avançar”.

![image](https://user-images.githubusercontent.com/49456349/229909803-0573394b-9144-4b04-b575-553623a92398.png)

 

Após clicar em “Avançar” os detalhes definidos por você durante o processo serão exibidos. Se quiser alterar algo, basta clicar em “Voltar” até chegar na opção que deseja alterar, altere e volte a clicar em “Avançar” até chegar na tela abaixo. Se estiver tudo certo, basta clicar em “Instalar”.

![image](https://user-images.githubusercontent.com/49456349/229909882-d8f5b778-f7b6-4864-a120-ac629788c396.png)

 
Após clicar em “Instalar”, o processo de instalação será iniciado. Basta aguardar que o processo seja concluído.
Caso deseje interromper o processo de instalação, basta clicar em “Cancelar”.

![image](https://user-images.githubusercontent.com/49456349/229909926-0084a3ce-34e7-4f62-9071-81339d8589b0.png)

 
Quando o processo de instalação for concluído, a tela abaixo será exibida. Se você deixar a opção “Iniciar o Planwork Backup” marcada e clicar em “Concluir”, o instalador será encerrado e o software em si será executado. Se não desejar que o software seja iniciado, basta desmarcar a opção e clicar em “Concluir”.

![image](https://user-images.githubusercontent.com/49456349/229909965-a967bbfa-6c97-4bc4-84e1-1d14e39bb5d7.png)

 
<br><h2>Primeiro uso</h2>
Agora que o software está instalado, está na hora de executá-lo pela primeira vez. Ao fazê-lo, a tela abaixo será exibida.

![image](https://user-images.githubusercontent.com/49456349/229910221-77cb59b4-0e99-45df-a808-e73fd12784b0.png)


<br><h3>Detalhes dos campos</h3>

1 – Endereço do servidor (Ex.: 127.0.0.1)<br>
Neste campo deve ser preenchido o endereço do servidor de banco de dados. Caso necessário, a instância do banco de dados deve ser informada junto (Ex.: servidor\sqlexpress).

2 – Usuário<br>
Neste campo deve ser preenchido o usuário que será usado para acessar o banco de dados, e pode ser o mesmo utilizado pelo Evolution.

3 – Senha<br>
Neste campo deve ser preenchida a senha do usuário informado no campo anterior.

4 – Prefixo do banco de dados<br>
Todos os bancos de dados usados pelo Evolution têm seus nomes iniciados por um conjunto de letras e um underscore ( _ ). Neste campo, deve ser preenchido esse conjunto de caracteres. Ex.: sfb_

5 – Nome do cliente<br>
Neste campo deve ser preenchido o nome da empresa, cliente Planwork, que usará o software de backup.

6 – Quantos backups manter (nº de dias)<br>
Neste campo deve ser preenchido a quantidade de versões de backup a serem mantidas. Como ele foi projetado para fazer um backup por dia, o número aqui preenchido corresponde ao número de dias de backup a serem mantidos.

7 – Pasta onde o backup será salvo<br>
Para preencher este campo, é necessário clicar no botão “Procurar” e selecionar a pasta na qual deseja salvar os backups gerados pelo software

<br><h4>Escolhendo a pasta</h4>
Ao clicar em “Procurar”, a tela abaixo será exibida:

![image](https://user-images.githubusercontent.com/49456349/229910316-729e65dc-765f-4dd4-8042-0b9ce27601a1.png)


Será necessário navegar até o diretório onde você deseja que os backups sejam salvos, entrar nele e clicar em “Selecionar pasta”.

Com todos os campos preenchidos, basta clicar em “Salvar.” 

![image](https://user-images.githubusercontent.com/49456349/229910387-4f021118-6165-45e2-8550-fe71b3d91f45.png)

 
Todos os campos nesta tela são obrigatórios. Caso algum dos campos permaneça em branco, não será possível seguir adiante.
Ao clicar em “Salvar” deixando algum campo em branco, a mensagem abaixo será exibida.

![image](https://user-images.githubusercontent.com/49456349/229910437-c37cc929-3aa5-4fd6-ad4b-dee7b19602c9.png)

 
Ao clicar em “OK” a mensagem será fechada e você poderá concluir as configurações.

O campo "Quantos backups manter (Nº de dias)" só aceita valores numéricos inteiros. Caso algo diferente disso seja inserido neste campo, a mensagem abaixo será exibida.

![image](https://user-images.githubusercontent.com/49456349/230103300-e628f340-2965-4f95-a70b-236da3b632fb.png)

Ao clicar em "OK", a janela de alerta será fechada e você poderá corrigir o valor do campo.

<br><h3>Possível erro</h3><br>
Conforme informado anteriormente no processo de instalação, o arquivo de configuração gerado pelas configurações acima é salvo no mesmo diretório onde o software foi instalado. Caso o usuário que executou o software não possua permissão para gravar arquivos nesse diretório, a mensagem abaixo será exibida. Ao clicar em “OK” o software será encerrado.

![image](https://user-images.githubusercontent.com/49456349/229910508-4d1866b9-4d9e-4f84-ae66-f4c63e07aa6c.png)

 
<br><h2>Primeiro backup</h2><br>
Se tudo deu certo ao salvar o arquivo de configuração, a tela abaixo será exibida.

![image](https://user-images.githubusercontent.com/49456349/229910550-ded7c88c-396d-4afd-b1c8-85f067b7af80.png)


Nessa tela, há três opções:

1 – Executar um backup<br>
Selecionando essa opção o software fará um backup do banco de dados, salvando os arquivos resultantes no diretório selecionado nas configurações;

2 – Refazer as configurações<br>
Selecionando essa opção, a janela de configuração será novamente aberta, exibindo os dados preenchidos anteriormente para que o usuário possa revisá-las;

3 – Apenas encerrar o programa<br>
Selecionando essa opção, o software será encerrado;

Clicando em “OK”, a opção selecionada é executada.
Caso a opção escolhida tenha sido “Executar um backup”, o software iniciará o processo de backup, exibindo a mensagem abaixo quando concluir. Clicando em “OK” o software é encerrado.

IMPORTANTE: Para economizar recursos de memória e processamento durante a execução do backup, o processo de backup não exibe dados na tela, tal como barra de progresso ou quaisquer outras informações, apenas exibindo a mensagem abaixo quando o processo estiver concluído.

![image](https://user-images.githubusercontent.com/49456349/229910617-61895dc0-ac84-447b-9479-1e0a81332354.png)
 
Caso algum erro ocorra durante o processo, o software emitirá um alerta e os dados do erro serão armazenados em um arquivo de log, salvo no mesmo diretório onde o backup é salvo.

<br><h2>O arquivo de log</h2><br>
O nome do arquivo de log segue a seguinte estrutura:<br><br>
Cliente_BancoDeDados_AAAA-MM-DD.log<br>
Cliente = Nome preenchido no campo “Nome do cliente” na tela de configurações.<br>
AAAA = Ano, composto por quatro dígitos<br>
MM = Mês, composto por dois dígitos<br>
DD = Dia, composto por dois dígitos<br><br>
Exemplo: Acme_BancoDeDados_2023-03-26.log<br>

<br><h3>O conteúdo do log</h3><br>
Durante o processo, todos os passos executados com sucesso são registrados no arquivo de log. Caso algum dos passos apresente problemas, os dados do erro também serão registrados neste arquivo.

No caso de sucesso na execução do backup, o conteúdo do arquivo de log será semelhante ao exibido abaixo:

![image](https://user-images.githubusercontent.com/49456349/229910778-5fab76fb-462a-486c-b128-6fceb9e81a9a.png)
 

<br><h3>Sobre o backup</h3><br>
O nome do arquivo de backup resultante da execução do software segue a seguinte estrutura:<br><br>
Cliente_BancoDeDados_AAAA-MM-DD.7z<br>
Cliente = Nome preenchido no campo “Nome do cliente” na tela de configurações.<br>
AAAA = Ano, composto por quatro dígitos<br>
MM = Mês, composto por dois dígitos<br>
DD = Dia, composto por dois dígitos<br><br>
Exemplo: Acme_BancoDeDados_2023-03-26.7z<br>


Para a realização completa do backup o software executa diversos passos:

1 Verifica a existência do arquivo de configuração

2 Caso o arquivo não exista, é executado o processo de configuração explicado anteriormente. Caso já exista, a seguinte tela será exibida:

![image](https://user-images.githubusercontent.com/49456349/229910904-d8fb4cea-61d4-4f02-b390-5ee92e060e53.png)


As opções são as mesmas exibidas e explicadas na sessão “Primeiro Backup”<br>
3 – Ao escolher “Executar um backup” o software se conecta ao banco de dados<br>
3.1 – Coleta uma lista de todos os bancos de dados cujo nome se inicia com o prefixo preenchido na tela de configurações<br>
3.2 – Realiza o backup de cada um dos arquivos listados, criando um arquivo com a extensão “.bak” para cada um deles em um diretório temporário dentro daquele que foi escolhido na tela de configurações<br>
3.4 – Após concluir o backup de cada um dos bancos, inicia o processo de compactação. O formato escolhido foi o 7zip, formato gratuito e de código aberto, usando o método de compactação LZMA.<br>
3.5 – Após verificar que a compactação ocorreu corretamente, exclui o diretório temporário e seu conteúdo (arquivos ".bak”), reduzindo o consumo de espaço em disco.<br>
3.6 – Verifica se existem backups mais antigos que o número de dias especificado na tela de configurações. Caso exista, os exclui<br>

<br><h2>Automação</h2><br>
Para tornar o processo de backup automático, o software conta com um parâmetro de linha de comando. Ao utilizar o software com esse parâmetro, duas coisas podem ocorrer:<br>
1 – Se o arquivo de configuração já tiver sido criado, o software é executado de forma oculta, sem exibir telas e/ou alertas e seu funcionamento, correto ou não, poderá ser acompanhado pelo arquivo de log.<br>
2 – Se o arquivo de configuração ainda não existir, o software exibirá a janela de configurações e os passos a serem seguidos serão exatamente como descritos anteriormente. Neste caso, sem os dados necessários para seguir com o procedimento, o backup não será realizado.<br><br>

Para tornar o processo totalmente automático, é necessário configurar o Agendador de Tarefas do Windows de forma que o software seja executado diariamente em horário a ser determinado pelo cliente.<br>
A configuração do Agendador de Tarefas não será abordada aqui, pois cabe ao profissional de TI do cliente fazê-la, porém, uma informação importante precisa ser esclarecida. Ao definir a ação da tarefa agendada, os campos “Adicione argumentos (opcional)” e “Iniciar em (opcional)” devem ser preenchidos.<br>
O campo “Adicione argumentos (opcional)” deve conter o termo “auto” (sem as aspas);<br>
O campo “Iniciar em (opcional)” deve conter o caminho para a pasta onde o software foi instalado.<br>
Como informado anteriormente no descritivo do processo de instalação, o caminho do diretório de instalação, bem como o diretório em si, não pode ter espaços e/ou caracteres especiais. Ex.: C:\Arquivos de Programas(x86). O Agendador de Tarefas do Windows costuma não iniciar a tarefa quando esse tipo de caractere está presente no campo “Iniciar em (opcional)”.<br><br>
A imagem a seguir ilustra o preenchimento padrão dos campos citados acima:

![image](https://user-images.githubusercontent.com/49456349/229910999-576441d7-0d03-45a9-91bd-8b9028d1ebcf.png)


<br><h2>Considerações finais</h2><br>
O software Planwork Backup é oferecido pela Planwork como uma cortesia, a fim de facilitar a automação dos backups de bancos de dados dos nossos clientes. Por ser ofertado como uma cortesia, não há quaisquer garantias de seu correto funcionamento e não será fornecido suporte a este software.
Assim sendo, a empresa e/ou pessoa que adotar o Planwork Backup como ferramenta padrão de backup de bancos de dados isenta a Planwork de todas e quaisquer responsabilidades, assumindo-as para si, bem como todas as consequências resultantes.


