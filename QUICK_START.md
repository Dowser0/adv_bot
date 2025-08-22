# 🚀 Início Rápido - Repositório Privado

## ⚡ Configuração em 3 Passos

### 1. 🎯 Criar Repositório no GitHub
- Acesse [github.com](https://github.com)
- Clique em **"New repository"**
- Nome: `adv_bot`
- **✅ Marque como PRIVADO**
- **❌ NÃO inicialize com README**
- Clique em **"Create repository"**

### 2. 🔑 Criar Token de Acesso
- GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
- **Generate new token**
- **Scopes**: ✅ `repo` (para repositórios privados)
- **Copie o token** e guarde em local seguro

### 3. 🖥️ Executar Script Automático
```bash
# Execute o arquivo:
setup_git.bat
```

**OU** configure manualmente:
```bash
git init
git add .
git commit -m "Initial commit: Advanced WoW Bot"
git remote add origin https://github.com/SEU_USUARIO/adv_bot.git
git branch -M main
git push -u origin main
```

## 🔐 Autenticação
- **Usuário**: seu usuário do GitHub
- **Senha**: use o **TOKEN** (não sua senha)

## 📁 Estrutura Criada
```
adv_bot/
├── .github/          # GitHub Actions, Issues, Dependabot
├── adv_bot.py        # Bot principal
├── adv_bot_gui.py    # Interface gráfica
├── requirements.txt   # Dependências Python
├── setup.py          # Configuração do projeto
├── LICENSE           # Licença MIT
├── CODE_OF_CONDUCT   # Código de conduta
├── .gitignore        # Arquivos ignorados
├── setup_git.bat     # Script de configuração
└── SETUP_REPOSITORY.md # Guia completo
```

## 🎯 Próximos Passos
1. **Configurar colaboradores** (se necessário)
2. **Criar Issues** para planejar melhorias
3. **Configurar branches** para desenvolvimento
4. **Usar Pull Requests** para revisar código

---

**💡 Dica**: Use `setup_git.bat` para configuração automática!
**⚠️ Lembre-se**: Este é um projeto educacional. Use com responsabilidade.
