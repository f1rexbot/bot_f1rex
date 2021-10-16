from python_graphql_client import GraphqlClient
from discord.ext import commands
import discord

client = GraphqlClient(endpoint="https://db-f1rex.herokuapp.com/v1/graphql")
sinal = "/"
admins = []

def query(qr):
    return client.execute(query=qr)

adms = (query("query MyQuery { admins(where: {ativo: {_eq: true}}) { nome } }"))['data']['admins']
for adm in adms:
    admins.append(adm['nome'])

chave_bot = str((((query('query MyQuery { chave_bot(where: {ativo: {_eq: true}}) { chave } }'))["data"]["chave_bot"])[0])["chave"])

bot = commands.Bot(sinal)

@bot.event
async def on_ready():
    print(f"Ola sou o F1REX")

@bot.command(name="iniciar")
async def recepição(ctx):
    nome = ctx.author.name
    await ctx.send(f"Ola senhor(a) {nome}\nPara usar o bot, você pode {sinal}filmes para ver todos os filmes ativos\nPode usar {sinal}baixar 'nome do filme' para baixar")

@bot.command(name="filmes")
async def ativos(ctx):
    nome = ctx.author.name
    filmes = (query("query MyQuery { filmes(where: {ativo: { _eq: true } } ) { nome} }"))["data"]["filmes"]
    await ctx.send(f" [!] {nome} [!] Esses são os filmes ativos:")
    for filme in filmes:
        await ctx.send(f"[+] ]===> {filme['nome']}")

@bot.command(name="filmes_baixar")
async def baixar(ctx,*,message):
    nome = ctx.author.name
    link = (query('query MyQuery { filmes(where: {nome: {_eq: "'+message+'" } } ) { link } }'))["data"]["filmes"]
    if(len(link) != 0):
        await ctx.send(f"[!] Aqui está o seu link {str(nome)}: {str(link[0]['link'])} [!]")
    else:
        await ctx.send("[!] O nome do filme está incorreto [!]")

@bot.command(name="filmes_add")
async def add(ctx,*,message):
    if(str(ctx.author) in admins):
        ad = str(message).split()
        if(len(ad) > 1):
            link = str(f"https://docs.google.com/uc?export=download&id={ad[1]}")
            nr = str(ad[0]).replace('_',' ')
            qr = 'mutation MyMutation { insert_filmes(objects: {link: "'+link+'", nome: "'+nr+'", ativo: true}) { returning { id } } }'
            r = query(qr)
            if(len(r['data']['insert_filmes']['returning']) > 0):
                await ctx.send(f"[+] ]====> O filme {nr} foi adicionado com sucesso por {ctx.author.name}")
            else:
                await ctx.send("Erro")
        else:
            await ctx.send(f"Precisa passar dois parametros {sinal}add 'nome' 'id do arquivo'")
    else:
        await ctx.send("Você precisa ter autorização")

@bot.command(name="admin")
async def list_adm(ctx):
    global admins
    if(str(ctx.author) in admins):
        admins = []
        adms = (query("query MyQuery { admins(where: {ativo: {_eq: true}}) { nome } }"))['data']['admins']
        for adm in adms:
            admins.append(adm['nome'])
        list_admins = (query('query MyQuery { admins(where: {ativo: {_eq: true}}) { nome } }'))['data']['admins']
        await ctx.send(f"{ctx.author.name}, os administradores ativos são:")
        for admm in list_admins:
            await ctx.send(f"[&] ]===> {admm['nome']}")
    else:
        await ctx.send("Você precisa de autorização")

@bot.command(name="admin_add")
async def administradores(ctx,*,message):
    global admins
    if(str(ctx.author) in admins):
        a = query('mutation MyMutation { insert_admins(objects: {nome: "'+str(message)+'", ativo: true}) { returning { id } } }')
        admins = []
        adms = (query("query MyQuery { admins(where: {ativo: {_eq: true}}) { nome } }"))['data']['admins']
        for adm in adms:
            admins.append(adm['nome'])
        await ctx.send(f"{ctx.author.name} adicionou {str(message)} como adiministrador")
    else:
        await ctx.send("Você precisa ter autorização para adicionar novos admins")

