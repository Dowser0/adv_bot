# 🚀 Configuração do Repositório Git

Este guia te ajudará a configurar um repositório Git privado para o projeto `adv_bot`.

## 📋 Pré-requisitos

- [Git](https://git-scm.com/) instalado no seu computador
- Conta no [GitHub](https://github.com/) (ou outro serviço de Git)
- Python 3.7+ instalado

## 🔧 Passo a Passo

### 1. Criar o Repositório no GitHub

1. Acesse [github.com](https://github.com)
2. Clique no botão **"New"** ou **"+"** → **"New repository"**
3. Configure o repositório:
   - **Repository name**: `adv_bot`
   - **Description**: `Advanced World of Warcraft bot with multiple window support`
   - **Visibility**: ✅ **Private** (recomendado para este tipo de projeto)
   - **Initialize this repository with**: ❌ Não marque nenhuma opção
4. Clique em **"Create repository"**

### 2. Configurar o Repositório Local

Abra o PowerShell na pasta do projeto e execute os comandos:

```powershell
# Inicializar o repositório Git
git init

# Adicionar todos os arquivos
git add .

# Fazer o primeiro commit
git commit -m "Initial commit: Advanced WoW Bot with multiple window support"

# Adicionar o repositório remoto (substitua YOUR_USERNAME pelo seu usuário)
git remote add origin https://github.com/YOUR_USERNAME/adv_bot.git

# Configurar a branch principal
git branch -M main

# Enviar para o GitHub
git push -u origin main
```

### 3. Configurar Informações Pessoais (se necessário)

```powershell
git config user.name "Seu Nome"
git config user.email "seu.email@exemplo.com"
```

### 4. Verificar a Configuração

```powershell
# Verificar o status
git status

# Verificar os remotes
git remote -v

# Verificar as branches
git branch -a
```

## 🔐 Configurações de Segurança

### Autenticação por Token (Recomendado)

1. No GitHub, vá em **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Clique em **"Generate new token"**
3. Configure:
   - **Note**: `adv_bot_local`
   - **Expiration**: Escolha uma data adequada
   - **Scopes**: ✅ `repo` (para repositórios privados)
4. Clique em **"Generate token"**
5. **IMPORTANTE**: Copie o token e guarde em local seguro

### Usar o Token

Quando o Git pedir senha, use o token ao invés da senha do GitHub.

## 📁 Estrutura do Repositório

Após a configuração, seu repositório terá esta estrutura:

```
adv_bot/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── workflows/
│   │   └── python-app.yml
│   └── dependabot.yml
├── adv_bot.py
├── adv_bot_gui.py
├── requirements.txt
├── setup.py
├── README.md
├── README_GUI.md
├── EXEMPLO_USO.md
├── LICENSE
├── CODE_OF_CONDUCT.md
├── .gitignore
├── .gitattributes
├── install.bat
└── install_gui.bat
```

## 🚀 Comandos Úteis

### Enviar Alterações

```powershell
# Ver o status das alterações
git status

# Adicionar arquivos modificados
git add .

# Fazer commit
git commit -m "Descrição das alterações"

# Enviar para o GitHub
git push
```

### Baixar Alterações

```powershell
# Baixar alterações do GitHub
git pull
```

### Ver Histórico

```powershell
# Ver commits
git log --oneline

# Ver diferenças
git diff
```

## 🛡️ Boas Práticas

1. **Commits frequentes**: Faça commits pequenos e frequentes
2. **Mensagens descritivas**: Use mensagens claras nos commits
3. **Branches**: Use branches para novas funcionalidades
4. **Pull Requests**: Use Pull Requests para revisar código
5. **Issues**: Use Issues para reportar bugs e solicitar features

## 🔧 Solução de Problemas

### Erro de Autenticação

```powershell
# Verificar configuração
git config --list

# Reconfigurar usuário
git config user.name "Seu Nome"
git config user.email "seu.email@exemplo.com"
```

### Erro de Push

```powershell
# Forçar push (use com cuidado)
git push -f origin main

# Ou fazer pull primeiro
git pull origin main
git push origin main
```

### Reverter Alterações

```powershell
# Descartar alterações não commitadas
git checkout -- .

# Reverter último commit
git reset --hard HEAD~1
```

## 📞 Suporte

Se encontrar problemas:

1. Verifique a [documentação do Git](https://git-scm.com/doc)
2. Consulte a [documentação do GitHub](https://docs.github.com/)
3. Use o comando `git help <comando>` para ajuda específica

## 🎯 Próximos Passos

Após configurar o repositório:

1. **Configurar GitHub Actions** para CI/CD
2. **Configurar Dependabot** para atualizações automáticas
3. **Criar Issues** para planejar melhorias
4. **Configurar branches** para desenvolvimento
5. **Adicionar colaboradores** se necessário

---

**⚠️ Lembre-se**: Este é um projeto educacional. Use com responsabilidade e sempre respeite os Termos de Serviço dos jogos.
