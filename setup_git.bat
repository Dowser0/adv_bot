@echo off
echo ========================================
echo    CONFIGURACAO DO REPOSITORIO GIT
echo ========================================
echo.

REM Verificar se o Git está instalado
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Git nao esta instalado!
    echo Por favor, instale o Git de: https://git-scm.com/
    echo.
    pause
    exit /b 1
)

echo Git encontrado! Versao:
git --version
echo.

REM Verificar se já é um repositório Git
if exist ".git" (
    echo AVISO: Esta pasta ja e um repositorio Git!
    echo.
    echo Status atual:
    git status
    echo.
    echo Remotes configurados:
    git remote -v
    echo.
    pause
    exit /b 0
)

echo Inicializando repositorio Git...
git init

echo.
echo Adicionando arquivos...
git add .

echo.
echo Fazendo primeiro commit...
git commit -m "Initial commit: Advanced WoW Bot with multiple window support"

echo.
echo ========================================
echo    CONFIGURACAO DO REPOSITORIO REMOTO
echo ========================================
echo.
echo Para continuar, voce precisa:
echo 1. Criar um repositorio no GitHub
echo 2. Copiar a URL do repositorio
echo.
echo Exemplo de URL: https://github.com/seuusuario/adv_bot.git
echo.

set /p repo_url="Digite a URL do seu repositorio: "

if "%repo_url%"=="" (
    echo.
    echo Nenhuma URL fornecida. Configuracao cancelada.
    echo.
    echo Para configurar manualmente, execute:
    echo git remote add origin SUA_URL_AQUI
    echo git branch -M main
    echo git push -u origin main
    echo.
    pause
    exit /b 0
)

echo.
echo Configurando repositorio remoto...
git remote add origin "%repo_url%"

echo.
echo Configurando branch principal...
git branch -M main

echo.
echo ========================================
echo    CONFIGURACAO DE AUTENTICACAO
echo ========================================
echo.
echo IMPORTANTE: Para repositorios privados, voce precisa:
echo 1. Criar um Personal Access Token no GitHub
echo 2. Usar o token como senha quando solicitado
echo.
echo Para criar o token:
echo 1. Vá em GitHub.com → Settings → Developer settings
echo 2. Personal access tokens → Tokens (classic)
echo 3. Generate new token → repo (para repositorios privados)
echo.

set /p continue="Pressione ENTER para continuar ou 'n' para cancelar: "

if /i "%continue%"=="n" (
    echo.
    echo Configuracao cancelada.
    echo.
    echo Para enviar manualmente, execute:
    echo git push -u origin main
    echo.
    pause
    exit /b 0
)

echo.
echo Enviando para o GitHub...
echo NOTA: Se solicitado, use seu TOKEN como senha, nao sua senha do GitHub!
echo.

git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo    SUCESSO! REPOSITORIO CONFIGURADO
    echo ========================================
    echo.
    echo Seu projeto foi enviado para o GitHub com sucesso!
    echo.
    echo Comandos uteis:
    echo - git status          : Ver status das alteracoes
    echo - git add .           : Adicionar alteracoes
    echo - git commit -m "msg" : Fazer commit
    echo - git push            : Enviar alteracoes
    echo - git pull            : Baixar alteracoes
    echo.
) else (
    echo.
    echo ========================================
    echo    ERRO AO ENVIAR PARA O GITHUB
    echo ========================================
    echo.
    echo Possiveis causas:
    echo - URL incorreta
    echo - Problemas de autenticacao
    echo - Repositorio nao existe
    echo.
    echo Para tentar novamente:
    echo git push -u origin main
    echo.
)

echo.
pause