@bot.command(name="admin_remove")
async def admin_remoce(ctx,*,message):
    global admins
    if(str(ctx.author) in admins):
        admins = []
        re = query('mutation MyMutation { delete_admins(where: {nome: {_eq: "'+str(message)+'"} }) { returning { id } } }')
        adms = (query("query MyQuery { admins(where: {ativo: {_eq: true}}) { nome } }"))['data']['admins']
        for adm in adms:
            admins.append(adm['nome'])
        await ctx.send(f"{ctx.author.name} removeu o cargo de {str(message)}")
        
    else:
        await ctx.send("Você não tem autorização para remover o carco")

@bot.command(name="series")
async def seris(ctx):
    nome = ctx.author.name
    series = (query("query MyQuery { series(where: {ativo: { _eq: true } } ) { nome} }"))["data"]["series"]
    await ctx.send(f" [!] {nome} [!] Esses são os series ativos:")
    for serie in series:
        await ctx.send(f"[+] ]===> {serie['nome']}")

@bot.command(name="series_baixar")
async def baixar(ctx,*,message):
    nome = ctx.author.name
    link = (query('query MyQuery { series(where: {nome: {_eq: "'+message+'" } } ) { link } }'))["data"]["series"]
    if(len(link) != 0):
        await ctx.send(f"[!] Aqui está o seu link {str(nome)}: {str(link[0]['link'])} [!]")
    else:
        await ctx.send("[!] O nome da serie está incorreto [!]")

@bot.command(name="series_add")
async def add(ctx,*,message):
    if(str(ctx.author) in admins):
        ad = str(message).split()
        if(len(ad) > 1):
            link = str(f"https://docs.google.com/uc?export=download&id={ad[1]}")
            nr = str(ad[0]).replace('_',' ')
            qr = 'mutation MyMutation { insert_series(objects: {link: "'+link+'", nome: "'+nr+'", ativo: true}) { returning { id } } }'
            r = query(qr)
            if(len(r['data']['insert_series']['returning']) > 0):
                await ctx.send(f"[+] ]====> A serie {nr} foi adicionado com sucesso por {ctx.author.name}")
            else:
                await ctx.send("Erro")
        else:
            await ctx.send(f"Precisa passar dois parametros {sinal}add 'nome' 'id do arquivo'")
    else:
        await ctx.send("Você precisa ter autorização")

@bot.command(name="comandos")
async def comando(ctx):
    if(str(ctx.author) in admins):
        await ctx.send(f"{ctx.author.name}, esses são os nossos comandos:\n{sinal}iniciar mostra exemplos de como se usa o bot.\n{sinal}filmes mostra os filmes disponiveis.\n{sinal}filmes_baixar 'nome do filme' lhe da o link de download do filme.\n{sinal}filmes_add 'nome do fileme' 'id do filme' adiciona um filme ao bot.\n{sinal}series para ver as seres ativas.\n{sinal}series_baixar 'nome da serie'.\n{sinal}series_add 'nome do series' 'id do series' adiciona um series ao bot.\n{sinal}admin mostra a lista com todos os adminis.\n{sinal}admin_add 'nome do usuario' add um admin.\n{sinal}admin_remove 'nome do usuario' remove o usario do cargo de admin.")
    else:
        await ctx.send(f"{ctx.author.name}, esses são os nossos comandos:\n{sinal}iniciar mostra exemplos de como se usa o bot.\n{sinal}filmes mostra os filmes disponiveis.\n{sinal}filmes_baixar 'nome do filme' lhe da o link de download do filme.\n{sinal}series para ver as seres ativas.\n{sinal}series_baixar 'nome da serie'.")

@bot.event
async def on_message(message):
    if(message.author == bot.user):
        pass
    
    await bot.process_commands(message)

bot.run(chave_bot)