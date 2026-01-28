# HEARTBEAT.md - Tarefas Periódicas

## 📧 Verificar Emails do Igor
- Rodar: `python3 /root/clawd/scripts/check_gmail.py --unread --days 1`
- Alertar sobre emails urgentes (failed deploys, erros, faturas)
- Resumir emails importantes não lidos

## 🔧 Verificar Deploys
- Se houver email de "Failed deployment" da Vercel, investigar e tentar resolver
- Se houver CI failed do GitHub, verificar o erro

## 📊 Status Geral
- Verificar se há tarefas pendentes em memory/
- Atualizar Igor se algo importante aconteceu
